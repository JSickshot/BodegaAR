import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from datetime import datetime, timedelta
from PIL import Image, ImageTk

class PuntoDeVentaApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Bodegas AR")
        
        self.image = Image.open("C:/BodegasAR/ar.jpg")
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
                            tarifa REAL
                         )''')
        
        self.c.execute('''SELECT COUNT(*) FROM bodegas''')
        if self.c.fetchone()[0] == 0:
            self.insertar_bodegas()
        
        self.frame_principal = tk.Frame(self.master, padx=20, pady=20)
        self.frame_principal.pack()
        
        self.label_imagen = tk.Label(self.frame_principal, image=self.photo)
        self.label_imagen.pack()
        
        self.btn_registrar_nueva_renta = tk.Button(self.frame_principal, text="Registrar Nueva Renta", command=self.mostrar_interfaz_registro, font=("Arial", 12))
        self.btn_registrar_nueva_renta.pack(side="left", padx=5, pady=5)

        self.btn_ver_bodegas = tk.Button(self.frame_principal, text="Ver Bodegas Rentadas", command=self.ver_bodegas_rentadas, font=("Arial", 12), bg="lightblue")
        self.btn_ver_bodegas.pack(side="left", padx=5, pady=5)

    def insertar_bodegas(self):
        for i in range(1, 21):
            self.c.execute('''INSERT INTO bodegas (numero, ocupada, tarifa) VALUES (?, ?, ?)''', (i, False, 1500))
        self.conn.commit()
    
    def ver_bodegas_rentadas(self):
        bodegas_rentadas = []
        self.c.execute('''SELECT numero, fecha_inicio, fecha_fin, pagado FROM bodegas WHERE ocupada = 1''')
        for bodega in self.c.fetchall():
            bodegas_rentadas.append(f"Bodega {bodega[0]}:\nFecha de inicio: {bodega[1]}\nFecha de fin: {bodega[2]}\nPagado: {'Sí' if bodega[3] else 'No'}\n{'-'*30}")
        
        if not bodegas_rentadas:
            messagebox.showinfo("Bodegas Rentadas", "No hay bodegas rentadas actualmente.")
        else:
            message = "\n\n".join(bodegas_rentadas)
            self.mostrar_ventana_emergente("Bodegas Rentadas", message)
        
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
        self.master.destroy()
        root = tk.Tk()
        app = RegistroRentasApp(root)
        root.mainloop()

    def pagar_renta(self):
        bodega_seleccionada = self.combo_bodegas.get()
        self.c.execute('''UPDATE bodegas SET pagado = 1 WHERE numero = ?''', (bodega_seleccionada,))
        self.conn.commit()
        messagebox.showinfo("Éxito", f"Se ha registrado el pago de la renta de la Bodega {bodega_seleccionada}.")

class RegistroRentasApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Registrar Nueva Renta")
        
        self.conn = sqlite3.connect("bodegas.db")
        self.c = self.conn.cursor()
        
        self.frame_registro = tk.Frame(self.master, padx=20, pady=20)
        self.frame_registro.pack()
        
        self.label_titulo = tk.Label(self.frame_registro, text="Registrar Nueva Renta", font=("Arial", 18, "bold"))
        self.label_titulo.pack()
        
        self.label_subtitulo = tk.Label(self.frame_registro, text="Seleccione una bodega para rentar:", font=("Arial", 12))
        self.label_subtitulo.pack()
        
        self.bodegas_disponibles = self.obtener_bodegas_disponibles()
        self.combo_bodegas = ttk.Combobox(self.frame_registro, values=self.bodegas_disponibles, state="readonly", font=("Arial", 12))
        self.combo_bodegas.pack(side="left", padx=5, pady=5)
        
        self.label_fecha_actual = tk.Label(self.frame_registro, text="Fecha actual:", font=("Arial", 12))
        self.label_fecha_actual.pack(side="left", padx=5, pady=5)
        
        self.entry_fecha_actual = tk.Entry(self.frame_registro, font=("Arial", 12))
        self.entry_fecha_actual.pack(side="left", padx=5, pady=5)
        self.entry_fecha_actual.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        self.btn_rentar = tk.Button(self.frame_registro, text="Rentar", command=self.rentar_bodega, font=("Arial", 12))
        self.btn_rentar.pack(side="left", padx=5, pady=5)
        
        self.btn_regresar = tk.Button(self.frame_registro, text="Regresar", command=self.regresar, font=("Arial", 12))
        self.btn_regresar.pack(side="left", padx=5, pady=5)
        
    def obtener_bodegas_disponibles(self):
        self.c.execute('''SELECT numero FROM bodegas WHERE ocupada = 0''')
        bodegas_libres = self.c.fetchall()
        return [bodega[0] for bodega in bodegas_libres]
    
    def rentar_bodega(self):
        bodega_seleccionada = self.combo_bodegas.get()
        fecha_inicio = self.entry_fecha_actual.get()
        
        if not fecha_inicio:
            messagebox.showerror("Error", "Por favor ingrese la fecha de inicio.")
            return
        
        fecha_fin = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        
        self.c.execute('''UPDATE bodegas SET ocupada = 1, fecha_inicio = ?, fecha_fin = ? WHERE numero = ?''', (fecha_inicio, fecha_fin, bodega_seleccionada))
        self.conn.commit()
        
        self.combo_bodegas["values"] = self.obtener_bodegas_disponibles()  
        messagebox.showinfo("Éxito", f"Bodega {bodega_seleccionada} rentada exitosamente.")
        
    def regresar(self):
        self.master.destroy()
        root = tk.Tk()
        app = PuntoDeVentaApp(root)
        root.mainloop()

def main():
    root = tk.Tk()
    app = PuntoDeVentaApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
