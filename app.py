from flask import (Flask, render_template, redirect, url_for, request)
import email_manager

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("formulaire_code.html"), 200

pp.route('/soumettre', methods=['POST'])
def soumettre():
    email_manager_object = email_manager.EmailManager()
    form_data = request.form.to_dict()
    ##form_data["prix"]=str(calculs(request))
    form_data["prix"]="Le prix décidé en personne"
    recipient = request.form.get("courriel")
    email_manager_object.send_email(form_data=form_data)
    return redirect(url_for("confirmation",
                            user_email=recipient), code=302)

@app.route('/confirmation')
def confirmation():
    user_email = request.args.get("user_email")
    return render_template("email_confirmation.html",
                           user_email = user_email), 200

if __name__ == '__main__':
    app.run()
