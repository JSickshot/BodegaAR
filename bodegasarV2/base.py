import sqlite3

conn = sqlite3.connect('pos.db')
cursor = conn.cursor()

# Crear tabla de bodegas
cursor.execute('''
CREATE TABLE IF NOT EXISTS bodegas (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    size REAL NOT NULL,
    location TEXT NOT NULL,
    status TEXT NOT NULL
)
''')

# Crear tabla de rentas
cursor.execute('''
CREATE TABLE IF NOT EXISTS rentas (
    id INTEGER PRIMARY KEY,
    bodega_id INTEGER NOT NULL,
    renter_name TEXT NOT NULL,
    rent_start_date TEXT NOT NULL,
    rent_end_date TEXT NOT NULL,
    FOREIGN KEY (bodega_id) REFERENCES bodegas(id)
)
''')

conn.commit()
conn.close()
