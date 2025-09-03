import tkinter as tk
from tkinter import messagebox
from database import bookings, buses
from gui.ticket_receipt import TicketReceipt

class BookTicket:
    def __init__(self, root, bus):
        self.root = root
        self.bus = bus
        self.root.title("Book Ticket")
        self.root.geometry("300x300")

        tk.Label(root, text=f"Booking for {bus[1]}").pack(pady=10)

        tk.Label(root, text="Passenger Name:").pack()
        self.name = tk.Entry(root)
        self.name.pack()

        tk.Label(root, text="Age:").pack()
        self.age = tk.Entry(root)
        self.age.pack()

        tk.Label(root, text="Seat Number:").pack()
        self.seat = tk.Entry(root)
        self.seat.pack()

        tk.Button(root, text="Confirm Booking", command=self.book).pack(pady=10)

    def book(self):
        passenger = self.name.get()
        age = self.age.get()
        seat = self.seat.get()

        if not passenger or not age.isdigit() or not seat.isdigit():
            messagebox.showerror("Error", "Invalid details!")
            return

        seat_num = int(seat)
        if seat_num > self.bus[4]:  # total seats check
            messagebox.showerror("Error", "Invalid seat number")
            return

        ticket = bookings.book_ticket(self.bus[0], passenger, int(age), seat_num)
        if ticket:
            win = tk.Toplevel(self.root)
            TicketReceipt(win, ticket)
            self.root.destroy()
        else:
            messagebox.showerror("Error", "Seat already booked or unavailable!")
