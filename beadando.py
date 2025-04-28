from abc import ABC, abstractmethod
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from ttkthemes import ThemedTk


class Jarat(ABC):
    def __init__(self, jaratszam, celallomas, indulasi_ido, jegyar):
        self.jaratszam = jaratszam
        self.celallomas = celallomas
        self.indulasi_ido = indulasi_ido
        self.jegyar = jegyar
        self.foglalasok = []

    @abstractmethod
    def jegy_ara(self):
        pass

    def foglalas_hozzaad(self, foglalas):
        self.foglalasok.append(foglalas)
        return True

    def foglalas_torol(self, foglalas):
        if foglalas in self.foglalasok:
            self.foglalasok.remove(foglalas)
            return True
        return False

    def __str__(self):
        return f"{self.jaratszam} - {self.celallomas} - {self.indulasi_ido.strftime('%Y-%m-%d %H:%M')} - {self.jegy_ara():,.0f} Ft"

class BelfoldiJarat(Jarat):
    def jegy_ara(self):
        return self.jegyar * 0.9  # 10% kedvezmény belföldi járatokra

class NemzetkoziJarat(Jarat):
    def jegy_ara(self):
        return self.jegyar * 1.2  # 20% felár nemzetközi járatokra

class Legitarsasag:
    def __init__(self, nev):
        self.nev = nev
        self.jaratok = []

    def jarat_hozzaad(self, jarat):
        self.jaratok.append(jarat)
        return True

    def jarat_keres(self, jaratszam):
        for jarat in self.jaratok:
            if jarat.jaratszam.upper() == jaratszam.upper(): # Kis/nagybetű érzéketlen keresés
                return jarat
        return None

class JegyFoglalas:
    def __init__(self, jarat, utas_neve, foglalas_idopontja):
        self.jarat = jarat
        self.utas_neve = utas_neve
        self.foglalas_idopontja = foglalas_idopontja
        self.ar = jarat.jegy_ara()

    def __str__(self):
        return (f"\n\tJáratszám: \t\t{self.jarat.jaratszam}\n"
                f"\tCélállomás: \t\t{self.jarat.celallomas}\n"
                f"\tIndulás: \t\t{self.jarat.indulasi_ido.strftime('%Y-%m-%d %H:%M')}\n"
                f"\tUtas neve: \t\t{self.utas_neve}\n"
                f"\tFoglalás ideje: {self.foglalas_idopontja.strftime('%Y-%m-%d %H:%M')}\n"
                f"\tÁr: \t\t{self.ar:,.0f} Ft")

class RepulojegyRendszer:
    def __init__(self):
        self.legitarsasag = Legitarsasag("Python Airlines")
        self._inicializalas()

    def _inicializalas(self):
        # Belföldi járatok
        bf1 = BelfoldiJarat("BF123", "Budapest", datetime(2025, 7, 1, 10, 30), 5000)
        bf2 = BelfoldiJarat("BF456", "Debrecen", datetime(2025, 7, 2, 12, 45), 8000)

        # Nemzetközi járatok
        nk1 = NemzetkoziJarat("NK789", "London", datetime(2025, 7, 3, 8, 15), 15000)

        self.legitarsasag.jarat_hozzaad(bf1)
        self.legitarsasag.jarat_hozzaad(bf2)
        self.legitarsasag.jarat_hozzaad(nk1)

        # Kezdeti foglalások
        self.foglalas_letrehozasa(bf1, "Kiss Péter", datetime.now())
        self.foglalas_letrehozasa(bf1, "Nagy Anna", datetime.now())
        self.foglalas_letrehozasa(bf2, "Kovács István", datetime.now())
        self.foglalas_letrehozasa(bf2, "Tóth Éva", datetime.now())
        self.foglalas_letrehozasa(nk1, "Szabó Gábor", datetime.now())
        self.foglalas_letrehozasa(nk1, "Horváth Zsuzsa", datetime.now())

    def foglalas_letrehozasa(self, jarat, utas_neve, foglalas_idopontja):
        if jarat and utas_neve and foglalas_idopontja:
             # Egyszerűsített ellenőrzés: Van-e már foglalás ezen a néven erre a járatra?
            for foglalas in jarat.foglalasok:
                if foglalas.utas_neve.lower() == utas_neve.lower():
                     # Itt lehetne összetettebb logika, pl. helyek száma alapján
                     # messagebox.showwarning("Figyelmeztetés", f"{utas_neve} már rendelkezik foglalással erre a járatra.")
                     # return None # Vagy engedjük többször foglalni ugyanannak az embernek? Most engedjük.
                     pass

            foglalas = JegyFoglalas(jarat, utas_neve, foglalas_idopontja)
            jarat.foglalas_hozzaad(foglalas)
            return foglalas
        return None

    def foglalas_lemondasa(self, jaratszam, utas_neve):
        jarat = self.legitarsasag.jarat_keres(jaratszam)
        if jarat:
            # Fontos: A lista másolatán iterálunk, hogy törölni tudjunk belőle iterálás közben
            for foglalas in jarat.foglalasok[:]:
                # Kis/nagybetű érzéketlen összehasonlítás
                if foglalas.utas_neve.lower() == utas_neve.lower():
                    jarat.foglalas_torol(foglalas)
                    return True
        return False # Akkor is False, ha a járat megvan, de az utas nincs rajta

    def osszes_foglalas_listazasa(self):
        osszes_foglalas = []
        for jarat in self.legitarsasag.jaratok:
            osszes_foglalas.extend(jarat.foglalasok)
        return osszes_foglalas

    

    def elerheto_jaratok_listazasa(self, celallomas=None, jarat_tipus=None, datum=None):
      
        szurt_jaratok = []
        
        for jarat in self.legitarsasag.jaratok:
            # Célállomás szerinti szűrés (részleges egyezés)
            if celallomas and celallomas.lower() not in jarat.celallomas.lower():
                continue
                
            # Járat típusa szerinti szűrés (BF/NK prefix alapján)
            if jarat_tipus:
                jarat_prefix = jarat.jaratszam[:2].upper()  # Az első 2 karakter
                if (jarat_tipus.lower() == 'belföldi' and jarat_prefix != 'BF') or \
                   (jarat_tipus.lower() == 'nemzetközi' and jarat_prefix != 'NK'):
                    continue
            
            # Dátum szerinti szűrés
            if datum and jarat.indulasi_ido.date() != datum:
                continue
                
            # Csak jövőbeli járatokat jelenítünk meg
            if jarat.indulasi_ido <= datetime.now():
                continue
                
            szurt_jaratok.append(jarat)
            
        return szurt_jaratok

class RepulojegyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Airlines - Repülőjegy Foglalási Rendszer")
    
        self.root.minsize(600, 400) 

        self.rendszer = RepulojegyRendszer()

        self.configure_styles()

        self.create_widgets()

    def configure_styles(self):
        style = ttk.Style()
        style.configure('TButton', padding=6, relief="flat", font=('Segoe UI', 10))
        style.configure('Title.TLabel', font=('Segoe UI', 20, 'bold'), padding=(10, 15), foreground='blue')
        style.configure('Header.TLabel', font=('Segoe UI', 12, 'bold'), padding=(0, 10))
        style.configure('TFrame', padding=10)
        style.configure('TLabel', font=('Segoe UI', 10), padding=5)
        style.configure('TEntry', padding=5, font=('Segoe UI', 10))
        style.configure('TCombobox', padding=5, font=('Segoe UI', 10))

        self.text_bg = style.lookup('TFrame', 'background') 
        self.text_fg = style.lookup('TLabel', 'foreground') 
        
        

    def create_widgets(self):
        # Fő keret
        self.main_frame = ttk.Frame(self.root, padding=15)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.main_frame.columnconfigure(0, weight=1) 
        self.main_frame.rowconfigure(2, weight=1)    

        # Cím
        title_label = ttk.Label(
            self.main_frame,
            text="Python Airlines",
            style='Title.TLabel',
            anchor='center'
        )

        title_label.grid(row=0, column=0, pady=(0, 25), sticky="nsew")

        # Gombok kerete
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=1, column=0, pady=10, sticky="ew") 

        buttons = [
            ("Járatok", self.list_flights),
            ("Foglalás", self.book_ticket),
            ("Lemondás", self.cancel_booking),
            ("Foglalások", self.list_bookings),
            ("Kilépés", self.root.quit)
        ]

        # Gombok egyenletes elosztása a grid segítségével
        for i, (text, command) in enumerate(buttons):
            btn = ttk.Button(button_frame, text=text, command=command)
            btn.grid(row=0, column=i, padx=5, pady=5, sticky="ew")
            button_frame.columnconfigure(i, weight=1) 

        # Külső frame, amely kitölti az elérhető teret
        result_outer_frame = ttk.Frame(self.main_frame, padding=(0, 10, 0, 0))
        result_outer_frame.grid(row=2, column=0, sticky="nsew")

        # A fő keret rugalmas a 2. sorban és 0. oszlopban
        self.main_frame.rowconfigure(2, weight=1)
        self.main_frame.columnconfigure(0, weight=1)

        # A külső frame konfigurálása 5 oszlopra paddinggel
        for i in range(5):
            result_outer_frame.columnconfigure(i, weight=1, pad=5)  # 5 pixel padding minden oszlop között
        result_outer_frame.rowconfigure(0, weight=1)  # Függőleges középre igazítás

        # Belső frame (a 3. oszlopnál kezdődik és 3 oszlop széles)
        result_inner_frame = ttk.Frame(result_outer_frame)
        result_inner_frame.grid(
            row=0,
            column=3,          # 3. oszlop (0-tól indexelünk)
            columnspan=3,      # 3 oszlop széles (2-3-4)
            pady=30,           # Függőleges margó
            sticky="nsew"
        )

        # A Text widget (kitölti a belső frame-et)
        self.result_text = tk.Text(
            result_inner_frame,
            wrap=tk.WORD,
            font=("Consolas", 11),
            padx=10,
            pady=10,
            bd=0,
            relief=tk.FLAT,
            bg=self.text_bg,
            fg=self.text_fg,
        )
        self.result_text.grid(row=0, column=0, sticky="nsew")

        # A belső frame súlyozása
        result_inner_frame.rowconfigure(0, weight=1)
        result_inner_frame.columnconfigure(0, weight=1)
        
        # # Görgetősáv a Text widgethez (ttk stílusú)
        # scrollbar = ttk.Scrollbar(result_outer_frame, command=self.result_text.yview)
        # scrollbar.grid(row=0, column=1, sticky="ns") # ns = north-south (függőleges kitöltés)
        # self.result_text.config(yscrollcommand=scrollbar.set)
        

    def clear_result(self):
        self.result_text.config(state=tk.NORMAL) # Írhatóvá tesszük a törléshez
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state=tk.DISABLED) # Visszaállítjuk csak olvashatóra

    def display_in_result(self, header, content_list):
        self.clear_result()
        self.result_text.config(state=tk.NORMAL)
        self.result_text.insert(tk.END, header + "\n", 'header')
        
        # Színes címkék definiálása
        self.result_text.tag_configure('bf_jarat', foreground='green')
        self.result_text.tag_configure('nk_jarat', foreground='blue')
        
        if content_list:
            for item in content_list:
                # Megnézzük, hogy a sor BF vagy NK járatszámmal kezdődik-e
                if str(item).strip().startswith("BF"):
                    self.result_text.insert(tk.END, f"{item}\n", 'bf_jarat')
                elif str(item).strip().startswith("NK"):
                    self.result_text.insert(tk.END, f"{item}\n", 'nk_jarat')
                else:
                    self.result_text.insert(tk.END, f"{item}\n")
                
                self.result_text.insert(tk.END, "-" * 50 + "\n") # Elválasztó
        else:
            self.result_text.insert(tk.END, "Nincs megjeleníthető adat.\n")

        self.result_text.tag_configure('header', font=('Segoe UI', 12, 'bold'), spacing1=5, spacing3=5)
        self.result_text.config(state=tk.DISABLED)

    def list_flights(self):
        jaratok = self.rendszer.elerheto_jaratok_listazasa()
        self.display_in_result("\t\tELÉRHETŐ JÁRATOK\n\n", jaratok)

    def list_bookings(self):
        foglalasok = self.rendszer.osszes_foglalas_listazasa()
        formatted_bookings = []
        for idx, foglalas in enumerate(foglalasok, 1):
             formatted_bookings.append(f"\n\t\t--- Foglalás #{idx} ---\n{foglalas}\n")
        self.display_in_result("\t\tÖSSZES FOGLALÁS\n\n", formatted_bookings)
        # Opcionálisan hozzáadhatunk egy összefoglalót
        self.result_text.config(state=tk.NORMAL)
        if foglalasok:
            self.result_text.insert(tk.END, f"\nÖsszesen {len(foglalasok)} foglalás.\n")
        self.result_text.config(state=tk.DISABLED)




    def foglalas_letrehozasa(self, jarat, utas_neve, foglalas_idopontja):
        if not jarat or not utas_neve or not foglalas_idopontja:
            return None
            
        # Ellenőrizzük, hogy a járat indulási ideje a jövőben van-e
        if jarat.indulasi_ido <= datetime.now():
            messagebox.showwarning("Figyelmeztetés", "Ez a járat már elindult, nem foglalható.")
            return None
            
        # Ellenőrizzük, hogy a foglalás időpontja érvényes (nem múltbeli)
        if foglalas_idopontja > datetime.now():
            messagebox.showwarning("Figyelmeztetés", "A foglalás időpontja nem lehet a jövőben.")
            return None
            
        # Ellenőrizzük, hogy van-e még szabad hely (egyszerűsített változat)
        if len(jarat.foglalasok) >= 10:  # Például max 10 foglalás
            messagebox.showwarning("Figyelmeztetés", "Nincs szabad hely ezen a járaton.")
            return None

        foglalas = JegyFoglalas(jarat, utas_neve, foglalas_idopontja)
        jarat.foglalas_hozzaad(foglalas)
        return foglalas


    def book_ticket(self):
        booking_window = tk.Toplevel(self.root)
        booking_window.title("Jegy Foglalása")
        booking_window.resizable(False, False) 

        frame = ttk.Frame(booking_window, padding=15)
        frame.pack(fill=tk.BOTH, expand=True)

        frame.columnconfigure(1, weight=1) 

        ttk.Label(frame, text="Járat:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        jaratok = self.rendszer.elerheto_jaratok_listazasa() #Alapbol a meglévő járatok az opciók
        jarat_options = [f"{j.jaratszam}: {j.celallomas} ({j.indulasi_ido.strftime('%Y-%m-%d %H:%M')})" for j in jaratok]
        if not jaratok:
             messagebox.showinfo("Információ", "Jelenleg nincsenek elérhető járatok.", parent=booking_window)
             booking_window.destroy()
             return

        jarat_var = tk.StringVar()
        jarat_combobox = ttk.Combobox(
            frame,
            textvariable=jarat_var,
            values=jarat_options,
            state="readonly",
            width=40 
        )
        jarat_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        if jarat_options:
            jarat_combobox.current(0) 

        
        ttk.Label(frame, text="Utas neve:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        name_entry = ttk.Entry(frame, width=40) 
        name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        name_entry.focus() 

        def confirm_booking():
            selected = jarat_var.get()
            if not selected:
                messagebox.showerror("Hiba", "Válasszon járatot!", parent=booking_window)
                return

            try:
                jaratszam = selected.split(":")[0].strip()
            except IndexError:
                messagebox.showerror("Hiba", "Érvénytelen járat formátum.", parent=booking_window)
                return

            utas_neve = name_entry.get().strip()
            if not utas_neve:
                messagebox.showerror("Hiba", "Adja meg az utas nevét!", parent=booking_window)
                return

            jarat = self.rendszer.legitarsasag.jarat_keres(jaratszam)
            if jarat:
                foglalas = self.rendszer.foglalas_letrehozasa(jarat, utas_neve, datetime.now())
                if foglalas:
                    ar = foglalas.ar
                    messagebox.showinfo("Siker", 
                                    f"Foglalás '{utas_neve}' részére a {jaratszam} járatra sikeresen rögzítve!\n"
                                    f"Jegy ára: {ar:,.0f} Ft", 
                                    parent=booking_window)
                    booking_window.destroy()
                    self.list_bookings()
                else:
                    messagebox.showerror("Hiba", "Hiba történt a foglalás során.", parent=booking_window)
            else:
                messagebox.showerror("Hiba", f"Nem található járat ezzel a járatszámmal: {jaratszam}", parent=booking_window)


        button_frame_popup = ttk.Frame(frame)
        button_frame_popup.grid(row=2, column=0, columnspan=2, pady=(15, 0))

        confirm_button = ttk.Button(
            button_frame_popup,
            text="Foglalás",
            command=confirm_booking
        )
        confirm_button.pack(side=tk.LEFT, padx=5)

        cancel_button = ttk.Button(
            button_frame_popup,
            text="Mégse",
            command=booking_window.destroy
        )
        cancel_button.pack(side=tk.LEFT, padx=5)

        booking_window.bind('<Return>', lambda event: confirm_booking())


    def cancel_booking(self):
        cancel_window = tk.Toplevel(self.root)
        cancel_window.title("Foglalás Lemondása")
        cancel_window.resizable(False, False)

        frame = ttk.Frame(cancel_window, padding=15)
        frame.pack(fill=tk.BOTH, expand=True)
        frame.columnconfigure(1, weight=1)

        ttk.Label(frame, text="Járatszám:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        flight_entry = ttk.Entry(frame, width=30)
        flight_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        flight_entry.focus() 

        ttk.Label(frame, text="Utas neve:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        name_entry = ttk.Entry(frame, width=30)
        name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        def confirm_cancel():
            jaratszam = flight_entry.get().strip().upper() 
            utas_neve = name_entry.get().strip()

            if not jaratszam or not utas_neve:
                messagebox.showerror("Hiba", "Mindkét mezőt ki kell tölteni!", parent=cancel_window)
                return

            jarat = self.rendszer.legitarsasag.jarat_keres(jaratszam)
            if not jarat:
                messagebox.showerror("Hiba", f"Nem található járat a(z) {jaratszam} járatszámmal!", parent=cancel_window)
                return

            if jarat.indulasi_ido <= datetime.now():
                messagebox.showerror("Hiba", "Ez a járat már elindult, a foglalás nem mondható le.", parent=cancel_window)
                return

            foglalas = next((f for f in jarat.foglalasok 
                            if f.utas_neve.lower() == utas_neve.lower()), None)
            if not foglalas:
                messagebox.showerror("Hiba", 
                                f"Nem található foglalás '{utas_neve}' névvel a {jaratszam} járaton.",
                                parent=cancel_window)
                return

            time_left = jarat.indulasi_ido - datetime.now()
            if time_left.total_seconds() < 3600:  # 1 órán belül
                messagebox.showerror("Hiba", 
                                "Az indulásig kevesebb mint 1 óra van, a foglalás már nem mondható le.",
                                parent=cancel_window)
                return

            # Megerősítés kérése
            confirm = messagebox.askyesno(
                "Megerősítés",
                f"Biztosan törölni szeretné '{utas_neve}' foglalását a {jaratszam} járatról?\n"
                f"Indulás: {jarat.indulasi_ido.strftime('%Y-%m-%d %H:%M')}\n"
                f"Jegy ára: {foglalas.ar:,.0f} Ft",
                parent=cancel_window
            )

            if confirm:
                if self.rendszer.foglalas_lemondasa(jaratszam, utas_neve):
                    messagebox.showinfo("Siker", "A foglalás sikeresen törölve.", parent=cancel_window)
                    cancel_window.destroy()
                    self.list_bookings()  # Frissítjük a listát
                else:
                    messagebox.showerror("Hiba", 
                                    "Hiba történt a foglalás törlése közben.",
                                    parent=cancel_window)

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(15, 0))

        confirm_button = ttk.Button(
            button_frame,
            text="Lemondás",
            command=confirm_cancel
        )
        confirm_button.pack(side=tk.LEFT, padx=5)

        cancel_button = ttk.Button(
            button_frame,
            text="Mégse",
            command=cancel_window.destroy
        )
        cancel_button.pack(side=tk.LEFT, padx=5)

        # Enter lenyomására is működjön
        cancel_window.bind('<Return>', lambda event: confirm_cancel())
        
        
        
    def list_flights(self):
        # Szűrési ablak létrehozása
        filter_window = tk.Toplevel(self.root)
        filter_window.title("Járat Szűrése (Bezáráskor az összes listázódik)")
        filter_window.resizable(False, False)
        
        frame = ttk.Frame(filter_window, padding=15)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Város szerinti szűrés (opcionális)
        ttk.Label(frame, text="Célállomás (részlet is lehet):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        city_entry = ttk.Entry(frame)
        city_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        city_entry.insert(0, "")  # Üres alapértelmezett érték
        
        # Járat típusa (opcionális)
        ttk.Label(frame, text="Járat típusa:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        flight_type = tk.StringVar()
        flight_type_combobox = ttk.Combobox(
            frame, 
            textvariable=flight_type,
            values=["Mindegy", "Belföldi", "Nemzetközi"],
            state="readonly"
        )
        flight_type_combobox.current(0)
        flight_type_combobox.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        # Dátum szerinti szűrés (opcionális)
        ttk.Label(frame, text="Dátum (éééé-hh-nn):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        date_entry = ttk.Entry(frame)
        date_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        date_entry.insert(0, "")  # Üres alapértelmezett érték
        
        def apply_filters():
            try:
                # Szűrési paraméterek kinyerése - mind opcionális
                celallomas = city_entry.get().strip() or None
                tipus = flight_type.get().lower() if flight_type.get() != "Mindegy" else None
                
                # Dátum feldolgozása (ha meg van adva)
                datum_str = date_entry.get().strip()
                datum = None
                if datum_str:  # Csak akkor próbáljuk feldolgozni, ha nem üres
                    datum = datetime.strptime(datum_str, "%Y-%m-%d").date()
                
                # Járatok szűrése (bármelyik paraméter lehet None)
                jaratok = self.rendszer.elerheto_jaratok_listazasa(
                    celallomas=celallomas,
                    jarat_tipus=tipus,
                    datum=datum
                )
                
                # Eredmény megjelenítése
                if jaratok:
                    self.display_in_result("\t\tSZŰRT JÁRATOK\n\n", jaratok)
                else:
                    self.display_in_result("\t\tSZŰRT JÁRATOK\n\n", ["Nincs találat a megadott szűrőkkel!"])
                
                filter_window.destroy()
                
            except ValueError as e:
                messagebox.showerror("Hiba", f"Érvénytelen dátum formátum! Használj éééé-hh-nn formátumot vagy hagyd üresen.\nHiba: {str(e)}", parent=filter_window)
        
        # Gombok
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=(10, 0))
        
        filter_button = ttk.Button(
            button_frame,
            text="Szűrés",
            command=apply_filters
        )
        filter_button.pack(side=tk.LEFT, padx=5)
        
        cancel_button = ttk.Button(
            button_frame,
            text="Mégse",
            command=filter_window.destroy
        )
        cancel_button.pack(side=tk.LEFT, padx=5)
        
        # Minden mező opcionális, alapértelmezett üres értékekkel
        def on_close():
            jaratok = self.rendszer.elerheto_jaratok_listazasa()
            self.display_in_result("\t\tELÉRHETŐ JÁRATOK\n\n", jaratok)
            filter_window.destroy()
            
        filter_window.protocol("WM_DELETE_WINDOW", on_close)
        
        # Enter-re is szűrjen bármelyik mezőben
        city_entry.bind('<Return>', lambda e: apply_filters())
        flight_type_combobox.bind('<Return>', lambda e: apply_filters())
        date_entry.bind('<Return>', lambda e: apply_filters())

def main():
    try:
        root = ThemedTk() 
    except tk.TclError:
        root = tk.Tk()

    app = RepulojegyApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()