import sqlite3
import os

def init_db():
    # Get the directory containing this script
    db_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create db directory if it doesn't exist
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
    
    # Connect to database (this will create it if it doesn't exist)
    db_path = os.path.join(db_dir, 'db.db')
    conn = sqlite3.connect(db_path)
    
    try:
        # Read the SQL script
        with open(os.path.join(db_dir, 'db.sql'), 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # Execute the SQL script
        conn.executescript(sql_script)
        
        # Commit the changes
        conn.commit()
        print("Database initialized successfully!")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    init_db() 