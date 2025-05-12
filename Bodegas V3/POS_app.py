import sqlite3
import os
import platform
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
from pdf_generator import generar_contrato  # Asegúrate de que el archivo pdf_generator.py esté correctamente implementado

class POSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bodegas AR")
        self.root.configure(bg="white")

        self.last_contract_file = None  # Ruta al último contrato generado

        self.conn = sqlite3.connect("bodegas1.db")
        self.cursor = self.conn.cursor()
        self.create_tables()

        title = Label(root, text="Registro de Arrendatarios - Bodegas AR", font=("Arial", 16, "bold"), bg="white", fg="black")
        title.pack(pady=10)

        form_frame = Frame(root, bg="white")
        form_frame.pack(pady=10)

        Label(form_frame, text="Nombre:", bg="white").grid(row=0, column=0, sticky=W, padx=5, pady=5)
        self.name_entry = Entry(form_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        Label(form_frame, text="Domicilio:", bg="white").grid(row=2, column=0, sticky=W, padx=5, pady=5)
        self.address_entry = Entry(form_frame)
        self.address_entry.grid(row=2, column=1, padx=5, pady=5)

        Label(form_frame, text="Teléfono:", bg="white").grid(row=1, column=0, sticky=W, padx=5, pady=5)
        self.phone_entry = Entry(form_frame)
        self.phone_entry.grid(row=1, column=1, padx=5, pady=5)

        Label(form_frame, text="Bodega:", bg="white").grid(row=3, column=0, sticky=W, padx=5, pady=5)
        self.bodega_var = StringVar()
        self.bodega_combo = ttk.Combobox(form_frame, textvariable=self.bodega_var, values=self.get_available_bodegas())
        self.bodega_combo.grid(row=3, column=1, padx=5, pady=5)

        Label(form_frame, text="Fecha de inicio (YYYY-MM-DD):", bg="white").grid(row=4, column=0, sticky=W, padx=5, pady=5)
        self.start_date_entry = Entry(form_frame)
        self.start_date_entry.grid(row=4, column=1, padx=5, pady=5)

        Label(form_frame, text="Fecha de fin (YYYY-MM-DD):", bg="white").grid(row=5, column=0, sticky=W, padx=5, pady=5)
        self.end_date_entry = Entry(form_frame)
        self.end_date_entry.grid(row=5, column=1, padx=5, pady=5)

        save_button = Button(form_frame, text="Guardar arrendatario", bg="black", fg="white", command=self.save_rental)
        save_button.grid(row=6, column=0, columnspan=2, pady=10)

        print_button = Button(root, text="Imprimir último contrato", bg="gray", fg="white", command=self.imprimir_ultimo_contrato)
        print_button.pack(pady=5)

        self.tree = ttk.Treeview(root, columns=("Bodega", "Estado", "Arrendatario", "Fin Contrato"), show="headings")
        self.tree.heading("Bodega", text="Bodega")
        self.tree.heading("Estado", text="Estado")
        self.tree.heading("Arrendatario", text="Arrendatario")
        self.tree.heading("Fin Contrato", text="Vence")
        self.tree.pack(pady=10)

        self.load_bodega_status()

    def create_tables(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS bodegas (
            id INTEGER PRIMARY KEY,
            nombre TEXT UNIQUE
        )""")
        
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS rentas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            telefono TEXT,
            domicilio TEXT,
            bodega_id INTEGER,
            start_date TEXT,
            end_date TEXT,
            FOREIGN KEY (bodega_id) REFERENCES bodegas(id)
        )""")
        self.conn.commit()

        
        bodega_names = ["Bodega A1", "Bodega A2", "Bodega B1", "Bodega B2", "Bodegas C1", "Bodegas C2", "Bodegas D1", "Bodegas D2", "Bodegas E1", "Bodegas E2", "Bodegas F1", "Bodegas F"]
        for name in bodega_names:
            try:
                self.cursor.execute("INSERT INTO bodegas (nombre) VALUES (?)", (name,))
            except sqlite3.IntegrityError:
                continue
        self.conn.commit()

    def get_available_bodegas(self):
        self.cursor.execute("""SELECT nombre FROM bodegas 
                               WHERE id NOT IN (SELECT bodega_id FROM rentas WHERE end_date >= ?)""", (datetime.today().strftime("%Y-%m-%d"),))
        return [row[0] for row in self.cursor.fetchall()]

    def save_rental(self):
        nombre = self.name_entry.get()
        telefono = self.phone_entry.get()
        domicilio = self.address_entry.get()
        bodega_nombre = self.bodega_var.get()
        start = self.start_date_entry.get()
        end = self.end_date_entry.get()

        if not all([nombre, telefono, domicilio, bodega_nombre, start, end]):
            messagebox.showerror("Error", "Por favor completa todos los campos.")
            return

        try:
            start_date = datetime.strptime(start, "%Y-%m-%d")
            end_date = datetime.strptime(end, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error de fecha", "Por favor ingrese las fechas en el formato correcto (YYYY-MM-DD).")
            return

        self.cursor.execute("SELECT id FROM bodegas WHERE nombre=?", (bodega_nombre,))
        bodega_id_row = self.cursor.fetchone()
        if not bodega_id_row:
            messagebox.showerror("Error", "La bodega seleccionada no existe.")
            return

        bodega_id = bodega_id_row[0]

        self.cursor.execute("""INSERT INTO rentas (nombre, telefono, domicilio, bodega_id, start_date, end_date)
                               VALUES (?, ?, ?, ?, ?, ?)""", (nombre, telefono, domicilio, bodega_id, start, end))
        self.conn.commit()

        # Crear la carpeta 'contratos' si no existe
        if not os.path.exists('contratos'):
            os.makedirs('contratos')


        filename = generar_contrato(nombre, telefono, domicilio, bodega_nombre, start, end)
        self.last_contract_file = filename

        self.abrir_pdf(filename)

        messagebox.showinfo("Éxito", "Arrendatario guardado y contrato generado.")
        self.load_bodega_status()
        self.clear_form()

    def abrir_pdf(self, filename):
        try:
            if platform.system() == "Windows":
                os.startfile(filename)
            elif platform.system() == "Darwin":
                os.system(f"open '{filename}'")
            else:  # Linux
                os.system(f"xdg-open '{filename}'")
        except Exception as e:
            messagebox.showerror("Error al abrir el PDF", str(e))

    def imprimir_pdf(self, filename):
        try:
            if platform.system() == "Windows":
                os.startfile(filename, "print")
            elif platform.system() == "Darwin":
                os.system(f"lp '{filename}'")
            else:
                os.system(f"lpr '{filename}'")
            messagebox.showinfo("Impresión enviada", "Contrato enviado a la impresora.")
        except Exception as e:
            messagebox.showerror("Error al imprimir", str(e))

    def imprimir_ultimo_contrato(self):
        if self.last_contract_file and os.path.exists(self.last_contract_file):
            self.imprimir_pdf(self.last_contract_file)
        else:
            messagebox.showwarning("Sin contrato", "No hay contrato reciente para imprimir.")

    def load_bodega_status(self):
        self.tree.delete(*self.tree.get_children())

        self.cursor.execute("SELECT id, nombre FROM bodegas")
        bodegas = self.cursor.fetchall()

        for bodega_id, nombre in bodegas:
            self.cursor.execute("""SELECT nombre, end_date FROM rentas WHERE bodega_id=? AND end_date >= ?""", (bodega_id, datetime.today().strftime("%Y-%m-%d")))
            renta = self.cursor.fetchone()
            if renta:
                estado = "Ocupada"
                arrendatario = renta[0]
                fin = renta[1]
            else:
                estado = "Disponible"
                arrendatario = "-"
                fin = "-"
            self.tree.insert("", "end", values=(nombre, estado, arrendatario, fin))

    def clear_form(self):
        self.name_entry.delete(0, END)
        self.phone_entry.delete(0, END)
        self.start_date_entry.delete(0, END)
        self.end_date_entry.delete(0, END)
        self.bodega_combo["values"] = self.get_available_bodegas()
        self.bodega_var.set("")

if __name__ == "__main__":
    root = Tk()
    app = POSApp(root)
    root.mainloop()
