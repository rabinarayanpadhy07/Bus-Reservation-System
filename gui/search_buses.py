import tkinter as tk
from tkinter import messagebox
from database import buses
from gui.book_ticket import BookTicket

class SearchBuses:
    def __init__(self, root):
        self.root = root
        self.root.title("Search Buses")
        self.root.geometry("400x300")

        tk.Label(root, text="Source:").pack()
        self.source = tk.Entry(root)
        self.source.pack()

        tk.Label(root, text="Destination:").pack()
        self.destination = tk.Entry(root)
        self.destination.pack()

        tk.Button(root, text="Search", command=self.search).pack(pady=10)

    def search(self):
        src = self.source.get()
        dest = self.destination.get()

        if not src or not dest:
            messagebox.showerror("Error", "Please enter both source and destination")
            return

        results = buses.search_buses(src, dest)

        win = tk.Toplevel(self.root)
        win.title("Available Buses")
        win.geometry("500x300")

        if results:
            for bus in results:
                btn = tk.Button(win, text=f"{bus[1]} ({bus[5]} seats left)", 
                                command=lambda b=bus: self.book_ticket(b))
                btn.pack(pady=5)
        else:
            tk.Label(win, text="No buses found").pack(pady=20)

    def book_ticket(self, bus):
        win = tk.Toplevel(self.root)
        BookTicket(win, bus)
