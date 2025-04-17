import re
from unidecode import unidecode
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.units import inch
import os

def format_cpf(cpf):
    """Format CPF to standard format: XXX.XXX.XXX-XX"""
    # Remove non-numeric characters
    cpf = re.sub(r'[^0-9]', '', cpf)
    
    # Apply formatting if CPF has 11 digits
    if len(cpf) == 11:
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    return cpf

def format_cnpj(cnpj):
    """Format CNPJ to standard format: XX.XXX.XXX/XXXX-XX"""
    # Remove non-numeric characters
    cnpj = re.sub(r'[^0-9]', '', cnpj)
    
    # Apply formatting if CNPJ has 14 digits
    if len(cnpj) == 14:
        return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
    return cnpj

def format_telefone(telefone):
    """Format phone number to standard format: (XX) XXXXX-XXXX or (XX) XXXX-XXXX"""
    # Remove non-numeric characters
    telefone = re.sub(r'[^0-9]', '', telefone)
    
    # Apply formatting based on length
    if len(telefone) == 10:  # (XX) XXXX-XXXX
        return f"({telefone[:2]}) {telefone[2:6]}-{telefone[6:]}"
    elif len(telefone) == 11:  # (XX) XXXXX-XXXX
        return f"({telefone[:2]}) {telefone[2:7]}-{telefone[7:]}"
    return telefone

def normalize_string(text):
    """Remove accents and special characters from a string"""
    return unidecode(str(text))

def get_brasil_datetime():
    """
    Retorna o horário atual ajustado para o fuso horário de Brasília (UTC-3)
    
    Returns:
        datetime: Objeto datetime com o horário de Brasília
    """
    return datetime.now() - timedelta(hours=3)

def generate_pdf_report(data, title, headers, filename, date_range=None):
    """
    Generate a PDF report from data
    
    Args:
        data (list): List of data rows
        title (str): Report title
        headers (list): Column headers
        filename (str): Output filename
        date_range (tuple, optional): Start and end date for report period
    
    Returns:
        str: Path to the generated PDF file
    """
    # Create a PDF document
    doc = SimpleDocTemplate(
        filename,
        pagesize=landscape(A4),
        rightMargin=72, leftMargin=72,
        topMargin=72, bottomMargin=18
    )
    
    # Styles for the document
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='ReportTitle',
        parent=styles['Heading1'],
        fontSize=14,
        alignment=TA_CENTER,
        spaceAfter=12
    ))
    
    # Content elements
    elements = []
    
    # Add title
    elements.append(Paragraph(f"<b>{title}</b>", styles['ReportTitle']))
    elements.append(Spacer(1, 0.25 * inch))
    
    # Add date range if provided
    if date_range:
        date_start, date_end = date_range
        date_text = f"Período: {date_start} a {date_end}"
        elements.append(Paragraph(date_text, styles['Normal']))
        elements.append(Spacer(1, 0.25 * inch))
    
    # Generation info
    generation_info = f"Gerado em: {get_brasil_datetime().strftime('%d/%m/%Y %H:%M:%S')}"
    elements.append(Paragraph(generation_info, styles['Normal']))
    elements.append(Spacer(1, 0.25 * inch))
    
    # Create the table with headers and data
    table_data = [headers] + data
    
    table = Table(table_data, repeatRows=1)
    
    # Define cor verde personalizada do VigiAPP
    verde_vigiapp = colors.HexColor('#2f9e41')
    
    # Apply table style
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), verde_vigiapp),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    elements.append(table)
    
    # Build the PDF
    doc.build(elements)
    
    return filename
