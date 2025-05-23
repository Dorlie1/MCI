import smtplib
import yaml

class EmailManager:
    def __init__(self):
        self.config_path="config.yaml"

    def load_config(self):
        with open(self.config_path, "r") as f:
            return yaml.safe_load(f)["email"]

    def send_email(self, form_data):
        config = self.load_config()
        smtpserver = smtplib.SMTP_SSL(config["smtp_server"], config["smtp_port"])
        smtpserver.ehlo()
        smtpserver.login(config["username"], config["password"])

        # Test send mail
        sent_from = config["username"]
        sent_to = config["recipient"]
        email_text = self.format_email_text(form_data)
        #smtpserver.sendmail(sent_from, sent_to, email_text)



    def format_email_text(form_data):
        text = "Merci pour votre achat chez Premium Design!\n Voici un reçu de votre achat:"
        name = str(form_data["nom"])