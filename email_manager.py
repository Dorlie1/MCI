from msal import ConfidentialClientApplication
import requests
import yaml

class EmailManager:
    def __init__(self, config_path="config.yaml"):
        self.config = self.load_config(config_path)
        self.token = self.authenticate()

    def load_config(self, path):
        with open(path, "r") as f:
            return yaml.safe_load(f)

    def authenticate(self):
        azure = self.config["azure"]
        app = ConfidentialClientApplication(
            client_id=azure["client_id"],
            authority=f"https://login.microsoftonline.com/{azure['tenant_id']}",
            client_credential=azure["client_secret"]
        )
        token_response = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
        if "access_token" not in token_response:
            raise Exception(f"Authentication failed: {token_response}")
        return token_response["access_token"]

    def send_email(self, subject, body_text, other_recipient):
        azure = self.config["azure"]
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        recipients = [
            {"emailAddress": {"address": azure["recipient_email"]}},
            {"emailAddress": {"address": other_recipient}}
        ]

        message = {
            "message": {
                "subject": subject,
                "body": {
                    "contentType": "Text",
                    "content": body_text
                },
                "toRecipients": recipients
            }
        }

        url = f"https://graph.microsoft.com/v1.0/users/{azure['sender_email']}/sendMail"
        response = requests.post(url, headers=headers, json=message)
        if response.status_code == 202:
            print("✅ Email sent successfully.")
        else:
            raise Exception(f"❌ Failed to send email: {response.status_code} - {response.text}")