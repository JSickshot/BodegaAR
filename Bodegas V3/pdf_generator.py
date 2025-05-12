import os
from reportlab.lib.pagesizes import letter, inch
from reportlab.pdfgen import canvas
from datetime import datetime

def generar_contrato(nombre, telefono, domicilio, bodega, fecha_inicio, fecha_fin):
    # Directorio donde se guardarán los contratos
    directorio_contratos = "contratos"

    # Crear la carpeta 'contratos' si no existe
    if not os.path.exists(directorio_contratos):
        os.makedirs(directorio_contratos)

    # Definir el nombre del archivo PDF
    filename = f"{directorio_contratos}/Contrato_{nombre.replace(' ', '_')}.pdf"
    
    # Crear el objeto Canvas
    c = canvas.Canvas(filename, pagesize=letter)
    
    width, height = letter
    margen = 1 * inch  # Ahora 'inch' está definido correctamente
    y = height - margen

    # Título centrado y grande
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, y, "CONTRATO DE ARRENDAMIENTO DE BODEGA")
    y -= 40

    # Subtítulo
    c.setFont("Helvetica", 12)
    c.drawString(margen, y, f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y')}")
    y -= 30

    # Cuerpo del contrato con diseño
    texto = (
        f"En la ciudad de _______, a los {datetime.now().day} días del mes de "
        f"{datetime.now().strftime('%B')} del año {datetime.now().year}, se celebra el presente "
        f"Contrato de Arrendamiento entre:\n\n"
        f"1. ARRENDADOR: Nombre del arrendador (persona física o moral con domicilio en ________).\n\n"
        f"2. ARRENDATARIO: {nombre}, con domicilio en {domicilio} y teléfono {telefono}, quien en lo "
        f"sucesivo se denominará 'EL ARRENDATARIO'.\n\n"
        f"Las partes acuerdan el arrendamiento de la bodega identificada como '{bodega}', desde el "
        f"{fecha_inicio} hasta el {fecha_fin}, conforme a las siguientes cláusulas:\n\n"
        f"PRIMERA.- Objeto del contrato...\n"
        f"SEGUNDA.- Duración del contrato...\n"
        f"TERCERA.- Renta y forma de pago...\n"
        f"... (puedes agregar más cláusulas aquí)\n\n"
        f"Ambas partes aceptan las condiciones del presente contrato, firmando de conformidad."
    )

    text_obj = c.beginText()
    text_obj.setTextOrigin(margen, y)
    text_obj.setFont("Helvetica", 11)
    text_obj.setLeading(18)  # Espaciado entre líneas
    for line in texto.split('\n'):
        text_obj.textLine(line)
    c.drawText(text_obj)

    # Firma
    y -= 180
    c.setFont("Helvetica", 11)
    c.drawString(margen, y, "___________________________")
    c.drawString(margen + 250, y, "___________________________")
    y -= 15
    c.drawString(margen, y, "Firma del Arrendador")
    c.drawString(margen + 250, y, "Firma del Arrendatario")

    # Guardar el archivo PDF
    c.save()

    return filename
