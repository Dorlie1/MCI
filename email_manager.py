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
from db.databse import Database

DISC_MESSAGES = {
            "D": """Dominance (D)
        Nous sommes directs et décidés. Nous prenons des risques et résolvons des problèmes. Nous sommes davantage concernés à terminer des tâches et à gagner plutôt que d’avoir l’approbation des gens.
        Quoique notre énergie intérieure tend à nous rendre insensible à ceux qui nous entourent, les « D » n’ont pas peur de confronter les statu quo, et nous aimons réagir à des confrontations directes. Notre plus grande crainte est que l’on nous tienne pour acquis et même méprise nos possibles faiblesses – ce qui inclus une aversion à la routine, une tendance à sur le dos – nous donnons une grande importance au temps et utilisons notre pensée innovatrice pour accomplir des tâches difficiles et conquérir des défis.""",

            "I": """Influence (I)
        Nous sommes inspirants et faisons impression. Enthousiastes, optimistes, impulsifs et émotionnels nous avons tendance à résoudre les problèmes de façon créative et sommes excellents pour encourager.
        Nous avons souvent un grand nombre d’amis, mais pouvons être davantage concernés par l’approbation et la popularité que l’obtention de résultats. Notre plus grande crainte est le rejet, mais nous sommes à notre meilleur quand vient le temps de motiver les autres. Notre sens de l’humour positif nous aide à gérer les conflits. Quoique nous puissions être inattentifs aux détails et avons une faible écoute, nous pouvons être de grands agents de paix et des co-équipiers efficaces quand nous contrôlons nos sentiments et minimisons notre besoin de divertir et de devenir le centre d’attraction. Nous valorisons beaucoup les contacts humains et les relations.""",

            "S": """Stabilité (S)
        Nous sommes stables et plus réservés. Nous n’aimons pas le changement et sommes à l’aise dans des environnements sécuritaires et non menaçants. Nous sommes souvent amicaux et compréhensifs, ainsi que de bons écouteurs et des travailleurs loyaux, qui sont contents de faire le même travail avec constance.
        Avec une incroyable habileté à pardonner, fiables et dignes de confiance, les « S » ont tendance à se faire les meilleurs amis. Cependant, notre plus grande peur est la perte de sécurité et nos possibles faiblesses incluent, naturellement, non seulement la résistance au changement, mais la difficulté de s’y ajuster. Nous pouvons aussi être trop sensibles à la critique et incapables d’établir des priorités. Afin d’éviter qu’on profite de nous, nous avons besoin d’être plus forts et apprendre comment dire « non. » Nous aimons aussi aider les autres, nous allons joyeusement saisir cette occasion. Nous nous sentons davantage valorisés quand nous avons vraiment aidé quelqu’un.""",

            "C": """Conformité (C)
        Nous sommes complaisants et analytiques. Des lignes de pensées prudentes et logiques nous font avancer, et la précision est une priorité élevée. Nos standards sont élevés et nous valorisons une approche systémique à la résolution de problèmes.
        Bien que nous sommes à l’aise quand on nous donne des opportunités de trouver des solutions, nous avons tendance à ignorer les sentiments des autres et nous pouvons facilement être critiques et tout-à-fait grincheux. Il est difficile pour nous de verbaliser nos sentiments, mais quand nous ne sommes pas embourbés dans les détails et avons des limites claires, nous pouvons être un grand avantage pour l’équipe en contribuant par des « vérifications de la réalité » sous forme de calculs. Notre plus grande crainte est la critique et notre besoin de perfection est souvent une faiblesse, ainsi que notre tendance à céder en plein milieu d’un argument. Cependant, nous sommes minutieux dans toutes les activités et pouvons apporter à l’équipe l’élément d’être consciencieux et d’humeur égale qui procurera un fondement solide. Nous valorisons d’être corrects.""",

            "D/I": """D / I
        Nous sommes des finisseurs curieux qui mettons l’emphase sur la dernière ligne et travaillons fort pour atteindre nos buts. Nous sommes plus déterminés qu’inspirés, cependant nos attentes et standards élevés envers nous-mêmes et ceux qui nous entourent, typiquement nous amènent à faire un impact, motivant les autres à nous suivre. Nous avons un étalage d’intérêts et pouvons devenir distraits en entreprenant trop de projets. Nous avons souvent besoin de nous focaliser, prioriser et simplement ralentir. Parce que nous sommes à l’aise dans l’activité et aller de l’avant, nous aimons accomplir des tâches au moyen d’un grand nombre de personnes. Josué (Josué 1), Noé (Genèse 6-9), Sarah (Genèse 16, 1 Pierre 3 : 6).""",

            "D/S": """D / S
        Nous sommes exécuteurs avec une habileté à persévérer. Nous sommes plus actifs que passifs, mais possédons une calme sensibilité et de la fermeté qui fait de nous de bons leaders. Il semble que nous sommes orientés vers les gens, mais pouvons facilement être dominants et décisifs quand vient la planification des tâches et des projets. Nous nous efforçons d’accomplir des buts avec une détermination féroce qui vient d’une forte énergie intérieure, mais nous pourrions tirer profit d’une réflexion contemplative et conservatrice ainsi que de passer plus de temps à focaliser sur nos relations. Daniel (Daniel 1-6), Job (Job 1: 5, Jacques 5: 11), Marthe (Luc 10: 38-42).""",

            "D/C": """D / C
        Nous sommes des provocateurs qui pouvons être, soit des étudiants déterminés, soit des critiques qui défient. C’est important pour nous d’être en charge, cependant il nous importe peu ce que les autres pensent de nous du moment que le travail est accompli. Nous sommes très prévoyants et examinons toutes les possibilités pour trouver la meilleure solution. Nous préférons travailler seul. Bien que nous craignions l’échec et le manque d’influence, nous sommes motivés par les défis et pouvons souvent être d’excellents administrateurs. Nous pourrions tirer bénéfice de relaxer et de porter une meilleure attention aux gens. Malachie (Malachie 4), Nathan (2 Samuel 12 :1-13), Nahum (Nahum 1-3).""",

            "I/D": """I / D
        Nous sommes des personnes persuasives, sociables et énergiques. Nous aimons les grands groupes et utilisons notre pouvoir d’influence pour nous attirer le respect et convaincre les gens de suivre notre direction. Parfois, nous pouvons être perçus comme agités et nerveux, mais cela vient de notre besoin d’avoir part à des défis qui comportent de la variété, de la liberté et de la mobilité. Nous aurions avantage à regarder avant de sauter dans l’inconnu et prendre plus de temps pour étudier et rester tranquille. Nous sommes des leaders inspirants et savons comment obtenir des résultats des gens et à travers eux. Jean Baptiste (Luc 3), Pierre (Matthieu 16 et 26, Actes 3), Rébecca (Genèse 24).""",

            "I/S": """I / S
        Nous sommes des conseillers d’influence qui aiment les gens et ce n’est pas une surprise que les gens nous aiment. Nous vivons pour plaire et servir et avons tendance à avoir une bonne écoute. Bien paraître et encourager les autres est important pour nous, de même que poursuivre jusqu’au bout et être obéissant. Nous avons souvent des lacunes au niveau de l’organisation et pouvons davantage être concernés pour les personnes impliquées que la tâche qui nous a été confiée. Cependant, nous pouvons être tout aussi efficaces au milieu de la scène qu’en arrière-plan et nous brillons quand vient le temps d’influencer et d’aider les autres. Barnabas (Actes 4, 9, 11-15), Élisée (1 Rois 19, 2 Rois 2-3), Nicodème (Jean 3, 7, 19).""",

            "I/C": """I / C
        Nous sommes inspirants, quoique de prudents estimateurs qui sommes d’excellents communicateurs grâce à la combinaison d’une conscience concernée et de l’appréciation des gens. Nous excellons dans la façon d’améliorer la productivité. Nous avons tendance à être impatients et critiques et pouvons aussi être trop persuasifs et trop consumés par le désir de gagner. Nous aimons travailler à « l’intérieur de la boîte » et nous aurions avantage à essayer de nouvelles choses et moins nous inquiéter à propos de ce que les autres pensent. Ce type de personnalité possède souvent le don d’enseigner; généralement, on peut se fier sur nous quand vient le temps de porter attention aux détails et de faire le travail.""",

            "S/D": """S / D
        Nous sommes des leaders tranquilles sur qui on peut compter pour que le travail soit fait. Nous performons mieux dans des petits groupes et n’aimons pas parler devant des foules. Bien que nous puissions être à la fois doux et durs de cœur, nous apprécions des relations étroites avec les gens, faisant attention pour ne pas dominer sur eux. Les défis nous motivent, en particulier ceux qui nous permettent d’avoir une approche méthodique. Nous avons tendance à être déterminés, persévérant à travers le temps et les luttes. Nous bénéficions de l’encouragement et des relations positives. Marthe (Luc 10 : 38-42), Job (Job 1 :5, Jacques 5 : 11).""",

            "S/I": """S / I
        Nous sommes des conseillers inspirants qui démontrent de la chaleur et de la sensibilité. Tolérants et indulgents, nous avons beaucoup d’amis parce qu’ils acceptent et représentent bien les autres. Notre nature sociable, désireuse d’être aimée et flexible nous rend enclins à être trop tolérants et à ne pas vouloir confronter. Nous pourrions bénéficier d’être davantage orientés vers la tâche et d’accorder plus d’attention aux détails. Gentil et pleins de considération, nous incluons les autres et inspirons les gens à nous suivre. Les mots d’affirmation peuvent nous suivre longtemps et avec la bonne motivation, nous pouvons être d’excellents co-équipiers. Marie de Magdala (Luc 7 : 36 – 47), Barnabas (Actes 4, 9, 11 – 15), Élisée (1 Rois 19, 2 Rois 2 – 13).""",

            "S/C": """S / C
        Nous sommes diplomates et fermes, ainsi qu’orientés vers les détails. Stables et contemplatifs, nous aimons peser les évidences et découvrir les faits avant d’arriver à une conclusion logique. Plus réfléchis, nous préférons prendre notre temps, en particulier quand les décisions impliquent d’autres personnes. Les faiblesses possibles incluent être très sensible et incapables de gérer la critique et nous devons faire attention à la manière dont nous traitons les autres. Opérant à notre meilleur dans des projets précis et pour une bonne cause, nous pouvons être un vecteur de paix; ceci fait de nous un équipier loyal et un ami. Moïse (Exode 3, 4, 20, 32), Jean (Jean 19 : 26 – 27), Éliézer (Genèse 24).""",

            "C/D": """C / D
        Nous sommes des inventeurs prudents et déterminés qui sommes constamment orientés vers la tâche et conscients des problèmes. Parfois perçus comme insensibles, oui nous sommes concernés pour les individus, mais avons de la difficulté à le démontrer. Souvent nous pensons que nous sommes les seuls à pouvoir faire le travail, mais à cause de nos habiletés administratives, nous sommes capables d’apporter des plans pour changer et améliorer les choses pour donner plus de fruits. Nous avons tendance à être sérieux et pourrions tirer avantage à être plus optimistes et enthousiastes. Malgré notre désir naturel de réussir, nous devrions nous concentrer à développer des relations saines et tout simplement aimer les gens. Betsaleel (Exode 35 : 30 – 36, 8, 37 : 1 – 9), Jochebed (Exode 1 : 22-2 :4), Jethro (Exode 2, 18).""",

            "C/I": """C / I
        Nous sommes attentifs aux détails. Nous essayons d’impressionner les autres en faisant les choses de la bonne façon et de stabiliser les situations. Non considérés comme agressifs et poussifs, nous aimons à la fois les grandes et les petites foules. Bien que nous travaillions bien avec les gens, nous sommes parfois trop sensibles en rapport à ce que les autres pensent de nous et de notre travail. Nous pourrions tirer avantage d’être plus autoritaires et auto-motivés. Souvent, nous sommes de très bons juges des caractères, nous faisons facilement confiance à ceux qui rencontrent nos standards. Nous sommes motivés par une véritable et enthousiaste approbation ainsi que par des explications concises et logiques. Myriam (Exode 15 – 21, Nombres 12 : 1 – 15), Esdras (Esdras 7, 8).""",

            "C/S": """C / S
        Nous sommes systémiques et stables. Nous avons tendance à faire une chose à la fois – et la faire bien. Réservés et prudents, nous aimerions mieux travailler à l’arrière-scène pour rester sur la bonne voie; cependant, nous prenons rarement des risques ou n’essayons de nouvelles choses et évidemment nous n’aimons pas les changements brusques dans notre environnement. Recherchant la précision à la lettre, nous requérons soigneusement l’exactitude et avons peur de la critique qui équivaut pour nous à l’échec. Travailleurs diligents, notre motivation vient du désir de servir les autres. Esther (Esther 4), Zacharie (Luc 1), Joseph (Matthieu 1 : 1 – 23).""",    
    }

class EmailManager:

    def __init__(self):
        self.config_path = "config.yaml"
        self.db = Database()

    def load_config(self):
        with open(self.config_path, "r", encoding='utf-8') as f:
            return yaml.safe_load(f)["email"]

    def _get_roles_for_traits(self, traits):
        all_roles = self.db.get_all_roles()
        matching_roles = {}
        
        # Map full trait names to codes
        trait_map = {
            'Dominance': 'D',
            'Influence': 'I',
            'Stabilité': 'S',
            'Sérieux': 'C'  # Assuming "Sérieux" corresponds to "Conformité"
        }
        
        # Convert full trait names to codes
        trait_codes = [trait_map[trait] for trait in traits if trait in trait_map]
        
        # Initialize dictionary with region keys
        for role in all_roles:
            if role['region'] not in matching_roles:
                matching_roles[role['region']] = []
        
        # Add roles that match the traits
        for role in all_roles:
            if role['trait'] in trait_codes:
                matching_roles[role['region']].append(role['nom'])
        
        return matching_roles

    def get_disc_message(self, personality_types):
        """
        personality_types: liste de types dominants, ex: ['D'], ['D', 'I'], etc.
        Retourne le message DISC avec "Voici la description :" si applicable.
        """ 
        # Map full names to codes
        trait_map = {
            'Dominance': 'D',
            'Influence': 'I',
            'Stabilité': 'S',
            'Sérieux': 'C',
        }
        if personality_types and isinstance(personality_types[0], str) and '/' in personality_types[0]:
            parts = [p.strip() for p in personality_types[0].split('/')]
        else:
            # fallback: treat as single or already split
            parts = personality_types

        codes = [trait_map.get(t.strip(), t.strip()) for t in parts]
        print("codes:", codes)

        if len(codes) == 1:
            key = codes[0]
        elif len(codes) == 2:
            key1 = f"{codes[0]}/{codes[1]}"
            key2 = f"{codes[1]}/{codes[0]}"
            print(key1, key2)
            key = key1 if key1 in DISC_MESSAGES else key2 if key2 in DISC_MESSAGES else None
        else:
            key = None

        if key and key in DISC_MESSAGES:
            return "Voici la description :\n\n" + DISC_MESSAGES[key]
        else:
            return ""

    def _format_personality_results(self, personality_scores, personality_type):
        # Format the DISC scores
        scores_text = "\n".join([f"{trait}: {score}/25" for trait, score in personality_scores.items()])
        
        # Get the dominant traits (those with score >= 15)
        dominant_traits = [trait for trait, score in personality_scores.items() if score >= 15]
        
        # Get matching roles for the dominant traits
        matching_roles = self._get_roles_for_traits(dominant_traits)
        
        # Format the roles by region
        roles_text = "\n\nÉquipes recommandées basés sur votre profil:\n"
        for region, roles in matching_roles.items():
            if roles:  # Only show regions that have matching roles
                roles_text += f"\n{region}:\n"
                roles_text += "\n".join(f"- {role}" for role in roles)
        
        # Combine all parts
        type_text = ", ".join(personality_type) if isinstance(personality_type, list) else personality_type
        return f"""Résultats du test DISC:

{scores_text}

Type de personnalité dominant: {type_text}{roles_text}"""

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
        
        # Add personality type and role recommendations
        type_text = ", ".join(form_data['personality_type']) if isinstance(form_data['personality_type'], list) else form_data['personality_type']
        story.append(Paragraph("Votre Type de Personnalité Dominant", styles['heading']))
        story.append(Paragraph(f"<b>{type_text}</b>", styles['normal']))
        
        # Add role recommendations
        story.append(Paragraph("Équipes Recommandées", styles['heading']))
        
        # Get dominant traits and matching roles
        dominant_traits = [trait for trait, score in form_data['personality_scores'].items() if score >= 15]
        matching_roles = self._get_roles_for_traits(dominant_traits)
        
        # Create a table for role recommendations
        roles_data = []
        for region, roles in matching_roles.items():
            if roles:  # Only show regions that have matching roles
                roles_data.append([
                    Paragraph(f"<b>{region}</b>", styles['normal']),
                    Paragraph("<br/>".join([f"• {role}" for role in roles]), styles['normal'])
                ])
        
        if roles_data:
            roles_table = Table(roles_data, colWidths=[2*inch, 5*inch])
            roles_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('GRID', (0, 0), (-1, -1), 1, HexColor('#BDC3C7')),
                ('BACKGROUND', (0, 0), (-1, -1), HexColor('#F8F9F9')),
                ('PADDING', (0, 0), (-1, -1), 12),
            ]))
            story.append(roles_table)
        
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

        message = self.get_disc_message(form_data['personality_type'])
        if message:
            body += "\n\n" + message

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