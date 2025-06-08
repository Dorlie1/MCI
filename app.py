from flask import (Flask, render_template, redirect, url_for, request, session, flash)
import email_manager
from calculs import process_form_data, process_don_form_data
from db.databse import Database
from functools import wraps
import os

app = Flask(__name__)
# Not the correct key, its for git
app.secret_key = os.urandom(24)
db = Database()

QUESTIONS_FIXES = [
    "Je suis confiant, exigeant et décidé",
    "J'aime accomplir plusieurs tâches à la fois",
    "Je me sens bien dans un environnement rempli de défis",
    "Je pense plus aux tâches, qu'aux autres ou à moi-même",
    "Je suis motivé par l'accomplissement et l'autorité",
    "J'aime influencer et inspirer d'autres personnes",
    "Je suis optimiste au sujet des autres",
    "J'ai tendance à être celui qui retient l'attention",
    "Je pense à motiver les gens",
    "Je suis motivé par la reconnaissance et l'approbation",
    "Je me développe bien dans un environnement stable",
    "Je préfère des consignes précises plus que des consignes générales",
    "J'aime les petits groupes de personnes",
    "Je préfère être un membre dans une équipe",
    "Je suis motivé par la stabilité et le soutien",
    "Je ne suis pas porté à prendre de grands risques",
    "J'aime les tâches, l'ordre et les détails",
    "La plupart du temps, j'ai raison",
    "Je me soumets à des règles clairement définies",
    "Je suis motivé par la qualité et l'exactitude"
]

don_questions = [
    "J'aime apprendre à propos du domaine de la gestion et aussi comment fonctionnent les organisations.",
    "Je suis capable de percevoir ce que les gens veulent vraiment communiquer, tant par ce qu'ils disent que par ce qu'ils ne disent pas.",
    "Je me sens accompli(e) lorsque je peux façonner\\créer quelque chose qui aide un des ministères de l'Église.",
    "En conversant, les autres me disent souvent : « Je n'ai jamais vu les choses de cette manière ».",
    "J'ai reçu des réactions positives en confrontant des personnes qui s'éloignaient de la vérité.",
    "Je recherche les non-croyants afin de leur présenter le message de Christ.",
    "J'aime donner de mes ressources à ceux qui en ont besoin.",
    "J'aime travailler dans l'ombre afin que les autres utilisent leurs dons d'une façon plus efficace.",
    "J'utilise ma maison pour apporter le ministère aux personnes en besoin.",
    "J'accepte volontiers la responsabilité pour des groupes qui manquent de direction ou de leadership.",
    "Je suis capable de m'identifier aux personnes qui souffrent et de m'impliquer dans leur processus de guérison.",
    "Je dis la vérité selon la Parole de Dieu même quand ce n'est pas populaire et difficile à accepter des autres.",
    "Il m'est important de bien connaître ceux que je sers et que je guide, et de me faire connaître d'eux.",
    "Je peux communiquer des concepts bibliques difficiles de façon à ce que les gens soient motivés à les apprendre et à les étudier davantage.",
    "Dès que je connais un but, j'aime développer un plan ou une stratégie pour l'atteindre.",
    "Les gens disent que j'ai une oreille patiente et attentive.",
    "Je peux visualiser comment une chose doit être construite avant de la construire.",
    "J'aime le défi de communiquer avec variété et créativité.",
    "Je suis attiré(e) vers ceux qui sont confus ou troublés afin de les encourager.",
    "Je recherche des manières différentes de partager efficacement ma foi.",
    "Parce que je veux voir des choses significatives arriver pour la gloire de Dieu, je donne plus que la dîme.",
    "Je crois que les tâches routinières que j'accomplis pour les ministères dans l'Église ont de l'importance spirituelle.",
    "J'aime rencontrer de nouvelles personnes et les aider à connaître d'autres gens dans l'Église.",
    "Je peux organiser efficacement les gens afin d'atteindre des buts spécifiques que je perçois comme étant le plan de Dieu.",
    "J'aime apporter le ministère aux personnes dans les hôpitaux, les prisons et les maisons de convalescence.",
    "Je me sens obligé(e) de démasquer le péché dans la culture, dans l'Église ou dans la vie de quelqu'un, afin que les gens marchent constamment dans la vérité.",
    "J'aime éduquer patiemment mais fermement les autres dans leur développement comme enfants de Dieu.",
    "J'aime étudier la Bible et partager des idées d'ordre pratique qui aideront les autres à grandir et agir dans l'obéissance.",
    "Je suis capable de visualiser un événement futur et résoudre des problèmes éventuels avant qu'ils n'arrivent.",
    "Je désire aider les gens à vivre une vie pleine et équilibrée.",
    "Je travaille bien de mes mains.",
    "J'aime développer mes aptitudes dans les arts : musique, artisanat, comédie, photographie, etc.",
    "Je mets gentiment mais fermement les autres au défi de se soumettre toujours davantage.",
    "Souvent, lorsque je partage l'Évangile, les gens désirent en savoir plus long à propos d'une relation avec Jésus-Christ.",
    "J'éprouve un sentiment d'accomplissement lorsque je partage mon argent et mes possessions, sans rien attendre en retour.",
    "Je me sens plus accompli(e) lorsque je peux servir dans un domaine où il y a un besoin évident.",
    "Je passe du temps avec les visiteurs afin de les mettre à l'aise et pour qu'ils se sentent appréciés.",
    "Je peux guider les autres pour qu'ils se fixent et atteignent des buts qui les rapprochent de Dieu.",
    "Je peux facilement regarder au-delà des handicaps ou des problèmes qui subsistent chez les autres pour voir une vie importante aux yeux de Dieu.",
    "Je parle de façon convaincante à des groupes ou à des individus à propos de l'obéissance aux commandements et aux enseignements de Dieu.",
    "Je préfère des relations stables et de longues durées à travers lesquelles je peux servir de modèle de leader pour des nouveaux ou des jeunes croyants.",
    "J'organise du matériel biblique et je donne des présentations systématiques qui sont appréciées du Corps.",
    "Je peux organiser des idées, des gens et des événements.",
    "J'ai donné à d'autres des conseils pratiques qui ont amené la guérison dans des relations brisées.",
    "Je peux former, développer ou adapter des ressources matérielles pour rencontrer des besoins.",
    "Je dois régulièrement m'isoler pour réfléchir et utiliser mon imagination.",
    "Je rassure ceux qui ont besoin de prendre des pas courageux dans leur foi, leur famille ou leur vie.",
    "J'ai tellement à cœur les brebis perdues que je me sens constamment motivé(e) à inviter les gens à recevoir Christ.",
    "Je gère bien mon argent afin de pouvoir supporter les ministères et faire avancer la cause de Christ.",
    "Je fais volontiers divers travaux dans l'Église pour rencontrer les besoins des autres.",
    "J'invite spontanément les gens chez moi pour leur apporter le ministère, même si ma maison n'est pas totalement présentable.",
    "Beaucoup de chrétiens demandent mon avis au sujet de décisions qu'ils doivent prendre ou de gestes qu'ils doivent poser.",
    "Je fais ce que je peux dans l'ombre pour démontrer l'amour de Dieu à ceux qui souffrent.",
    "Quand j'applique les principes bibliques à des sujets controversés dans notre culture, les gens changent souvent d'opinion.",
    "J'aime donner une direction et exercer une supervision générale sur quelques chrétiens.",
    "Quand j'enseigne aux autres, je suis à l'aise pour répondre aux questions.",
    "Je peux m'occuper de plusieurs détails à la fois, dans l'accomplissement d'une tâche.",
    "Les gens me confient des choses qu'ils n'ont pas dites aux autres et disent que c'est facile de me parler.",
    "J'aime travailler d'une façon créative avec de la laine, du fil, du métal, du verre, etc.",
    "Je critique d'une façon constructive les performances et le travail d'autrui.",
    "Je suis attiré par les gens aux cœurs brisés et je désire les aider à grandir dans leur foi.",
    "Mes conversations avec les non-croyants semblent souvent inclure des sujets spirituels.",
    "Je donne souvent anonymement pour aider à rencontre les besoins financiers d'un individu ou d'un ministère.",
    "J'aime trouver des choses à faire et les exécuter, même sans qu'on me le demande.",
    "J'aime accueillir, souhaiter la bienvenue et créer une atmosphère chaleureuse pour ceux qui s'occupent de diverses fonctions dans l'Église.",
    "Parce que je peux ajuster mon style de leadership, je peux motiver une grande variété d'individus à travailler ensemble pour atteindre un but ou accomplir une tâche.",
    "Je peux soutenir avec patience ceux qui passent à travers des expériences difficiles, pendant qu'ils essaient de stabiliser leur vie émotionnelle et spirituelle.",
    "Quand je communique des vérités divines, les gens sont inspirés à les appliquer et à se détourner de leurs erreurs.",
    "J'ai de la compassion pour les croyants égarés et je désire les protéger.",
    "Des chrétiens m'ont dit qu'ils ont changé leur comportement parce que je les ai aidés à mieux comprendre une vérité biblique ou un sujet personnel.",
    "J'aime rendre les ministères plus efficaces.",
    "Je me soucie des gens en les aidants à trouver des solutions pratiques à leurs difficultés spirituelles ou relationnelles.",
    "Je suis capable de concevoir et de construire des choses qui aident l'Église à mieux prendre soin des gens.",
    "À travers mes expressions artistiques, des gens ont reconnu des vérités plus profondes à propos d'eux-mêmes, de leurs relations, et de Dieu.",
    "Je fortifie ceux qui vacillent dans leur foi en les dirigeants vers les promesses et la vérité de Dieu.",
    "J'aime que les gens qui m'entourent sachent que je suis chrétien et je désire qu'ils m'interrogent sur ma relation avec Christ.",
    "Je suis capable de gagner de gros montants d'argent pour l'œuvre du Seigneur.",
    "Il m'est difficile de dire « non » lorsque je vois tant de besoins dans l'Église.",
    "J'ouvre ma maison avec joie à ceux qui ont besoin de soutien physique ou émotionnel.",
    "Je sais habituellement où je vais et je peux influencer d'autres chrétiens dans cette direction.",
    "J'aide ceux qui sont sans soutien et qui sont considérés indignes par les autres.",
    "Je stimule les autres à utiliser des principes bibliques lors de prise de décision dans leur vie privée \\personnelle et publique\\professionnelle.",
    "Je peux guider la personne dans tout ce qu'elle est : relationnellement, émotionnellement, physiquement, spirituellement, etc.",
    "J'aime expliquer la Parole de façon à amener les gens à écouter et à agir en conséquence.",
    "Je perçois les gens comme des ressources précieuses à coordonner, pour une plus grande efficacité dans l'Église.",
    "Je suis capable de m'identifier et d'aider des personnes amères, en colère et dans la confusion.",
    "J'honore Dieu par mes dons et habiletés manuelles.",
    "À moins de faire quelque chose qui m'intéresse, j'ai généralement une capacité d'attention limitée.",
    "J'inspire les autres à prendre le règne de Christ plus au sérieux.",
    "Quand je partage mon témoignage et le plan de Dieu pour le salut, les gens répondent souvent par la foi.",
    "Quand je sais que les ressources que je partage avec les autres sont vraiment nécessaires, je ne m'inquiète pas de savoir si mes ressources seront réapprovisionnées.",
    "J'aime utiliser mes habiletés tant naturelles qu'acquises pour aider un ministère à être plus efficace.",
    "J'aime fournir le gîte et le couvert à ceux qui en ont besoin.",
    "Je suis capable de clarifier une vision pour le ministère et de gérer les gens et les ressources d'une façon décidée pour amener sa réalisation.",
    "On m'a dit que je m'implique trop personnellement et émotivement lorsque j'aide les personnes dans le besoin.",
    "Je mets les croyants au défi de confronter et de se détourner de « leurs péchés, même face au rejet, à la pression ou aux accusations d'avoir un esprit étroit.",
    "J'ai tellement les gens à cœur que j'aime avancer dans la vie avec un petit groupe de croyants, tout en les guidant.",
    "J'ai le désir et la capacité de relier la vérité de Dieu à la vie de façon à ce que les chrétiens développent des attitudes et des valeurs saines.",
    "Je peux voir l'image globale et formuler un plan détaillé pour l'accomplir.",
    "Je peux être en désaccord avec des gens sans qu'ils se sentent jugés ou rejetés et je maintiens une relation d'aide saine.",
    "Je peux prendre du matériel de base et en façonner des objets désirés.",
    "Indépendamment de ce que je fais, j'ai l'impression que j'aurais pu faire mieux.",
    "J'aime motiver les autres à prendre leur cheminement spirituel plus au sérieux.",
    "Après avoir conduit les gens à Christ, je les guide aussi vers des opportunités de devenir des disciples.",
    "Je suis comblé(e) de savoir que mon support financier fait une différence significative dans les vies et les ministères du peuple de Dieu.",
    "J'aime encourager les autres en servant quand et où il y a un besoin.",
    "Je fais ce que je peux pour aider les nouveaux à se sentir chez eux.",
    "Les groupes que j'ai conduits ont grandi et ont senti la présence de Dieu, même au milieu de circonstances difficiles.",
    "Je ressens tellement de compassion pour les gens dans la souffrance que je fais tout ce que je peux pour alléger leur fardeau et les soulager.",
    "Je suis prêt à souffrir personnellement ou à ce que les autres souffrent si ceci va produire une marche plus obéissante et plus fidèle avec Dieu.",
    "Les autres m'ont dit combien ils ont apprécié mon intérêt pour eux et mon soutien à long terme.",
    "Les gens disent qu'ils apprennent beaucoup quand j'enseigne la Bible et ils semblent motivés à l'étudier davantage par eux-mêmes."
]

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('admin'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def hello_world():
    return render_template("accueil.html"), 200

@app.route('/formulaire_info')
def formulaire_info():
    return render_template("formulaire_information.html"), 200

@app.route('/formulaire_test')
def formulaire_test():
    return render_template("formulaire_test.html", questions=QUESTIONS_FIXES), 200

@app.route('/formulaire_don')
def formulaire_don():
    return render_template("formulaire_don.html", don_questions=don_questions), 200

@app.route('/soumettre', methods=['POST'])
def soumettre():
    email_manager_object = email_manager.EmailManager()
    form_data = request.form.to_dict()
    
    # Process the personality assessment
    print(form_data)
    results = process_form_data(form_data)
    form_data["personality_scores"] = results["scores"]
    form_data["personality_type"] = results["personality_type"]

    results_don = process_don_form_data(form_data)
    form_data["don_scores"] = results_don["don_scores"]
    form_data["dons"] = results_don["dons"]
    form_data["dons_grand"] = results_don["dons_grand"]
    
    recipient = request.form.get("courriel")
    personality = results["personality_type"]
    email_manager_object.send_email(form_data=form_data)
    return redirect(url_for("confirmation",
                          email_utilisateur=recipient,
                          personality=personality), code=302)

@app.route('/confirmation')
def confirmation():
    email_utilisateur = request.args.get("email_utilisateur")
    personality = request.args.get("personality")
    return render_template("email_confirmation.html", email_utilisateur=email_utilisateur, personality=personality), 200

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        password = request.form.get('password')
        if db.check_password(password):
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            flash('Mot de passe incorrect', 'error')
            return render_template('admin.html')
        
    if not session.get('logged_in'):
        return render_template('admin.html')

    all_roles = db.get_all_roles_with_don()
    regions = db.get_regions()
    dons = db.get_all_dons() 

    # Organize roles by region and don
    roles_by_region = []
    for region in regions:
        region_data = {
            'id': region['id'],
            'name': region['nom'],
            'dons': []
        }
        for don in dons:
            don_roles = [
                role for role in all_roles
                if role['region'] == region['nom'] and role['don_code'] == don['code']
            ]
            don_data = {
                'id': don['id'],
                'code': don['code'],
                'nom': don['nom'],
                'description': don['description'],
                'roles': don_roles
            }
            region_data['dons'].append(don_data)
        roles_by_region.append(region_data)

    return render_template('admin.html', roles_by_region=roles_by_region)

@app.route('/admin/login', methods=['POST'])
def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if db.verifier_utilisateur(username, password):
        session['logged_in'] = True
        return redirect(url_for('admin'))
    else:
        return render_template('admin.html', error="Nom d'utilisateur ou mot de passe incorrect")

@app.route('/admin/add_role', methods=['POST'])
@login_required
def add_role():
    role_name = request.form.get('role_name')
    region_id = request.form.get('region_id')
    don_id = request.form.get('don_id')
    if role_name and region_id and don_id:
        db.add_role(role_name, region_id, don_id)
        flash('Équipe ajoutée avec succès', 'success')
    else:
        flash('Erreur lors de l\'ajout de l\'équipe', 'error')
    return redirect(url_for('admin'))

@app.route('/admin/delete_role', methods=['POST'])
@login_required
def delete_role():
    role_id = request.form.get('role_id')
    if role_id and db.delete_role(role_id):
        flash('Équipe supprimée avec succès', 'success')
    else:
        flash('Erreur lors de la suppression de l\'équipe', 'error')
    return redirect(url_for('admin'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == '__main__':
    app.run(debug=True)
