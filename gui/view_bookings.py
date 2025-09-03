import tkinter as tk
from tkinter import messagebox
from database.db import connect_db

def view_bookings(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT b.id, bs.name, bs.source, bs.destination, bs.date, bs.time, b.seats
        FROM bookings b
        JOIN buses bs ON b.bus_id = bs.id
        WHERE b.user_id=?
    """, (user_id,))
    bookings = cursor.fetchall()
    conn.close()

    booking_window = tk.Toplevel()
    booking_window.title("My Bookings")
    booking_window.geometry("500x400")

    if not bookings:
        tk.Label(booking_window, text="No bookings found").pack(pady=10)
        return

    for booking in bookings:
        booking_info = f"Booking ID:{booking[0]} Bus:{booking[1]} {booking[2]}→{booking[3]}, Date:{booking[4]}, Time:{booking[5]}, Seats:{booking[6]}"
        tk.Label(booking_window, text=booking_info).pack(pady=2)
