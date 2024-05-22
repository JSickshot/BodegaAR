import sqlite3

def crear_base_datos():
    # Conectar a la base de datos (o crearla si no existe)
    conn = sqlite3.connect('bodegas.db')

    # Crear un cursor para ejecutar consultas
    c = conn.cursor()

    # Crear la tabla "bodegas" si no existe
    c.execute('''CREATE TABLE IF NOT EXISTS bodegas (
                    numero INTEGER PRIMARY KEY,
                    ocupada INTEGER,
                    fecha_inicio TEXT,
                    fecha_fin TEXT,
                    nombre TEXT,
                    apellido_paterno TEXT,
                    apellido_materno TEXT
                )''')

    # Guardar los cambios y cerrar la conexión
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # Si ejecutas este script directamente, se creará la base de datos
    crear_base_datos()
