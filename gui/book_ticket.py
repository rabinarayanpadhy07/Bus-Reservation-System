import tkinter as tk
from tkinter import messagebox
from database.db import connect_db
from datetime import datetime

def launch_booking(bus, user_id):  # Accept user_id
    book_window = tk.Toplevel()
    book_window.title("Book Ticket")
    book_window.geometry("300x250")

    tk.Label(book_window, text=f"Bus: {bus[1]} {bus[2]}→{bus[3]}").pack(pady=5)
    tk.Label(book_window, text=f"Date: {bus[4]}, Time: {bus[5]}, Available Seats: {bus[6]}").pack(pady=5)
    tk.Label(book_window, text=f"Price per seat: {bus[7]}").pack(pady=5)

    tk.Label(book_window, text="Number of Seats").pack(pady=5)
    entry_seats = tk.Entry(book_window)
    entry_seats.pack(pady=5)

    def confirm_booking():
        try:
            seats_requested = int(entry_seats.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid number of seats")
            return

        if seats_requested > bus[6]:
            messagebox.showerror("Error", "Not enough seats available")
            return

        conn = connect_db()
        cursor = conn.cursor()

        # Save booking
        cursor.execute("""
            INSERT INTO bookings (user_id, bus_id, seats, booking_date)
            VALUES (?, ?, ?, ?)
        """, (user_id, bus[0], str(seats_requested), datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

        # Update bus seats
        cursor.execute("UPDATE buses SET seats=? WHERE id=?", (bus[6] - seats_requested, bus[0]))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", f"Booked {seats_requested} seats successfully!")
        book_window.destroy()

    tk.Button(book_window, text="Book Ticket", command=confirm_booking).pack(pady=10)
