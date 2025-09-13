from database.db_connection import get_connection

def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Execute all SQL commands from setup.sql
    with open("database/setup.sql", "r") as f:
        cursor.executescript(f.read())

    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == "__main__":
    initialize_db()
