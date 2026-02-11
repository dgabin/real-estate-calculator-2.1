from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO

def generar_pdf(summary, percentages):
    """
    Genera un archivo PDF con el plan de pagos.
    Retorna un objeto BytesIO (el archivo en memoria).
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    normal_style = styles['Normal']
    
    # 1. Título
    elements.append(Paragraph("Plan de Pagos: Propiedad en Construcción", title_style))
    elements.append(Spacer(1, 20))
    
    # 2. Resumen General
    text = f"""
    <b>Precio de la Propiedad:</b> ${summary['property_price']:,.2f}<br/>
    <b>Meses de Construcción:</b> {summary['number_of_months']}<br/>
    """
    elements.append(Paragraph(text, normal_style))
    elements.append(Spacer(1, 20))

    # 3. Datos para la Tabla
    data = [
        ["Concepto", "Monto", "Detalle"], # Encabezado
        ["Separación", f"${summary['separation_paid']:,.2f}", "Pago Inmediato"],
        ["Inicial a la Firma", f"${summary['due_at_signing']:,.2f}", f"Completar el {percentages['initial_target']}%"],
        ["Cuotas Mensuales", f"${summary['monthly_payment']:,.2f}", "Durante la construcción"],
        ["Pago Final", f"${summary['final_payment']:,.2f}", "Contra Entrega / Financiamiento"]
    ]

    # 4. Crear Tabla
    t = Table(data, colWidths=[200, 150, 200])
    
    # Estilo de la Tabla
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(t)
    elements.append(Spacer(1, 40))

    # 5. Pie de página
    footer_text = "Generado por Calculadora Inmobiliaria. Precios sujetos a cambios."
    elements.append(Paragraph(footer_text, styles['Italic']))

    # Construir PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer
