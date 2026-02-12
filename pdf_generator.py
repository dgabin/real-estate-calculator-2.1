from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

def generar_pdf(summary, percentages, mortgage):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    heading_style = styles['Heading2']
    normal_style = styles['Normal']
    
    # Título
    elements.append(Paragraph("Análisis de Inversión Inmobiliaria", title_style))
    elements.append(Spacer(1, 10))
    
    elements.append(Paragraph(f"<b>Precio Propiedad:</b> ${summary['property_price']:,.2f}", normal_style))
    elements.append(Spacer(1, 20))

    # --- TABLA 1: CONSTRUCCIÓN ---
    elements.append(Paragraph("Fase 1: Plan de Pagos (Construcción)", heading_style))
    data_con = [
        ["Concepto", "Monto", "Nota"],
        ["Separación", f"${summary['separation_paid']:,.2f}", "Pagado"],
        ["Firma Contrato", f"${summary['due_at_signing']:,.2f}", f"Completar {percentages['initial_target']}%"],
        ["Cuotas Mensuales", f"${summary['monthly_payment']:,.2f}", f"Por {summary['number_of_months']} meses"],
        ["A Financiar", f"${summary['final_payment']:,.2f}", "Contra Entrega"]
    ]
    
    t1 = Table(data_con, colWidths=[180, 150, 180])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.aliceblue),
    ]))
    elements.append(t1)
    elements.append(Spacer(1, 20))

    # --- TABLA 2: FINANCIAMIENTO ---
    elements.append(Paragraph("Fase 2: Estimado Hipotecario (Banco)", heading_style))
    
    data_bank = [
        ["Concepto", "Valor", "Detalle"],
        ["Monto Préstamo", f"${mortgage['loan_amount']:,.2f}", f"A {mortgage['years']} Años"],
        ["Tasa Interés", f"{mortgage['rate']}%", "Anual Estimada"],
        ["Cuota (Capital+Interés)", f"${mortgage['monthly_principal_interest']:,.2f}", "Sin Seguros"],
        ["Seguros (Vida/Incendio)", f"${mortgage['monthly_insurance']:,.2f}", "Estimado Mensual"],
        ["CUOTA TOTAL", f"${mortgage['monthly_total']:,.2f}", "Pago Mensual Banco"]
    ]

    t2 = Table(data_bank, colWidths=[180, 150, 180])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'), # Negrita para el total
        ('BACKGROUND', (0, 1), (-1, -1), colors.honeydew),
    ]))
    elements.append(t2)
    
    elements.append(Spacer(1, 30))
    elements.append(Paragraph("Nota: Los valores de seguros y tasas bancarias son estimados y pueden variar.", styles['Italic']))

    doc.build(elements)
    buffer.seek(0)
    return buffer
