from database.db_connection import get_connection

def book_seats(user_id, bus_id, seats_to_book):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Check available seats
        cursor.execute("SELECT available_seats FROM Buses WHERE id = ?", (bus_id,))
        result = cursor.fetchone()
        if not result:
            return False, "Bus not found."
        available_seats = result[0]

        if available_seats < seats_to_book:
            return False, "Not enough seats available."

        # Insert booking
        cursor.execute("""
            INSERT INTO Bookings (user_id, bus_id, seats_booked)
            VALUES (?, ?, ?)
        """, (user_id, bus_id, seats_to_book))

        # Update available seats
        cursor.execute("""
            UPDATE Buses
            SET available_seats = available_seats - ?
            WHERE id = ?
        """, (seats_to_book, bus_id))

        conn.commit()
        return True, "Booking successful!"

    except Exception as e:
        conn.rollback()
        return False, str(e)

    finally:
        conn.close()


def get_user_bookings(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT b.id, bs.name, bs.source, bs.destination, bs.date, bs.time, b.seats_booked, b.booking_time
        FROM Bookings b
        JOIN Buses bs ON b.bus_id = bs.id
        WHERE b.user_id = ?
        ORDER BY b.booking_time DESC
    """, (user_id,))
    data = cursor.fetchall()
    conn.close()
    return data


def cancel_booking(booking_id, user_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Find booking
        cursor.execute("SELECT bus_id, seats_booked FROM Bookings WHERE id = ? AND user_id = ?", (booking_id, user_id))
        booking = cursor.fetchone()
        if not booking:
            return False, "Booking not found."

        bus_id, seats = booking

        # Delete booking
        cursor.execute("DELETE FROM Bookings WHERE id = ?", (booking_id,))

        # Restore seats
        cursor.execute("UPDATE Buses SET available_seats = available_seats + ? WHERE id = ?", (seats, bus_id))

        conn.commit()
        return True, "Booking cancelled successfully."

    except Exception as e:
        conn.rollback()
        return False, str(e)

    finally:
        conn.close()
