import tkinter as tk
from tkinter import messagebox, Toplevel, Scrollbar, Listbox, OptionMenu, StringVar
import sqlite3
from datetime import datetime


class POSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bodegas AR")
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        self.conn = sqlite3.connect('pos.db')
        self.cursor = self.conn.cursor()
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.config(bg="white")
        self.container = tk.Frame(root, bg="white")
        self.container.pack(expand=True, fill="both")

        self.create_tables()
        self.update_bodega_status()

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)

        bodega_frame = tk.Frame(self.container)
        bodega_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.name_label = tk.Label(bodega_frame, text="Nombre de la bodega", font=("Arial", 20), justify="center")
        self.name_label.grid(row=0, column=0, padx=10, pady=5)

        self.name_entry = tk.Entry(bodega_frame)
        self.name_entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        self.size_label = tk.Label(bodega_frame, text="Tamaño", justify="center")
        self.size_label.grid(row=2, column=0, padx=10, pady=5)

        self.size_entry = tk.Entry(bodega_frame)
        self.size_entry.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

        self.location_label = tk.Label(bodega_frame, text="Ubicación", justify="center")
        self.location_label.grid(row=4, column=0, padx=10, pady=5)

        self.location_entry = tk.Entry(bodega_frame)
        self.location_entry.grid(row=5, column=0, padx=10, pady=5, sticky="ew")

        self.add_bodega_button = tk.Button(bodega_frame, text="Añadir Bodega", command=self.add_bodega)
        self.add_bodega_button.grid(row=6, column=0, padx=10, pady=10, sticky="ew")

        # Rental frame
        rental_frame = tk.Frame(self.container)
        rental_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.renter_name_label = tk.Label(rental_frame, text="Nombre del arrendatario", justify="center")
        self.renter_name_label.grid(row=0, column=0, padx=10, pady=5)

        self.renter_name_entry = tk.Entry(rental_frame)
        self.renter_name_entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        self.bodega_id_label = tk.Label(rental_frame, text="Bodega a rentar", justify="center")
        self.bodega_id_label.grid(row=2, column=0, padx=10, pady=5)

        self.bodega_id_var = StringVar(rental_frame)
        self.bodega_id_option_menu = OptionMenu(rental_frame, self.bodega_id_var, *self.get_available_bodegas())
        self.bodega_id_option_menu.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

        self.start_date_label = tk.Label(rental_frame, text="Fecha de inicio (YYYY-MM-DD)", justify="center")
        self.start_date_label.grid(row=4, column=0, padx=10, pady=5)

        self.start_date_entry = tk.Entry(rental_frame)
        self.start_date_entry.grid(row=5, column=0, padx=10, pady=5, sticky="ew")

        self.end_date_label = tk.Label(rental_frame, text="Fecha de fin (YYYY-MM-DD)", justify="center")
        self.end_date_label.grid(row=6, column=0, padx=10, pady=5)

        self.end_date_entry = tk.Entry(rental_frame)
        self.end_date_entry.grid(row=7, column=0, padx=10, pady=5, sticky="ew")

        self.add_rental_button = tk.Button(rental_frame, text="Registrar Renta", command=self.add_rental)
        self.add_rental_button.grid(row=8, column=0, padx=10, pady=10, sticky="ew")

        # Other buttons
        self.view_available_button = tk.Button(self.container, text="Ver Bodegas Disponibles", command=self.view_available_bodegas)
        self.view_available_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.view_occupied_button = tk.Button(self.container, text="Ver Bodegas Ocupadas", command=self.view_occupied_bodegas)
        self.view_occupied_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.view_total_button = tk.Button(self.container, text="Ver Total de Bodegas", command=self.view_total_bodegas)
        self.view_total_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.view_rented_bodega_button = tk.Button(self.container, text="Ver Detalles", command=self.view_rented_bodega_details)
        self.view_rented_bodega_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        self.edit_rented_bodega_button = tk.Button(self.container, text="Editar Detalles", command=self.edit_rented_bodega_details)
        self.edit_rented_bodega_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        self.end_rental_contract_button = tk.Button(self.container, text="Finalizar Contrato", command=self.end_rental_contract)
        self.end_rental_contract_button.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        self.bodegas_list = tk.Listbox(self.container, width=80)
        self.bodegas_list.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.add_rental_with_list_button = tk.Button(self.container, text="Añadir Renta desde Lista", command=self.show_bodegas_window)
        self.add_rental_with_list_button.grid(row=7, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

    def view_rented_bodega_details(self):
        selected_bodega = self.bodegas_list.get(tk.ACTIVE)
        bodega_id = selected_bodega.split("ID: ")[1].split(",")[0]
        self.cursor.execute('SELECT * FROM bodegas WHERE id = ?', (bodega_id,))
        bodega_details = self.cursor.fetchone()
        messagebox.showinfo("Detalles de la Bodega", f"Nombre: {bodega_details[1]}\nTamaño: {bodega_details[2]}\nUbicación: {bodega_details[3]}\nEstado: {bodega_details[4]}")

    def edit_rented_bodega_details(self):
        pass

    def end_rental_contract(self):
        selected_bodega = self.bodegas_list.get(tk.ACTIVE)
        bodega_id = selected_bodega.split("ID: ")[1].split(",")[0]
        self.cursor.execute('DELETE FROM rentas WHERE bodega_id = ?', (bodega_id,))
        self.cursor.execute('UPDATE bodegas SET status = "disponible" WHERE id = ?', (bodega_id,))
        self.conn.commit()
        messagebox.showinfo("Contrato Finalizado", "El contrato de alquiler ha sido finalizado correctamente")
        self.update_bodega_status()
        self.update_bodega_options()

    def minimize_window(self):
        self.root.geometry("")

    def create_tables(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS bodegas (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            size REAL NOT NULL,
            location TEXT NOT NULL,
            status TEXT NOT NULL
        )
        ''')
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS rentas (
            id INTEGER PRIMARY KEY,
            bodega_id INTEGER NOT NULL,
            renter_name TEXT NOT NULL,
            rent_start_date TEXT NOT NULL,
            rent_end_date TEXT NOT NULL,
            FOREIGN KEY (bodega_id) REFERENCES bodegas(id)
        )
        ''')
        self.conn.commit()

    def update_bodega_status(self):
        current_date = datetime.now().date()
        self.cursor.execute('''
        SELECT bodega_id FROM rentas WHERE rent_end_date < ?
        ''', (current_date,))
        bodegas_to_release = self.cursor.fetchall()
        for bodega in bodegas_to_release:
            self.cursor.execute('''
            UPDATE bodegas SET status = 'disponible' WHERE id = ?
            ''', (bodega[0],))
        self.conn.commit()

    def update_bodega_options(self):
        available_bodegas = self.get_available_bodegas()
        menu = self.bodega_id_option_menu["menu"]
        menu.delete(0, "end")
        for bodega_id in available_bodegas:
            menu.add_command(label=bodega_id, command=lambda value=bodega_id: self.bodega_id_var.set(value))

    def get_available_bodegas(self):
        self.cursor.execute('SELECT id FROM bodegas WHERE status = "disponible"')
        return [str(row[0]) for row in self.cursor.fetchall()]

    def add_bodega(self):
        name = self.name_entry.get()
        size = self.size_entry.get()
        location = self.location_entry.get()

        if name and size and location:
            self.cursor.execute('''
                INSERT INTO bodegas (name, size, location, status) VALUES (?, ?, ?, ?)
            ''', (name, float(size), location, 'disponible'))
            self.conn.commit()
            messagebox.showinfo("Éxito", "Bodega añadida correctamente")
            self.name_entry.delete(0, tk.END)
            self.size_entry.delete(0, tk.END)
            self.location_entry.delete(0, tk.END)
            self.update_bodega_status()
            self.update_bodega_options()
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")

    def add_rental(self):
        renter_name = self.renter_name_entry.get()
        bodega_id = self.bodega_id_var.get()
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()

        if renter_name and bodega_id and start_date and end_date:
            try:
                datetime.strptime(start_date, "%Y-%m-%d")
                datetime.strptime(end_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha incorrecto. Debe ser YYYY-MM-DD")
                return

            self.cursor.execute('''
                INSERT INTO rentas (bodega_id, renter_name, rent_start_date, rent_end_date) VALUES (?, ?, ?, ?)
            ''', (int(bodega_id), renter_name, start_date, end_date))
            self.conn.commit()
            self.cursor.execute('''
                UPDATE bodegas SET status = 'ocupada' WHERE id = ?
            ''', (int(bodega_id),))
            self.conn.commit()
            messagebox.showinfo("Éxito", "Renta registrada correctamente")
            self.renter_name_entry.delete(0, tk.END)
            self.bodega_id_var.set('')
            self.start_date_entry.delete(0, tk.END)
            self.end_date_entry.delete(0, tk.END)
            self.update_bodega_status()
            self.bodega_id_option_menu['menu'].delete(0, 'end')
            for bodega_id in self.get_available_bodegas():
                self.bodega_id_option_menu['menu'].add_command(label=bodega_id, command=tk._setit(self.bodega_id_var, bodega_id))
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")

    def view_available_bodegas(self):
        self.bodegas_list.delete(0, tk.END)
        self.cursor.execute('SELECT * FROM bodegas WHERE status = "disponible"')
        for row in self.cursor.fetchall():
            self.bodegas_list.insert(tk.END, f"ID: {row[0]}, Nombre: {row[1]}, Tamaño: {row[2]}, Ubicación: {row[3]}, Estado: {row[4]}")

    def view_occupied_bodegas(self):
        self.bodegas_list.delete(0, tk.END)
        self.cursor.execute('SELECT * FROM bodegas WHERE status = "ocupada"')
        for row in self.cursor.fetchall():
            self.bodegas_list.insert(tk.END, f"ID: {row[0]}, Nombre: {row[1]}, Tamaño: {row[2]}, Ubicación: {row[3]}, Estado: {row[4]}")

    def view_total_bodegas(self):
        self.bodegas_list.delete(0, tk.END)
        self.cursor.execute('''
        SELECT bodegas.id, bodegas.name, bodegas.size, bodegas.location, bodegas.status, rentas.rent_end_date, rentas.renter_name 
        FROM bodegas 
        LEFT JOIN rentas 
        ON bodegas.id = rentas.bodega_id
        ''')
        bodegas_info = self.cursor.fetchall()
        for row in bodegas_info:
            if row[4] == 'ocupada':
                end_date = row[5]
                if end_date:
                    remaining_days = (datetime.strptime(end_date, "%Y-%m-%d") - datetime.now()).days
                    self.bodegas_list.insert(tk.END, f"ID: {row[0]}, Nombre: {row[1]}, Tamaño: {row[2]}, Ubicación: {row[3]}, Estado: {row[4]}, Arrendatario: {row[6]}, Días restantes de renta: {remaining_days}")
                else:
                    self.bodegas_list.insert(tk.END, f"ID: {row[0]}, Nombre: {row[1]}, Tamaño: {row[2]}, Ubicación: {row[3]}, Estado: {row[4]}, Arrendatario: {row[6]}")
            else:
                self.bodegas_list.insert(tk.END, f"ID: {row[0]}, Nombre: {row[1]}, Tamaño: {row[2]}, Ubicación: {row[3]}, Estado: {row[4]}")

   


    def show_bodegas_window(self):
        available_window = Toplevel(self.root)
        available_window.title("Bodegas Disponibles")
        available_window.geometry("400x400")
        scrollbar = Scrollbar(available_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = Listbox(available_window, yscrollcommand=scrollbar.set)
        listbox.pack(expand=True, fill="both")

        self.cursor.execute('SELECT * FROM bodegas WHERE status = "disponible"')
        for row in self.cursor.fetchall():
            listbox.insert(tk.END, f"ID: {row[0]}, Nombre: {row[1]}, Tamaño: {row[2]}, Ubicación: {row[3]}, Estado: {row[4]}")

        scrollbar.config(command=listbox.yview)


if __name__ == "__main__":
    root = tk.Tk()
    app = POSApp(root)
    root.mainloop()
