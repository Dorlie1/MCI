import sqlite3
import hashlib

class Database:
    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect('db/db.db')
        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

    def verifier_utilisateur(self, nom, mot_de_passe):
        connection = self.get_connection()
        cursor = connection.cursor()

        # Hachage du mot de passe entré
        mot_de_passe_hache = hashlib.sha256(mot_de_passe.encode()).hexdigest()
        try:
            # Requête pour récupérer l'utilisateur unique
            cursor.execute("SELECT mot_de_passe FROM utilisateur WHERE id = 1 AND nom = ?", (nom,))
            resultat = cursor.fetchone()


            # Vérifie si un utilisateur a été trouvé et compare les mots de passe hachés
            if resultat and resultat[0] == mot_de_passe_hache:
                return True
            return False
        finally:
            cursor.close()
