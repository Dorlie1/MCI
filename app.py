from flask import (Flask, render_template, redirect, url_for, request, session, flash)
import email_manager
from calculs import process_form_data
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

@app.route('/soumettre', methods=['POST'])
def soumettre():
    email_manager_object = email_manager.EmailManager()
    form_data = request.form.to_dict()
    
    # Process the personality assessment
    results = process_form_data(form_data)
    form_data["personality_scores"] = results["scores"]
    form_data["personality_type"] = results["personality_type"]
    
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

@app.route('/admin', methods=['GET'])
def admin():
    if not session.get('logged_in'):
        return render_template('admin.html')
    
    # Récupérer tous les rôles et les organiser par région et trait
    all_roles = db.get_all_roles()
    regions = db.get_regions()
    traits = db.get_traits()
    
    # Organiser les données pour l'affichage
    roles_by_region = []
    for region in regions:
        region_data = {
            'id': region['id'],
            'name': region['nom'],
            'traits': []
        }
        
        for trait in traits:
            trait_roles = [
                role for role in all_roles 
                if role['region'] == region['nom'] and role['trait'] == trait['code']
            ]
            
            trait_data = {
                'id': trait['id'],
                'code': trait['code'],
                'description': trait['description'],
                'roles': trait_roles
            }
            region_data['traits'].append(trait_data)
        
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
    trait_id = request.form.get('trait_id')
    
    if role_name and region_id and trait_id:
        db.add_role(role_name, region_id, trait_id)
        flash('Rôle ajouté avec succès', 'success')
    else:
        flash('Erreur lors de l\'ajout du rôle', 'error')
    
    return redirect(url_for('admin'))

@app.route('/admin/delete_role', methods=['POST'])
@login_required
def delete_role():
    role_id = request.form.get('role_id')
    
    if role_id and db.delete_role(role_id):
        flash('Rôle supprimé avec succès', 'success')
    else:
        flash('Erreur lors de la suppression du rôle', 'error')
    
    return redirect(url_for('admin'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == '__main__':
    app.run(debug=True)
