import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from registroventas import RegistroVentas
from bodegasrentadas import BodegasRentadas


class InicioApp(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        self.image = Image.open("C:/Users/julio/Documents/BodegaAR/BodegasAR/image/ar.jpg")
        self.photo = ImageTk.PhotoImage(self.image)
        
        self.frame_principal = tk.Frame(self, padx=20, pady=20)
        self.frame_principal.pack(expand=True, fill="both")
        
        self.label_imagen = tk.Label(self.frame_principal, image=self.photo)
        self.label_imagen.pack(expand=True, fill="both")
        
        self.btn_registrar_nueva_renta = tk.Button(self.frame_principal, text="Registrar Nueva Renta", command=self.mostrar_interfaz_registro, font=("Arial", 12))
        self.btn_registrar_nueva_renta.pack(side="left", padx=5, pady=5, expand=True, fill="both")

        self.btn_ver_bodegas = tk.Button(self.frame_principal, text="Ver Bodegas Rentadas", command=self.ver_bodegas_rentadas, font=("Arial", 12), bg="lightblue")
        self.btn_ver_bodegas.pack(side="left", padx=5, pady=5, expand=True, fill="both")

    def mostrar_interfaz_registro(self):
        self.controller.show_frame(RegistroVentas)

    def ver_bodegas_rentadas(self):
        self.controller.show_frame(BodegasRentadas)

