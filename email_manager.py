import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import yaml
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import os

class EmailManager:
    def __init__(self):
        self.config_path = "config.yaml"

    def load_config(self):
        with open(self.config_path, "r", encoding='utf-8') as f:
            return yaml.safe_load(f)["email"]

    def _format_personality_results(self, personality_scores, personality_type):
        scores_text = "\n".join([f"{trait}: {score}/25" for trait, score in personality_scores.items()])
        type_text = ", ".join(personality_type) if isinstance(personality_type, list) else personality_type
        return f"Résultats du test DISC:\n\n{scores_text}\n\nType de personnalité dominant: {type_text}"

    def _create_pdf(self, form_data):
        # Create a temporary PDF file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"resultats_{timestamp}.pdf"
        
        # Create the PDF with landscape orientation
        doc = SimpleDocTemplate(
            filename,
            pagesize=landscape(letter),
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )

        # Get styles
        styles = getSampleStyleSheet()
        title_style = styles['Heading1']
        normal_style = styles['Normal']
        
        # Create the story (content)
        story = []
        
        # Add title
        story.append(Paragraph("Résultats des Tests - MCI Canada", title_style))
        story.append(Spacer(1, 30))
        
        # Add personality test results
        story.append(Paragraph("Résultats du Test DISC", styles['Heading2']))
        story.append(Spacer(1, 12))
        
        # Create table for personality scores
        scores_data = [[Paragraph("Trait", normal_style), Paragraph("Score", normal_style)]]
        for trait, score in form_data['personality_scores'].items():
            scores_data.append([Paragraph(trait, normal_style), Paragraph(f"{score}/25", normal_style)])
        
        scores_table = Table(scores_data, colWidths=[4*inch, 2*inch])
        scores_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(scores_table)
        story.append(Spacer(1, 20))
        
        # Add personality type
        type_text = ", ".join(form_data['personality_type']) if isinstance(form_data['personality_type'], list) else form_data['personality_type']
        story.append(Paragraph(f"Type de personnalité dominant: {type_text}", styles['Heading2']))
        
        # Build the PDF
        doc.build(story)
        
        return filename

    def send_email(self, form_data):
        config = self.load_config()
        
        msg = MIMEMultipart()
        msg['From'] = f"{config['sender_name']} <{config['sender_email']}>"
        
        # Add all recipients
        recipients = [form_data.get('courriel', '')] + [admin['email'] for admin in config['admin_recipients']]
        msg['To'] = ', '.join(recipients)
        
        msg['Subject'] = "Vos résultats des tests de personnalité et de dons"

        # Create email body
        body = f"""
Bonjour,

Merci d'avoir complété les tests de personnalité et de dons.

{self._format_personality_results(form_data['personality_scores'], form_data['personality_type'])}

N'hésitez pas à poser vos questions lors du cours.

Cordialement,
L'équipe MCI Canada
        """
        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        # Create and attach PDF
        pdf_file = self._create_pdf(form_data)
        with open(pdf_file, 'rb') as f:
            pdf_attachment = MIMEApplication(f.read(), _subtype='pdf')
            pdf_attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(pdf_file))
            msg.attach(pdf_attachment)
        
        # Clean up the temporary PDF file
        os.remove(pdf_file)

        # Send email
        with smtplib.SMTP_SSL(config['smtp_server'], config['smtp_port']) as server:
            server.login(config['username'], config['password'])
            server.send_message(msg)