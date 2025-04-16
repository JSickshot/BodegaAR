import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from InicioApp import InicioApp
from registroventas import RegistroVentas
from bodegasrentadas import BodegasRentadas


class FullscreenApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        for F in (InicioApp, RegistroVentas, BodegasRentadas):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(InicioApp)
    
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

if __name__ == "__main__":
    app = FullscreenApp()
    app.mainloop()
