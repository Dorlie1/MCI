import sqlite3
import hashlib
import os

def check_and_update_password():
    # Get database path
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.db')
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get current password hash
    cursor.execute("SELECT mot_de_passe FROM utilisateur WHERE id = 1")
    current = cursor.fetchone()
    
    if current:
        print(f"Current password hash in database: {current[0]}")
    else:
        print("No admin user found in database!")
        return
    
    # Calculate correct hash for 'Vision1!'
    correct_password = "Vision1!"
    correct_hash = hashlib.sha256(correct_password.encode()).hexdigest()
    print(f"Correct hash should be: {correct_hash}")
    
    # Update if different
    if current[0] != correct_hash:
        print("Updating password hash...")
        cursor.execute("UPDATE utilisateur SET mot_de_passe = ? WHERE id = 1", (correct_hash,))
        conn.commit()
        print("Password hash updated!")
    else:
        print("Password hash is correct!")
    
    conn.close()

if __name__ == '__main__':
    check_and_update_password() 