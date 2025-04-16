import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime, timedelta

class POSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bodegas AR - Gestión de Arrendatarios")
        self.root.configure(bg="white")

        
        self.conn = sqlite3.connect("bodegas.db")
        self.cursor = self.conn.cursor()
        self.create_tables()

        # Título
        title = Label(root, text="Registro de Arrendatarios - Bodegas AR", font=("Arial", 16, "bold"), bg="white", fg="black")
        title.pack(pady=10)

        # Frame del formulario
        form_frame = Frame(root, bg="white")
        form_frame.pack(pady=10)

        Label(form_frame, text="Nombre:", bg="white").grid(row=0, column=0, sticky=W, padx=5, pady=5)
        self.name_entry = Entry(form_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        Label(form_frame, text="Teléfono:", bg="white").grid(row=1, column=0, sticky=W, padx=5, pady=5)
        self.phone_entry = Entry(form_frame)
        self.phone_entry.grid(row=1, column=1, padx=5, pady=5)

        Label(form_frame, text="Bodega:", bg="white").grid(row=2, column=0, sticky=W, padx=5, pady=5)
        self.bodega_var = StringVar()
        self.bodega_combo = ttk.Combobox(form_frame, textvariable=self.bodega_var, values=self.get_available_bodegas())
        self.bodega_combo.grid(row=2, column=1, padx=5, pady=5)

        Label(form_frame, text="Fecha de inicio:", bg="white").grid(row=3, column=0, sticky=W, padx=5, pady=5)
        self.start_date_entry = Entry(form_frame)
        self.start_date_entry.grid(row=3, column=1, padx=5, pady=5)

        Label(form_frame, text="Fecha de fin:", bg="white").grid(row=4, column=0, sticky=W, padx=5, pady=5)
        self.end_date_entry = Entry(form_frame)
        self.end_date_entry.grid(row=4, column=1, padx=5, pady=5)

        save_button = Button(form_frame, text="Guardar arrendatario", bg="black", fg="white", command=self.save_rental)
        save_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Visualización de las bodegas
        self.tree = ttk.Treeview(root, columns=("Bodega", "Estado", "Arrendatario", "Fin Contrato"), show="headings")
        self.tree.heading("Bodega", text="Bodega")
        self.tree.heading("Estado", text="Estado")
        self.tree.heading("Arrendatario", text="Arrendatario")
        self.tree.heading("Fin Contrato", text="Vence")
        self.tree.pack(pady=10)

        self.load_bodega_status()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS bodegas (
                id INTEGER PRIMARY KEY,
                nombre TEXT UNIQUE
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS rentas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT,
                telefono TEXT,
                bodega_id INTEGER,
                start_date TEXT,
                end_date TEXT,
                FOREIGN KEY (bodega_id) REFERENCES bodegas(id)
            )
        """)
        self.conn.commit()

        # Bodegas predefinidas
        bodega_names = ["Bodega A1", "Bodega A2", "Bodega A3", "Bodega B1"]
        for name in bodega_names:
            try:
                self.cursor.execute("INSERT INTO bodegas (nombre) VALUES (?)", (name,))
            except sqlite3.IntegrityError:
                continue
        self.conn.commit()

    def get_available_bodegas(self):
        self.cursor.execute("""
            SELECT nombre FROM bodegas 
            WHERE id NOT IN (SELECT bodega_id FROM rentas WHERE end_date >= ?)
        """, (datetime.today().strftime("%Y-%m-%d"),))
        return [row[0] for row in self.cursor.fetchall()]

    def save_rental(self):
        nombre = self.name_entry.get()
        telefono = self.phone_entry.get()
        bodega_nombre = self.bodega_var.get()
        start = self.start_date_entry.get()
        end = self.end_date_entry.get()

        if not all([nombre, telefono, bodega_nombre, start, end]):
            messagebox.showerror("Error", "Por favor completa todos los campos.")
            return

        self.cursor.execute("SELECT id FROM bodegas WHERE nombre=?", (bodega_nombre,))
        bodega_id = self.cursor.fetchone()[0]

        self.cursor.execute("""
            INSERT INTO rentas (nombre, telefono, bodega_id, start_date, end_date)
            VALUES (?, ?, ?, ?, ?)
        """, (nombre, telefono, bodega_id, start, end))
        self.conn.commit()

        self.export_to_pdf(nombre, telefono, bodega_nombre, start, end)
        self.send_notification(nombre, telefono, end)

        messagebox.showinfo("Éxito", "Arrendatario registrado correctamente.")
        self.load_bodega_status()
        self.clear_form()

    def export_to_pdf(self, nombre, telefono, bodega, start, end):
        c = canvas.Canvas(f"contrato_{nombre.replace(' ', '_')}.pdf", pagesize=letter)
        c.drawString(100, 750, f"Contrato de Arrendamiento - Bodegas AR")
        c.drawString(100, 730, f"Nombre: {nombre}")
        c.drawString(100, 710, f"Teléfono: {telefono}")
        c.drawString(100, 690, f"Bodega asignada: {bodega}")
        c.drawString(100, 670, f"Fecha inicio: {start}")
        c.drawString(100, 650, f"Fecha fin: {end}")
        c.save()

    def send_notification(self, nombre, telefono, end_date_str):
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        today = datetime.today()
        diff = (end_date - today).days

        if diff in [30, 15]:
            print(f"ALERTA: El contrato de {nombre} vence en {diff} días.")

            # Aquí podrías integrar Twilio o un servicio de email para enviar notificación real

    def load_bodega_status(self):
        self.tree.delete(*self.tree.get_children())

        self.cursor.execute("SELECT id, nombre FROM bodegas")
        bodegas = self.cursor.fetchall()

        for bodega_id, nombre in bodegas:
            self.cursor.execute("SELECT nombre, end_date FROM rentas WHERE bodega_id=? AND end_date >= ?", (bodega_id, datetime.today().strftime("%Y-%m-%d")))
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

if __name__ == "__main__":
    root = Tk()
    app = POSApp(root)
    root.mainloop()
