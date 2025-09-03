import tkinter as tk
from tkinter import messagebox, simpledialog
from database.db import connect_db

def cancel_booking(user_id):
    booking_id = simpledialog.askinteger("Cancel Booking", "Enter Booking ID to cancel:")
    if booking_id is None:
        return

    conn = connect_db()
    cursor = conn.cursor()

    # Get booking details
    cursor.execute("SELECT bus_id, seats FROM bookings WHERE id=? AND user_id=?", (booking_id, user_id))
    booking = cursor.fetchone()
    if not booking:
        messagebox.showerror("Error", "Booking not found")
        conn.close()
        return

    bus_id, seats_booked = booking
    seats_booked = int(seats_booked)

    # Delete booking
    cursor.execute("DELETE FROM bookings WHERE id=?", (booking_id,))
    # Update bus seats
    cursor.execute("UPDATE buses SET seats = seats + ? WHERE id=?", (seats_booked, bus_id))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", f"Booking {booking_id} cancelled successfully!")
