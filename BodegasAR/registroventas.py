import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from datetime import datetime, timedelta

class RegistroVentas(tk.Frame):
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
