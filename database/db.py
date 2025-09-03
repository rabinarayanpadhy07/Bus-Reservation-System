import sqlite3

DB_NAME = "bus_reservation.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Bus table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS buses (
        bus_id INTEGER PRIMARY KEY AUTOINCREMENT,
        bus_name TEXT NOT NULL,
        source TEXT NOT NULL,
        destination TEXT NOT NULL,
        total_seats INTEGER NOT NULL,
        available_seats INTEGER NOT NULL
    )
    """)

    # Booking table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
        bus_id INTEGER,
        passenger_name TEXT NOT NULL,
        age INTEGER NOT NULL,
        seat_number INTEGER NOT NULL,
        FOREIGN KEY(bus_id) REFERENCES buses(bus_id)
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    print("✅ Tables created successfully!")
