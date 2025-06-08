import sqlite3
import hashlib
import os

class Database:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.db')

    def get_connection(self):
        # Create a new connection for each request
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def verifier_utilisateur(self, nom, mot_de_passe):
        connection = self.get_connection()
        try:
            cursor = connection.cursor()
            # Hachage du mot de passe entré
            mot_de_passe_hache = hashlib.sha256(mot_de_passe.encode()).hexdigest()
            print(f"Mot de passe haché entré: {mot_de_passe_hache}")

            # Requête pour récupérer l'utilisateur unique
            cursor.execute("SELECT mot_de_passe FROM utilisateur WHERE id = 1 AND nom = ?", (nom,))
            resultat = cursor.fetchone()
            
            if resultat:
                print(f"Mot de passe haché dans la base: {resultat[0]}")
            else:
                print("Aucun utilisateur trouvé avec ce nom")

            # Vérifie si un utilisateur a été trouvé et compare les mots de passe hachés
            if resultat and resultat[0] == mot_de_passe_hache:
                return True
            return False
        finally:
            connection.close()

    def get_all_roles(self):
        connection = self.get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT r.id, r.nom, reg.nom as region, t.code as trait, t.description as trait_description
                FROM roles r
                JOIN regions reg ON r.region_id = reg.id
                JOIN traits t ON r.trait_id = t.id
                ORDER BY reg.nom, t.code, r.nom
            """)
            return cursor.fetchall()
        finally:
            connection.close()

    def add_role(self, nom, region_id, don_id):
        connection = self.get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO roles (nom, region_id, don_id)
                VALUES (?, ?, ?)
            """, (nom, region_id, don_id))
            connection.commit()
            return cursor.lastrowid
        finally:
            connection.close()

    def delete_role(self, role_id):
        connection = self.get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM roles WHERE id = ?", (role_id,))
            connection.commit()
            return cursor.rowcount > 0
        finally:
            connection.close()

    def get_regions(self):
        connection = self.get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM regions ORDER BY nom")
            return cursor.fetchall()
        finally:
            connection.close()

    def get_traits(self):
        connection = self.get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM traits ORDER BY code")
            return cursor.fetchall()
        finally:
            connection.close()

    def get_all_roles_with_don(self):
        connection = self.get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT r.id, r.nom, reg.nom as region, d.code as don_code, d.nom as don_name
                FROM roles r
                JOIN regions reg ON r.region_id = reg.id
                JOIN dons d ON r.don_id = d.id
                ORDER BY reg.nom, d.code, r.nom
            """)
            return cursor.fetchall()
        finally:
            connection.close()

    def get_don_descriptions(self, dons):
        """
        dons: list of don codes, e.g. ['A', 'B']
        Returns: list of (nom, description) for each don
        """
        connection = self.get_connection()
        try:
            cursor = connection.cursor()
            # Use tuple for SQL IN clause
            placeholders = ','.join('?' for _ in dons)
            cursor.execute(f"SELECT nom, description FROM dons WHERE code IN ({placeholders})", dons)
            return cursor.fetchall()
        finally:
            connection.close()

    def get_all_dons(self):
        connection = self.get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM dons ORDER BY code")
            return cursor.fetchall()
        finally:
            connection.close()

    def get_don_code_to_name(self):
        connection = self.get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT code, nom FROM dons")
            return {row[0]: row[1] for row in cursor.fetchall()}
        finally:
            connection.close()