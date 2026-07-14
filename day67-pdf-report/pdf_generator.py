"""
PDF Generator Module
Creates PDF reports using reportlab
"""

import os
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch, cm
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import json


class PDFGenerator:
    """PDF report generator"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        self.elements = []
        self.filename = None
        self.doc = None
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            textColor=colors.HexColor('#2c3e50'),
            alignment=TA_CENTER,
            spaceAfter=30
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#3498db'),
            spaceAfter=12,
            spaceBefore=12
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#333333'),
            spaceAfter=6
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomFooter',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#888888'),
            alignment=TA_CENTER
        ))
    
    def create_report(self, filename: str, title: str, author: str = None):
        """
        Create a new PDF report
        
        Args:
            filename: Output filename
            title: Report title
            author: Report author
        """
        self.filename = filename
        self.elements = []
        
        os.makedirs(os.path.dirname(filename) or '.', exist_ok=True)
        self.doc = SimpleDocTemplate(
            filename,
            pagesize=A4,
            topMargin=2*cm,
            bottomMargin=2*cm,
            leftMargin=2*cm,
            rightMargin=2*cm
        )
        
        self.add_title(title, author)
        self.add_spacer(0.5)
    
    def add_title(self, title: str, author: str = None):
        """Add report title"""
        self.elements.append(Paragraph(title, self.styles['CustomTitle']))
        
        if author:
            self.elements.append(Paragraph(
                f"Author: {author}",
                ParagraphStyle(
                    'Author',
                    parent=self.styles['CustomBody'],
                    alignment=TA_CENTER,
                    fontSize=12
                )
            ))
        
        self.elements.append(Paragraph(
            f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            ParagraphStyle(
                'Date',
                parent=self.styles['CustomBody'],
                alignment=TA_CENTER,
                fontSize=10,
                textColor=colors.HexColor('#888888')
            )
        ))
        
        self.elements.append(Spacer(1, 0.5*inch))
        self.elements.append(Paragraph("="*80, self.styles['CustomBody']))
        self.elements.append(Spacer(1, 0.3*inch))
    
    def add_heading(self, text: str, level: int = 2):
        """Add a heading"""
        if level == 1:
            style = self.styles['Title']
        elif level == 2:
            style = self.styles['CustomHeading']
        else:
            style = self.styles['Heading3']
        
        self.elements.append(Spacer(1, 0.2*inch))
        self.elements.append(Paragraph(text, style))
    
    def add_paragraph(self, text: str):
        """Add a paragraph"""
        self.elements.append(Paragraph(text, self.styles['CustomBody']))
    
    def add_spacer(self, inches: float = 0.2):
        """Add a spacer"""
        self.elements.append(Spacer(1, inches*inch))
    
    def add_table(self, data: list, headers: list = None, col_widths: list = None):
        """
        Add a table to the report
        
        Args:
            data: Table data (list of rows)
            headers: Column headers
            col_widths: Column widths
        """
        table_data = []
        
        if headers:
            table_data.append([Paragraph(h, self.styles['CustomHeading']) for h in headers])
        
        for row in data:
            table_data.append([Paragraph(str(cell), self.styles['CustomBody']) for cell in row])
        
        table = Table(table_data, colWidths=col_widths)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ]))
        
        self.elements.append(table)
        self.elements.append(Spacer(1, 0.2*inch))
    
    def add_bar_chart(self, data: list, categories: list, title: str = None):
        """
        Add a bar chart
        
        Args:
            data: Chart data
            categories: Category labels
            title: Chart title
        """
        drawing = Drawing(400, 200)
        
        chart = VerticalBarChart()
        chart.x = 50
        chart.y = 50
        chart.width = 300
        chart.height = 120
        chart.data = [data]
        chart.categoryAxis.categoryNames = categories
        chart.categoryAxis.labels.boxAnchor = 'ne'
        chart.categoryAxis.labels.dx = 8
        chart.categoryAxis.labels.dy = -2
        chart.categoryAxis.labels.angle = 0
        chart.valueAxis.valueMin = 0
        chart.valueAxis.valueMax = max(data) * 1.2 if data else 10
        chart.bars[0].fillColor = colors.HexColor('#3498db')
        
        drawing.add(chart)
        
        if title:
            self.add_paragraph(f"<b>{title}</b>")
        
        self.elements.append(drawing)
        self.elements.append(Spacer(1, 0.2*inch))
    
    def add_pie_chart(self, data: list, labels: list, title: str = None):
        """
        Add a pie chart
        
        Args:
            data: Chart data
            labels: Slice labels
            title: Chart title
        """
        drawing = Drawing(400, 200)
        
        chart = Pie()
        chart.x = 150
        chart.y = 50
        chart.width = 100
        chart.height = 100
        chart.data = data
        chart.labels = labels
        
        if title:
            self.add_paragraph(f"<b>{title}</b>")
        
        drawing.add(chart)
        self.elements.append(drawing)
        self.elements.append(Spacer(1, 0.2*inch))
    
    def add_footer(self, text: str = None):
        """Add a footer"""
        if text is None:
            text = f"Report generated with Python PDF Generator - {datetime.now().strftime('%Y-%m-%d')}"
        
        self.elements.append(Spacer(1, 0.5*inch))
        self.elements.append(Paragraph("="*80, self.styles['CustomBody']))
        self.elements.append(Paragraph(text, self.styles['CustomFooter']))
    
    def save(self):
        """Save the PDF report"""
        if self.doc:
            self.doc.build(self.elements)
            print(f"[OK] PDF saved to: {self.filename}")
            return True
        return False


def generate_sample_data():
    """Generate sample data for report"""
    sales_data = [
        ['Laptop', 15000, 45, 675000],
        ['Mouse', 200, 120, 24000],
        ['Keyboard', 500, 80, 40000],
        ['Monitor', 3500, 30, 105000],
        ['Printer', 2500, 25, 62500],
        ['Tablet', 8000, 20, 160000],
        ['Phone', 12000, 35, 420000],
        ['Headphones', 300, 60, 18000]
    ]
    return sales_data


def generate_sample_sales_data():
    """Generate sample sales data for charts"""
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    sales = [12000, 15000, 18000, 14000, 20000, 25000]
    return months, sales
