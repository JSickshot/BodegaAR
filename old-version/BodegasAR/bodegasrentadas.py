import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from datetime import datetime, timedelta


class BodegasRentadas(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        self.conn = sqlite3.connect("bodegas.db")
        self.c = self.conn.cursor()
        
        self.bodegas_disponibles = self.obtener_bodegas_disponibles()
        self.combo_bodegas = ttk.Combobox(self, values=self.bodegas_disponibles, state="readonly", font=("Arial", 12))
        self.combo_bodegas.pack(side="top", padx=5, pady=5)
        
        self.btn_rentar = tk.Button(self, text="Rentar", command=self.rentar_bodega, font=("Arial", 12))
        self.btn_rentar.pack(side="bottom", padx=5, pady=5, fill="x")

        self.btn_regresar = tk.Button(self, text="Regresar", command=self.regresar, font=("Arial", 12))
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
