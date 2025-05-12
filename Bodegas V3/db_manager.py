import sqlite3
from datetime import datetime

class DBManager:
    def __init__(self, db_name="bodegas.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def get_client_info(self, bodega_name):
        self.cursor.execute("""
            SELECT r.nombre, r.telefono, r.start_date, r.end_date
            FROM rentas r
            JOIN bodegas b ON r.bodega_id = b.id
            WHERE b.nombre = ? AND r.end_date >= ?
        """, (bodega_name, datetime.today().strftime("%Y-%m-%d")))
        return self.cursor.fetchone()

    def close(self):
        self.conn.close()
