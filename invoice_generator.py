import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def build_pdf_invoice(invoice_details, items, filepath):
    doc = SimpleDocTemplate(filepath, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=20, textColor=colors.HexColor("#1A365D"))
    elements.append(Paragraph("INVOICE", title_style))
    elements.append(Spacer(1, 12))

    meta_text = f"""
    <b>Invoice Number:</b> {invoice_details['invoice_number']}<br/>
    <b>Date:</b> {invoice_details['invoice_date']}<br/>
    <b>Customer ID:</b> {invoice_details['customer_id']}<br/>
    <b>Customer Name:</b> {invoice_details['customer_name']}
    """
    elements.append(Paragraph(meta_text, styles['Normal']))
    elements.append(Spacer(1, 18))

    table_data = [["Description", "Qty", "Unit Price ($)", "Total ($)"]]
    for item in items:
        table_data.append([
            item['description'],
            str(item['quantity']),
            f"{item['unit_price']:.2f}",
            f"{item['line_total']:.2f}"
        ])

    table_data.append(["", "", "Subtotal:", f"{invoice_details['subtotal']:.2f}"])
    table_data.append(["", "", "Tax (10%):", f"{invoice_details['tax_amount']:.2f}"])
    table_data.append(["", "", "Total Due:", f"{invoice_details['total_amount']:.2f}"])

    item_table = Table(table_data, colWidths=[240, 50, 100, 100])
    item_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2B6CB0")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -4), 0.5, colors.lightgrey),
        ('FONTNAME', (2, -3), (-1, -1), 'Helvetica-Bold'),
    ]))

    elements.append(item_table)
    doc.build(elements)
    print(f"Generated PDF saved to: {filepath}")