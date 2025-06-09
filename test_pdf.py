from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Flowable, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
from datetime import datetime

# --- Section Banner with rounded corners ---
class SectionBar(Flowable):
    def __init__(self, width, height, color, text):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.color = color
        self.text = text

    def draw(self):
        self.canv.setFillColor(self.color)
        self.canv.roundRect(0, 0, self.width, self.height, 8, fill=1, stroke=0)
        self.canv.setFillColor(white)
        self.canv.setFont("Helvetica-Bold", 15)
        self.canv.drawCentredString(self.width/2, self.height/2-5, self.text)

# --- Top Banner ---
class ColorBar(Flowable):
    def __init__(self, width, height, color, text):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.color = color
        self.text = text

    def draw(self):
        self.canv.setFillColor(self.color)
        self.canv.rect(0, 0, self.width, self.height, fill=1, stroke=0)
        self.canv.setFillColor(white)
        self.canv.setFont("Helvetica-Bold", 22)
        self.canv.drawCentredString(self.width/2, self.height/2-8, self.text)

# --- Footer Banner ---
def draw_footer(canvas, doc):
    width = doc.pagesize[0]
    banner_height = 28
    canvas.saveState()
    canvas.setFillColor(HexColor('#2471A3'))
    canvas.rect(0, 0, width, banner_height, fill=1, stroke=0)
    canvas.setFillColor(white)
    canvas.setFont("Helvetica-Bold", 13)
    canvas.drawCentredString(width/2, 8, "©2024 MCI Canada")
    canvas.restoreState()

# --- Styles ---
def get_custom_styles():
    styles = getSampleStyleSheet()
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        textColor=HexColor('#2C3E50'),
        spaceAfter=10,
        fontName='Helvetica'
    )
    verse_style = ParagraphStyle(
        'Verse',
        parent=styles['Normal'],
        fontSize=12,
        textColor=HexColor('#2471A3'),
        spaceAfter=14,
        fontName='Helvetica-Oblique',
        alignment=1
    )
    subtitle_style = ParagraphStyle(
        'Subtitle',
        fontSize=15,
        textColor=HexColor('#2C3E50'),
        alignment=1,
        fontName='Helvetica-Bold',
        spaceAfter=6,
        spaceBefore=0
    )
    return {
        'normal': normal_style,
        'verse': verse_style,
        'subtitle': subtitle_style
    }

def create_pdf(form_data, disc_descriptions, don_descriptions, don_roles_by_region, egalite_message):
    filename = f"resultats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    doc = SimpleDocTemplate(
        filename,
        pagesize=landscape(letter),
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    styles = get_custom_styles()
    story = []

    # --- Top Banner ---
    story.append(ColorBar(doc.width + doc.leftMargin + doc.rightMargin, 40, HexColor('#8e44ad'), "Parcours Découverte MCI Canada"))
    story.append(Paragraph("Résultat des tests de personnalité et de dons.", styles['subtitle']))
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor('#2471A3')))
    story.append(Spacer(1, 16))

    # --- Coordonnées Section ---
    story.append(SectionBar(doc.width, 28, HexColor('#2471A3'), "Coordonnées"))
    story.append(Spacer(1, 10))
    coord_labels = [
        ("Prénom", form_data.get('prenom', '')),
        ("Nom de Famille", form_data.get('nom', '')),
        ("Adresse Courriel", form_data.get('courriel', '')),
        ("Date de naissance", form_data.get('date_naissance', '')),
        ("Genre", form_data.get('genre', '')),
        ("Vous souvenez-vous de votre date de salut ?", form_data.get('date_salut', '')),
        ("Date de salut", form_data.get('date_salut_date', '')),
        ("Êtes-vous baptisé(e) par immersion ?", form_data.get('baptise', '')),
        ("Date de baptême", form_data.get('date_bapteme', '')),
        ("État matrimonial", form_data.get('etat_matrimonial', '')),
        ("Date Completion Formulaire", datetime.now().strftime('%d/%m/%Y')),
    ]
    mid = (len(coord_labels) + 1) // 2
    left = coord_labels[:mid]
    right = coord_labels[mid:]
    if len(left) > len(right):
        right += [('', '')] * (len(left) - len(right))
    coord_table_data = []
    for l, r in zip(left, right):
        coord_row = [
            Paragraph(f"<b>{l[0]}</b><br/>{l[1]}", styles['normal']),
            Paragraph(f"<b>{r[0]}</b><br/>{r[1]}", styles['normal']) if r[0] else ''
        ]
        coord_table_data.append(coord_row)
    coord_table = Table(coord_table_data, colWidths=[3.5*inch, 3.5*inch])
    coord_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), HexColor('#F8F9F9')),
        ('BOX', (0, 0), (-1, -1), 0.5, HexColor('#D6DBDF')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(coord_table)
    story.append(Spacer(1, 24))

    # --- Profil de personnalité DISC Section ---
    story.append(SectionBar(doc.width, 28, HexColor('#2471A3'), "Profil de personnalité DISC"))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "«Merci d’avoir fait de moi une créature aussi merveilleuse : tu fais des merveilles, et je le reconnais bien. »<br/>Psaume 139 : 1",
        styles['verse']
    ))
    story.append(Spacer(1, 6))
    disc_table_data = [
        [Paragraph("<b>Type</b>", styles['normal']), Paragraph("<b>Description</b>", styles['normal'])]
    ]
    for disc_type, desc in disc_descriptions.items():
        disc_table_data.append([
            Paragraph(disc_type, styles['normal']),
            Paragraph(desc, styles['normal'])
        ])
    disc_table = Table(disc_table_data, colWidths=[1.5*inch, 7*inch])
    disc_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2471A3')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#F8F9F9')),
        ('LINEBELOW', (0, 0), (-1, 0), 1, HexColor('#2471A3')),
        ('LINEBELOW', (0, 1), (-1, -1), 0.5, HexColor('#D6DBDF')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(disc_table)
    story.append(Spacer(1, 16))

    # --- Egalité message (si besoin) ---
    if egalite_message:
        story.append(Paragraph(egalite_message, styles['normal']))
        story.append(Spacer(1, 16))

    # --- Dons principaux et équipes recommandées Section ---
    story.append(SectionBar(doc.width, 28, HexColor('#2471A3'), "Dons principaux et équipes recommandées"))
    story.append(Spacer(1, 10))
    if don_roles_by_region:
        region_names = list(next(iter(don_roles_by_region.values())).keys())
    else:
        region_names = []
    don_table_header = [Paragraph("<b>Don</b>", styles['normal']), Paragraph("<b>Description</b>", styles['normal'])]
    for region in region_names:
        don_table_header.append(Paragraph(f"<b>{region}</b>", styles['normal']))

    don_table_data = [don_table_header]
    for don, desc in don_descriptions.items():
        row = [Paragraph(don, styles['normal']), Paragraph(desc, styles['normal'])]
        for region in region_names:
            roles = don_roles_by_region[don].get(region, [])
            roles_str = "<br/>".join(roles) if roles else "-"
            row.append(Paragraph(roles_str, styles['normal']))
        don_table_data.append(row)

    don_table = Table(don_table_data, colWidths=[1.2*inch, 3.5*inch] + [2*inch]*len(region_names))
    don_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2471A3')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#F8F9F9')),
        ('LINEBELOW', (0, 0), (-1, 0), 1, HexColor('#2471A3')),
        ('LINEBELOW', (0, 1), (-1, -1), 0.5, HexColor('#D6DBDF')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(don_table)
    story.append(Spacer(1, 24))

    # --- Disponibilité Section ---
    story.append(SectionBar(doc.width, 28, HexColor('#2471A3'), "Disponibilité"))
    story.append(Spacer(1, 10))
    dispo_data = [[
        Paragraph(f"<b>Temps disponible</b><br/>{form_data.get('temps', '')}", styles['normal']),
        Paragraph(f"<b>Précision</b><br/>{form_data.get('precision', '')}", styles['normal'])
    ]]
    dispo_table = Table(dispo_data, colWidths=[4*inch, 4*inch])
    dispo_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), HexColor('#F8F9F9')),
        ('BOX', (0, 0), (-1, -1), 0.5, HexColor('#D6DBDF')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(dispo_table)
    story.append(Spacer(1, 24))

    doc.build(story, onFirstPage=draw_footer, onLaterPages=draw_footer)
    print(f"PDF généré : {filename}")

if __name__ == "__main__":
    # Example data
    form_data = {
        "prenom": "Mirabelle",
        "nom": "Perfection Divine",
        "courriel": "mirabelle@example.com",
        "date_naissance": "1990-01-01",
        "genre": "Femme",
        "date_salut": "oui",
        "date_salut_date": "2005-06-15",
        "baptise": "oui",
        "date_bapteme": "2006-09-10",
        "etat_matrimonial": "Célibataire",
        "temps": "Soirs de semaine",
        "precision": "Disponible après 18h, sauf le mercredi"
    }
    disc_descriptions = {
        "D/S": """Nous sommes exécuteurs avec une habileté à persévérer. Nous sommes plus actifs que passifs,
mais possédons une calme sensibilité et de la fermeté qui fait de nous de bons leaders. Il semble que
nous sommes orientés vers les gens, mais pouvons facilement être dominants et décisifs quand vient
la planification des tâches et des projets. Nous nous efforçons d’accomplir des buts avec une
détermination féroce qui vient d’une forte énergie intérieure, mais nous pourrions tirer profit d’une
réflexion contemplative et conservatrice ainsi que de passer plus de temps à focaliser sur nos
relations. Daniel (Daniel 1-6), Job (Job 1: 5, Jacques 5: 11), Marthe (Luc 10: 38-42).""",
        "S/D": """Nous sommes des leaders tranquilles sur qui on peut compter pour que le travail soit fait. Nous
performons mieux dans des petits groupes et n’aimons pas parler devant des foules. Bien que nous
puissions être à la fois doux et durs de cœur, nous apprécions des relations étroites avec les gens,
faisant attention pour ne pas dominer sur eux. Les défis nous motivent, en particulier ceux qui nous
permettent d’avoir une approche méthodique. Nous avons tendance à être déterminés, persévérant à
travers le temps et les luttes. Nous bénéficions de l’encouragement et des relations positives. Marthe
(Luc 10 : 38-42), Job (Job 1 :5, Jacques 5 : 11)."""
    }
    don_descriptions = {
        "Enseignement": "Capacité à transmettre la Parole de façon claire et structurée.",
        "Service": "Aide pratique et soutien dans l’église, avec humilité."
    }
    don_roles_by_region = {
        "Enseignement": {
            "Montréal": ["Équipe Alpha", "Équipe Beta"],
            "St-Bruno": ["Équipe Gamma"]
        },
        "Service": {
            "Montréal": ["Équipe Delta"],
            "St-Bruno": ["Équipe Epsilon", "Équipe Zeta"]
        }
    }
    egalite_message = (
        "Vous avez obtenu des résultats identiques pour votre test de personnalité. Nous vous invitons donc à :<br/>"
        "1.- Lire la définition de chaque trait de personnalité de votre résultat.<br/>"
        "2.- Envoyer un courriel à :<br/>"
        "   - Si Montréal : decouverte@mcigc.ca pour nous mentionner le trait de personnalité qui vous représente le mieux.<br/>"
        "   - Si St-Bruno : decouverters@mcigc.ca pour nous mentionner le trait de personnalité qui vous représente le mieux."
    )

    create_pdf(form_data, disc_descriptions, don_descriptions, don_roles_by_region, egalite_message)