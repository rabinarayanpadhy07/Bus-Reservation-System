import sqlite3
from database.db import connect_db

def add_sample_data():
    conn = connect_db()
    cursor = conn.cursor()

    # Sample admin credentials (hardcoded)
    admin_username = "admin"
    admin_password = "admin123"

    # For users table: sample user
    cursor.execute("""
    INSERT OR IGNORE INTO users (name, age, email, phone, password)
    VALUES (?, ?, ?, ?, ?)
    """, ("Test User", 25, "testuser@example.com", "1234567890", "user123"))

    # For buses table: sample bus
    cursor.execute("""
    INSERT OR IGNORE INTO buses (name, source, destination, date, time, seats, price)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, ("Express Line", "City A", "City B", "2025-09-10", "10:00", 40, 500))
    
    conn.commit()
    conn.close()
    print("Sample data added successfully!")

if __name__ == "__main__":
    add_sample_data()
