from database.db import get_connection
import sqlite3  # Needed for search_buses if not already imported elsewhere

def book_ticket(bus_id, passenger_name, age, seat_number):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Check if seat already booked
        cursor.execute(
            "SELECT 1 FROM bookings WHERE bus_id = ? AND seat_number = ?",
            (bus_id, seat_number)
        )
        if cursor.fetchone():
            return None  # Seat already booked

        # Check available seats
        cursor.execute("SELECT available_seats FROM buses WHERE bus_id = ?", (bus_id,))
        available = cursor.fetchone()
        if not available or available[0] <= 0:
            return None  # No seats available

        # Book ticket
        cursor.execute(
            "INSERT INTO bookings (bus_id, passenger_name, age, seat_number) VALUES (?, ?, ?, ?)",
            (bus_id, passenger_name, age, seat_number)
        )
        booking_id = cursor.lastrowid

        # Decrease available seats
        cursor.execute(
            "UPDATE buses SET available_seats = available_seats - 1 WHERE bus_id = ?",
            (bus_id,)
        )

        # Fetch bus details for receipt
        cursor.execute(
            "SELECT bus_name, source, destination FROM buses WHERE bus_id = ?",
            (bus_id,)
        )
        bus = cursor.fetchone()

        conn.commit()

        return {
            "booking_id": booking_id,
            "passenger_name": passenger_name,
            "age": age,
            "seat_number": seat_number,
            "bus_name": bus[0],
            "source": bus[1],
            "destination": bus[2]
        }

    finally:
        conn.close()

def search_buses(query):
    conn = get_connection()  # Use consistent connection method
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT * FROM buses 
            WHERE bus_name LIKE ? OR source LIKE ? OR destination LIKE ?
        """, (f"%{query}%", f"%{query}%", f"%{query}%"))
        results = cursor.fetchall()
        return results
    finally:
        conn.close()