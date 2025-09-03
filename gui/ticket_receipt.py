import tkinter as tk

class TicketReceipt:
    def __init__(self, root, ticket):
        self.root = root
        self.root.title("Ticket Receipt")
        self.root.geometry("400x300")

        tk.Label(root, text="🎟️ Ticket Receipt", font=("Arial", 16, "bold")).pack(pady=10)

        details = f"""
Booking ID: {ticket['booking_id']}
Passenger: {ticket['passenger_name']} (Age: {ticket['age']})
Bus: {ticket['bus_name']}
Route: {ticket['source']} → {ticket['destination']}
Seat Number: {ticket['seat_number']}
        """

        tk.Label(root, text=details, justify="left", font=("Arial", 12)).pack(pady=10)

        tk.Button(root, text="Close", command=root.destroy).pack(pady=10)
