import tkinter as tk
from gui import search_buses, view_bookings, cancel_booking

def launch_dashboard(user_id):
    root = tk.Tk()
    root.title("User Dashboard")
    root.geometry("400x400")

    tk.Label(root, text=f"Welcome User {user_id}", font=("Arial", 16)).pack(pady=10)

    tk.Button(root, text="Search Buses", width=20, command=lambda: search_buses.search_buses(user_id)).pack(pady=5)
    tk.Button(root, text="View My Bookings", width=20, command=lambda: view_bookings.view_bookings(user_id)).pack(pady=5)
    tk.Button(root, text="Cancel Booking", width=20, command=lambda: cancel_booking.cancel_booking(user_id)).pack(pady=5)

    root.mainloop()

