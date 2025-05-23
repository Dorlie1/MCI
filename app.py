from flask import (Flask, render_template, redirect, url_for, request)
import email_manager

app = Flask(__name__)

QUESTIONS_FIXES = [
    "Je suis confiant, exigeant et décidé",
    "J’aime accomplir plusieurs tâches à la fois",
    "Je me sens bien dans un environnement rempli de défis",
    "Je pense plus aux tâches, qu’aux autres ou à moi-même",
    "Je suis motivé par l’accomplissement et l’autorité",
    "J’aime influencer et inspirer d’autres personnes",
    "Je suis optimiste au sujet des autres",
    "J’ai tendance à être celui qui retient l’attention",
    "Je pense à motiver les gens",
    "Je suis motivé par la reconnaissance et l’approbation",
    "Je me développe bien dans un environnement stable",
    "Je préfère des consignes précises plus que des consignes générales",
    "J’aime les petits groupes de personnes",
    "Je préfère être un membre dans une équipe",
    "Je suis motivé par la stabilité et le soutien",
    "Je ne suis pas porté à prendre de grands risques",
    "J’aime les tâches, l’ordre et les détails",
    "La plupart du temps, j’ai raison",
    "Je me soumets à des règles clairement définies",
    "Je suis motivé par la qualité et l’exactitude"
]


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
    ##form_data = request.form.to_dict()
    ##form_data["prix"]=str(calculs(request))
    ##form_data["prix"]="Le prix décidé en personne"
    recipient = request.form.get("courriel")
    ##email_manager_object.send_email(form_data=form_data)
    return redirect(url_for("confirmation",
                            email_utilisateur=recipient), code=302)

@app.route('/confirmation')
def confirmation():
    email_utilisateur = request.args.get("email_utilisateur")
    return render_template("email_confirmation.html", email_utilisateur=email_utilisateur), 200

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == '__main__':
    app.run()
