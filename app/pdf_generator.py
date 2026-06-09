from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_LEFT
from reportlab.lib import colors
from datetime import datetime
import io

class InvoicePDFGenerator:
    def __init__(self, company_info):
        self.company_info = company_info
        self.styles = getSampleStyleSheet()
        self.setup_styles()
    
    def setup_styles(self):
        """Setup custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='CompanyName',
            parent=self.styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=6,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='InvoiceTitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#333333'),
            spaceAfter=12
        ))
        
        self.styles.add(ParagraphStyle(
            name='ItemLabel',
            fontSize=9,
            textColor=colors.HexColor('#666666'),
            spaceAfter=3
        ))
    
    def generate_invoice_pdf(self, invoice, filename=None):
        """Generate PDF for invoice"""
        if filename is None:
            filename = f"Invoice_{invoice.invoice_number}.pdf"
        
        doc = SimpleDocTemplate(
            filename,
            pagesize=A4,
            rightMargin=0.5*inch,
            leftMargin=0.5*inch,
            topMargin=0.5*inch,
            bottomMargin=0.5*inch
        )
        
        story = []
        
        # Header
        story.append(Paragraph(self.company_info['name'], self.styles['CompanyName']))
        story.append(Spacer(1, 0.1*inch))
        
        # Company Info
        company_details = f"""
        {self.company_info['address']}<br/>
        Phone: {self.company_info['phone']} | Email: {self.company_info['email']}<br/>
        GST: {self.company_info['gst']}
        """
        story.append(Paragraph(company_details, self.styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        # Invoice Title
        story.append(Paragraph(f"INVOICE #{invoice.invoice_number}", self.styles['InvoiceTitle']))
        story.append(Spacer(1, 0.1*inch))
        
        # Invoice Details
        details_data = [
            ['Invoice Date:', invoice.invoice_date.strftime('%d-%m-%Y'), 'Due Date:', invoice.due_date.strftime('%d-%m-%Y') if invoice.due_date else 'N/A'],
            ['Customer:', invoice.customer_name, 'Payment Method:', invoice.payment_method.upper()]
        ]
        
        details_table = Table(details_data, colWidths=[1.5*inch, 2*inch, 1.5*inch, 2*inch])
        details_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#666666')),
            ('TEXTCOLOR', (2, 0), (2, -1), colors.HexColor('#666666')),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('ALIGN', (3, 0), (3, -1), 'LEFT'),
        ]))
        story.append(details_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Items Table
        items_data = [['S.No', 'Product', 'Qty', 'Unit Price', 'Discount', 'Total']]
        
        for idx, item in enumerate(invoice.items, 1):
            items_data.append([
                str(idx),
                item.product_name,
                str(item.quantity),
                f"₹{item.unit_price:.2f}",
                f"₹{item.discount_amount:.2f}",
                f"₹{item.total_amount:.2f}"
            ])
        
        items_table = Table(items_data, colWidths=[0.5*inch, 3*inch, 0.8*inch, 1*inch, 1*inch, 1.2*inch])
        items_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')])
        ]))
        story.append(items_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Totals
        totals_data = [
            ['', '', 'Subtotal:', f"₹{invoice.subtotal:.2f}"],
            ['', '', f'Tax ({invoice.tax_percent}%):', f"₹{invoice.tax_amount:.2f}"],
            ['', '', 'Discount:', f"₹{invoice.discount_amount:.2f}"],
            ['', '', 'TOTAL AMOUNT:', f"₹{invoice.total_amount:.2f}"]
        ]
        
        totals_table = Table(totals_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        totals_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (2, -1), 'Helvetica'),
            ('FONTNAME', (3, 0), (3, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -2), 9),
            ('FONTSIZE', (0, -1), (-1, -1), 11),
            ('TEXTCOLOR', (0, -1), (-1, -1), colors.HexColor('#667eea')),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#f0f0f0')),
            ('GRID', (2, 0), (-1, -1), 1, colors.grey),
            ('BOTTOMPADDING', (0, -1), (-1, -1), 12),
            ('TOPPADDING', (0, -1), (-1, -1), 12)
        ]))
        story.append(totals_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Notes
        if invoice.notes:
            story.append(Paragraph("<b>Notes:</b>", self.styles['Normal']))
            story.append(Paragraph(invoice.notes, self.styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
        
        # Footer
        footer_text = f"<br/><br/>Generated on {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
        story.append(Spacer(1, 0.3*inch))
        story.append(Paragraph(footer_text, self.styles['Normal']))
        
        # Build PDF
        doc.build(story)
        return filename
    
    def generate_quotation_pdf(self, quotation, filename=None):
        """Generate PDF for quotation"""
        if filename is None:
            filename = f"Quotation_{quotation.quotation_number}.pdf"
        
        doc = SimpleDocTemplate(
            filename,
            pagesize=A4,
            rightMargin=0.5*inch,
            leftMargin=0.5*inch,
            topMargin=0.5*inch,
            bottomMargin=0.5*inch
        )
        
        story = []
        
        # Header
        story.append(Paragraph(self.company_info['name'], self.styles['CompanyName']))
        story.append(Spacer(1, 0.1*inch))
        
        # Company Info
        company_details = f"""
        {self.company_info['address']}<br/>
        Phone: {self.company_info['phone']} | Email: {self.company_info['email']}
        """
        story.append(Paragraph(company_details, self.styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        # Quotation Title
        story.append(Paragraph(f"QUOTATION #{quotation.quotation_number}", self.styles['InvoiceTitle']))
        story.append(Spacer(1, 0.1*inch))
        
        # Quotation Details
        details_data = [
            ['Quotation Date:', quotation.quotation_date.strftime('%d-%m-%Y'), 'Valid Until:', quotation.valid_until.strftime('%d-%m-%Y')],
            ['Customer:', quotation.customer_name, 'Status:', quotation.status.upper()]
        ]
        
        details_table = Table(details_data, colWidths=[1.5*inch, 2*inch, 1.5*inch, 2*inch])
        details_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#666666')),
            ('TEXTCOLOR', (2, 0), (2, -1), colors.HexColor('#666666')),
        ]))
        story.append(details_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Items Table
        items_data = [['S.No', 'Product', 'Qty', 'Unit Price', 'Total']]
        
        for idx, item in enumerate(quotation.items, 1):
            items_data.append([
                str(idx),
                item.product_name,
                str(item.quantity),
                f"₹{item.unit_price:.2f}",
                f"₹{item.quantity * item.unit_price:.2f}"
            ])
        
        items_table = Table(items_data, colWidths=[0.5*inch, 3.2*inch, 0.8*inch, 1*inch, 1.5*inch])
        items_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')])
        ]))
        story.append(items_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Totals
        totals_data = [
            ['', '', 'Subtotal:', f"₹{quotation.subtotal:.2f}"],
            ['', '', f'Tax ({quotation.tax_percent}%):', f"₹{quotation.tax_amount:.2f}"],
            ['', '', 'Discount:', f"₹{quotation.discount_amount:.2f}"],
            ['', '', 'TOTAL AMOUNT:', f"₹{quotation.total_amount:.2f}"]
        ]
        
        totals_table = Table(totals_data, colWidths=[2.2*inch, 1.3*inch, 1.5*inch, 1.5*inch])
        totals_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (2, -1), 'Helvetica'),
            ('FONTNAME', (3, 0), (3, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -2), 9),
            ('FONTSIZE', (0, -1), (-1, -1), 11),
            ('TEXTCOLOR', (0, -1), (-1, -1), colors.HexColor('#667eea')),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#f0f0f0')),
            ('GRID', (2, 0), (-1, -1), 1, colors.grey),
            ('BOTTOMPADDING', (0, -1), (-1, -1), 12),
            ('TOPPADDING', (0, -1), (-1, -1), 12)
        ]))
        story.append(totals_table)
        
        if quotation.notes:
            story.append(Spacer(1, 0.3*inch))
            story.append(Paragraph("<b>Notes:</b>", self.styles['Normal']))
            story.append(Paragraph(quotation.notes, self.styles['Normal']))
        
        story.append(Spacer(1, 0.3*inch))
        footer_text = f"<br/><br/>Generated on {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
        story.append(Paragraph(footer_text, self.styles['Normal']))
        
        doc.build(story)
        return filename
    
    def generate_purchase_order_pdf(self, purchase_order, filename=None):
        """Generate PDF for purchase order"""
        if filename is None:
            filename = f"PurchaseOrder_{purchase_order.po_number}.pdf"
        
        doc = SimpleDocTemplate(
            filename,
            pagesize=A4,
            rightMargin=0.5*inch,
            leftMargin=0.5*inch,
            topMargin=0.5*inch,
            bottomMargin=0.5*inch
        )
        
        story = []
        
        # Header
        story.append(Paragraph(self.company_info['name'], self.styles['CompanyName']))
        story.append(Spacer(1, 0.1*inch))
        
        # Company Info
        company_details = f"""
        {self.company_info['address']}<br/>
        Phone: {self.company_info['phone']} | Email: {self.company_info['email']}
        """
        story.append(Paragraph(company_details, self.styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        # PO Title
        story.append(Paragraph(f"PURCHASE ORDER #{purchase_order.po_number}", self.styles['InvoiceTitle']))
        story.append(Spacer(1, 0.1*inch))
        
        # PO Details
        details_data = [
            ['PO Date:', purchase_order.po_date.strftime('%d-%m-%Y'), 'Expected Delivery:', purchase_order.expected_delivery.strftime('%d-%m-%Y')],
            ['Supplier:', purchase_order.supplier_name, 'Status:', purchase_order.status.upper()]
        ]
        
        details_table = Table(details_data, colWidths=[1.5*inch, 2*inch, 1.5*inch, 2*inch])
        details_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#666666')),
            ('TEXTCOLOR', (2, 0), (2, -1), colors.HexColor('#666666')),
        ]))
        story.append(details_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Items Table
        items_data = [['S.No', 'Product', 'Qty', 'Unit Cost', 'Total']]
        
        for idx, item in enumerate(purchase_order.items, 1):
            items_data.append([
                str(idx),
                item.product_name,
                str(item.quantity),
                f"₹{item.unit_price:.2f}",
                f"₹{item.quantity * item.unit_price:.2f}"
            ])
        
        items_table = Table(items_data, colWidths=[0.5*inch, 3.2*inch, 0.8*inch, 1*inch, 1.5*inch])
        items_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')])
        ]))
        story.append(items_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Totals
        totals_data = [
            ['', '', 'Subtotal:', f"₹{purchase_order.subtotal:.2f}"],
            ['', '', f'Tax ({purchase_order.tax_percent}%):', f"₹{purchase_order.tax_amount:.2f}"],
            ['', '', 'Shipping:', f"₹{purchase_order.shipping_cost:.2f}"],
            ['', '', 'TOTAL AMOUNT:', f"₹{purchase_order.total_amount:.2f}"]
        ]
        
        totals_table = Table(totals_data, colWidths=[2.2*inch, 1.3*inch, 1.5*inch, 1.5*inch])
        totals_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (2, -1), 'Helvetica'),
            ('FONTNAME', (3, 0), (3, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -2), 9),
            ('FONTSIZE', (0, -1), (-1, -1), 11),
            ('TEXTCOLOR', (0, -1), (-1, -1), colors.HexColor('#667eea')),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#f0f0f0')),
            ('GRID', (2, 0), (-1, -1), 1, colors.grey),
        ]))
        story.append(totals_table)
        
        if purchase_order.notes:
            story.append(Spacer(1, 0.3*inch))
            story.append(Paragraph("<b>Special Instructions:</b>", self.styles['Normal']))
            story.append(Paragraph(purchase_order.notes, self.styles['Normal']))
        
        story.append(Spacer(1, 0.3*inch))
        footer_text = f"<br/><br/>Generated on {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
        story.append(Paragraph(footer_text, self.styles['Normal']))
        
        doc.build(story)
        return filename
