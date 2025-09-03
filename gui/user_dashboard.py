import tkinter as tk
from gui.search_buses import SearchBuses
from gui.cancel_ticket import CancelTicket

class UserDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("User Dashboard")
        self.root.geometry("400x300")

        tk.Label(root, text="User Dashboard", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Button(root, text="Search Buses", width=20, command=self.open_search).pack(pady=5)
        tk.Button(root, text="Cancel Ticket", width=20, command=self.open_cancel).pack(pady=5)

    def open_search(self):
        win = tk.Toplevel(self.root)
        SearchBuses(win)

    def open_cancel(self):
        win = tk.Toplevel(self.root)
        CancelTicket(win)
