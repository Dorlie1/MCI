import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import yaml
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
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

    def _create_custom_styles(self):
        styles = getSampleStyleSheet()
        
        # Custom title style
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=HexColor('#2C3E50'),  # Dark blue-grey
            spaceAfter=30,
            alignment=1  # Center alignment
        )
        
        # Custom heading style
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=18,
            textColor=HexColor('#34495E'),  # Lighter blue-grey
            spaceAfter=15,
            spaceBefore=25
        )
        
        # Custom normal style
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=12,
            textColor=HexColor('#2C3E50'),
            spaceAfter=12
        )
        
        return {
            'title': title_style,
            'heading': heading_style,
            'normal': normal_style
        }

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

        # Get custom styles
        styles = self._create_custom_styles()
        
        # Create the story (content)
        story = []
        
        # Add title with date
        title_text = f"Résultats des Tests - MCI Canada\n{datetime.now().strftime('%d/%m/%Y')}"
        story.append(Paragraph(title_text, styles['title']))
        
        # Add personality test results section
        story.append(Paragraph("Profil de Personnalité DISC", styles['heading']))
        
        # Description of DISC
        disc_description = """
        Le modèle DISC est un outil d'évaluation du comportement qui aide à mieux comprendre votre style naturel 
        de communication et d'interaction. Chaque lettre représente une dimension différente du comportement :
        <br/><br/>
        <b>D</b> - Dominance : Comment vous réagissez aux défis<br/>
        <b>I</b> - Influence : Comment vous interagissez avec les autres<br/>
        <b>S</b> - Stabilité : Comment vous réagissez au changement<br/>
        <b>C</b> - Conformité : Comment vous réagissez aux règles
        """
        story.append(Paragraph(disc_description, styles['normal']))
        story.append(Spacer(1, 20))
        
        # Create table for personality scores with improved styling
        scores_data = [
            [Paragraph('<b><font color="white">Dimension</font></b>', styles['normal']), 
             Paragraph('<b><font color="white">Score</font></b>', styles['normal']), 
             Paragraph('<b><font color="white">Interprétation</font></b>', styles['normal'])]
        ]
        
        # Function to get interpretation based on score
        def get_interpretation(score):
            if score >= 20:
                return "Très élevé"
            elif score >= 15:
                return "Élevé"
            elif score >= 10:
                return "Modéré"
            else:
                return "Faible"
        
        for trait, score in form_data['personality_scores'].items():
            scores_data.append([
                Paragraph(trait, styles['normal']),
                Paragraph(f"{score}/25", styles['normal']),
                Paragraph(get_interpretation(score), styles['normal'])
            ])
        
        scores_table = Table(scores_data, colWidths=[2.5*inch, 1.5*inch, 2*inch])
        scores_table.setStyle(TableStyle([
            # Header styling
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#34495E')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            # Alternating row colors
            ('BACKGROUND', (0, 1), (-1, -1), HexColor('#F8F9F9')),
            ('BACKGROUND', (0, 2), (-1, 2), HexColor('#EBF5FB')),
            ('BACKGROUND', (0, 3), (-1, 3), HexColor('#F8F9F9')),
            ('BACKGROUND', (0, 4), (-1, 4), HexColor('#EBF5FB')),
            # Global styling
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#BDC3C7')),
            ('ROWHEIGHT', (0, 0), (-1, -1), 30)
        ]))
        story.append(scores_table)
        story.append(Spacer(1, 30))
        
        # Add a personality type with improved styling
        type_text = ", ".join(form_data['personality_type']) if isinstance(form_data['personality_type'], list) else form_data['personality_type']
        story.append(Paragraph("Votre Type de Personnalité Dominant", styles['heading']))
        story.append(Paragraph(f"<b>{type_text}</b>", styles['normal']))
        
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

        # Create an email body
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