import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from datetime import datetime, timedelta
from PIL import Image, ImageTk
import random

class FullscreenApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight()))
        self.bind('<Escape>', self.toggle_fullscreen)
        
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        self.show_frame(PuntoDeVentaApp)
    
    def toggle_fullscreen(self, event=None):
        self.attributes('-fullscreen', not self.attributes('-fullscreen'))
    
    def show_frame(self, cont):
        frame = cont(self.container, self)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

class PuntoDeVentaApp(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        self.image = Image.open("C:/Users/julio/Documents/BodegaAR/BodegasAR/image/ar.jpg")
        self.photo = ImageTk.PhotoImage(self.image)

        self.conn = sqlite3.connect("bodegas.db")
        self.c = self.conn.cursor()
        
        self.c.execute('''CREATE TABLE IF NOT EXISTS bodegas (
                            id INTEGER PRIMARY KEY,
                            numero INTEGER,
                            ocupada BOOLEAN,
                            fecha_inicio DATE,
                            fecha_fin DATE,
                            pagado BOOLEAN,
                            tarifa REAL,
                            nombre TEXT,
                            apellido_paterno TEXT,
                            apellido_materno TEXT
                         )''')
        
        self.c.execute('''SELECT COUNT(*) FROM bodegas''')
        if self.c.fetchone()[0] == 0:
            self.insertar_bodegas()
        
        self.frame_principal = tk.Frame(self, padx=20, pady=20)
        self.frame_principal.pack(expand=True, fill="both")
        
        self.label_imagen = tk.Label(self.frame_principal, image=self.photo)
        self.label_imagen.pack(expand=True, fill="both")
        
        self.btn_registrar_nueva_renta = tk.Button(self.frame_principal, text="Registrar Nueva Renta", command=self.mostrar_interfaz_registro, font=("Arial", 12))
        self.btn_registrar_nueva_renta.pack(side="left", padx=5, pady=5, expand=True, fill="both")

        self.btn_ver_bodegas = tk.Button(self.frame_principal, text="Ver Bodegas Rentadas", command=self.ver_bodegas_rentadas, font=("Arial", 12), bg="lightblue")
        self.btn_ver_bodegas.pack(side="left", padx=5, pady=5, expand=True, fill="both")

    def insertar_bodegas(self):
        for i in range(1, 21):
            self.c.execute('''INSERT INTO bodegas (numero, ocupada, tarifa) VALUES (?, ?, ?)''', (i, False, 1500))
        self.conn.commit()
    
    def ver_bodegas_rentadas(self):
        bodegas_rentadas = []
        today = datetime.now().strftime("%Y-%m-%d")
        self.c.execute('''SELECT id, numero, fecha_inicio, fecha_fin, pagado, nombre, apellido_paterno, apellido_materno FROM bodegas WHERE ocupada = 1 AND fecha_fin < ?''', (today,))
        for bodega in self.c.fetchall():
            bodegas_rentadas.append(f"Folio: {self.generar_folio()}\nBodega {bodega[1]}:\nFecha de inicio: {bodega[2]}\nFecha de fin: {bodega[3]}\nPagado: {'Sí' if bodega[4] else 'No'}\nNombre: {bodega[5]}\nApellido Paterno: {bodega[6]}\nApellido Materno: {bodega[7]}\n{'-'*30}")
        
        if not bodegas_rentadas:
            messagebox.showinfo("Bodegas Rentadas", "No hay bodegas rentadas actualmente.")
        else:
            message = "\n\n".join(bodegas_rentadas)
            self.mostrar_ventana_emergente("Bodegas Rentadas", message)
        
    def generar_folio(self):
        return str(random.randint(10000, 99999))
        
    def mostrar_ventana_emergente(self, title, message):
        top = tk.Toplevel()
        top.title(title)
        
        top.geometry("400x400")  
        
        frame = tk.Frame(top)
        frame.pack(expand=True, fill="both")
        
        text = tk.Text(frame, wrap="word", font=("Arial", 12), padx=20, pady=20)
        text.pack(expand=True, fill="both")
        
        text.insert("1.0", message)
        
        text.tag_configure("center", justify='center')
        text.tag_add("center", "1.0", "end")
        text.config(state="disabled")

        scrollbar = tk.Scrollbar(frame, command=text.yview)
        scrollbar.pack(side="right", fill="y")
        text.config(yscrollcommand=scrollbar.set)

    def mostrar_interfaz_registro(self):
        self.controller.show_frame(RegistroRentasApp)

    def pagar_renta(self):
        bodega_seleccionada = self.combo_bodegas.get()
        self.c.execute('''UPDATE bodegas SET pagado = 1 WHERE numero = ?''', (bodega_seleccionada,))
        self.conn.commit()
        messagebox.showinfo("Éxito", f"Se ha registrado el pago de la renta de la Bodega {bodega_seleccionada}.")

class RegistroRentasApp(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        self.conn = sqlite3.connect("bodegas.db")
        self.c = self.conn.cursor()
        
        self.frame_registro = tk.Frame(self, padx=20, pady=20)
        self.frame_registro.pack(expand=True, fill="both")
        
        self.label_titulo = tk.Label(self.frame_registro, text="Registrar Nueva Renta", font=("Arial", 18, "bold"))
        self.label_titulo.pack()
        
        self.label_nombre = tk.Label(self.frame_registro, text="Nombre(s):", font=("Arial", 12))
        self.label_nombre.pack(side="top", padx=5, pady=5)
        
        self.entry_nombre = tk.Entry(self.frame_registro, font=("Arial", 12))
        self.entry_nombre.pack(side="top", padx=5, pady=5)
        
        self.label_apellido_paterno = tk.Label(self.frame_registro, text="Apellido Paterno:", font=("Arial", 12))
        self.label_apellido_paterno.pack(side="top", padx=5, pady=5)
        
        self.entry_apellido_paterno = tk.Entry(self.frame_registro, font=("Arial", 12))
        self.entry_apellido_paterno.pack(side="top", padx=5, pady=5)
        
        self.label_apellido_materno = tk.Label(self.frame_registro, text="Apellido Materno:", font=("Arial", 12))
        self.label_apellido_materno.pack(side="top", padx=5, pady=5)
        
        self.entry_apellido_materno = tk.Entry(self.frame_registro, font=("Arial", 12))
        self.entry_apellido_materno.pack(side="top", padx=5, pady=5)
        
        self.label_subtitulo = tk.Label(self.frame_registro, text="Seleccione una bodega para rentar:", font=("Arial", 12))
        self.label_subtitulo.pack(side="top", padx=5, pady=5)
        
        self.bodegas_disponibles = self.obtener_bodegas_disponibles()
        self.combo_bodegas = ttk.Combobox(self.frame_registro, values=self.bodegas_disponibles, state="readonly", font=("Arial", 12))
        self.combo_bodegas.pack(side="top", padx=5, pady=5)
        
        self.label_fecha_actual = tk.Label(self.frame_registro, text="Fecha actual:", font=("Arial", 12))
        self.label_fecha_actual.pack(side="top", padx=5, pady=5)
        
        self.entry_fecha_actual = tk.Entry(self.frame_registro, font=("Arial", 12))
        self.entry_fecha_actual.pack(side="top", padx=5, pady=5)
        self.entry_fecha_actual.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        self.btn_rentar = tk.Button(self.frame_registro, text="Rentar", command=self.rentar_bodega, font=("Arial", 12))
        self.btn_rentar.pack(side="bottom", padx=5, pady=5, fill="x")

        self.btn_regresar = tk.Button(self.frame_registro, text="Regresar", command=self.regresar, font=("Arial", 12))
        self.btn_regresar.pack(side="bottom", padx=5, pady=5, fill="x")
        
    def obtener_bodegas_disponibles(self):
        self.c.execute('''SELECT numero FROM bodegas WHERE ocupada = 0''')
        bodegas_libres = self.c.fetchall()
        return [bodega[0] for bodega in bodegas_libres]
    
    def rentar_bodega(self):
        bodega_seleccionada = self.combo_bodegas.get()
        fecha_inicio = self.entry_fecha_actual.get()
        nombre = self.entry_nombre.get()
        apellido_paterno = self.entry_apellido_paterno.get()
        apellido_materno = self.entry_apellido_materno.get()
        
        if not fecha_inicio:
            messagebox.showerror("Error", "Por favor ingrese la fecha de inicio.")
            return
        
        fecha_fin = (datetime.now() + timedelta(days=15)).strftime("%Y-%m-%d")
        
        self.c.execute('''UPDATE bodegas SET ocupada = 1, fecha_inicio = ?, fecha_fin = ?, nombre = ?, apellido_paterno = ?, apellido_materno = ? WHERE numero = ?''', (fecha_inicio, fecha_fin, nombre, apellido_paterno, apellido_materno, bodega_seleccionada))
        self.conn.commit()
        
        self.combo_bodegas["values"] = self.obtener_bodegas_disponibles()  
        messagebox.showinfo("Éxito", f"Bodega {bodega_seleccionada} rentada exitosamente.")
        
    def regresar(self):
        self.controller.show_frame(PuntoDeVentaApp)

if __name__ == "__main__":
    app = FullscreenApp()
    app.mainloop()
