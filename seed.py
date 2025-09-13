from database.db_connection import get_connection
import bcrypt

conn = get_connection()
cursor = conn.cursor()

# Sample Admin (hashed password)
admin_password = bcrypt.hashpw("adminpass".encode(), bcrypt.gensalt())
cursor.execute("INSERT OR IGNORE INTO Admins (name, email, password) VALUES (?, ?, ?)",
               ("Admin One", "admin@example.com", admin_password))

# Sample Bus
cursor.execute("""INSERT OR IGNORE INTO Buses 
(name, source, destination, date, time, total_seats, available_seats) 
VALUES (?, ?, ?, ?, ?, ?, ?)""",
               ("Express 101", "CityA", "CityB", "2025-09-20", "10:00", 40, 40))

conn.commit()
conn.close()

print("Seed data inserted successfully!")
