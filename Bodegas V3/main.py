
from db_manager import DBManager
from pdf_generator import generar_contrato

def main():
    bodega_consultada = "Bodega A1"

    db = DBManager()
    info = db.get_client_info(bodega_consultada)

    if info:
        nombre, telefono, start, end = info
        pdf_file = generar_contrato(nombre, telefono, bodega_consultada, start, end)
        print(f"Contrato generado exitosamente: {pdf_file}")
    else:
        print(f"No se encontró un arrendatario actual para la bodega: {bodega_consultada}")

    db.close()

if __name__ == "__main__":
    main()
