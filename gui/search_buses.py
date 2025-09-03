import tkinter as tk
from tkinter import messagebox
from database.db import connect_db
from gui import book_ticket

def search_buses(user_id):  # Accept user_id
    root = tk.Toplevel()
    root.title("Search Buses")
    root.geometry("350x250")

    tk.Label(root, text="Source").pack(pady=5)
    entry_source = tk.Entry(root)
    entry_source.pack(pady=5)

    tk.Label(root, text="Destination").pack(pady=5)
    entry_destination = tk.Entry(root)
    entry_destination.pack(pady=5)

    tk.Label(root, text="Date (YYYY-MM-DD)").pack(pady=5)
    entry_date = tk.Entry(root)
    entry_date.pack(pady=5)

    def perform_search():
        source = entry_source.get()
        destination = entry_destination.get()
        date = entry_date.get()

        if not source or not destination or not date:
            messagebox.showerror("Error", "Please fill all fields")
            return

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM buses WHERE source=? AND destination=? AND date=?
        """, (source, destination, date))
        buses = cursor.fetchall()
        conn.close()

        result_window = tk.Toplevel(root)
        result_window.title("Available Buses")
        result_window.geometry("500x400")

        if not buses:
            tk.Label(result_window, text="No buses found").pack(pady=10)
            return

        for bus in buses:
            bus_info = f"ID:{bus[0]} {bus[1]} {bus[2]}→{bus[3]}, Time:{bus[5]}, Seats:{bus[6]}, Price:{bus[7]}"
            tk.Label(result_window, text=bus_info).pack(pady=2)
            tk.Button(result_window, text="Book", command=lambda b=bus: book_ticket.launch_booking(b, user_id)).pack(pady=2)

    tk.Button(root, text="Search", command=perform_search).pack(pady=10)
