import tkinter as tk
from tkinter import messagebox
from database import bookings

class CancelTicket:
    def __init__(self, root):
        self.root = root
        self.root.title("Cancel Ticket")
        self.root.geometry("300x200")

        tk.Label(root, text="Enter Booking ID:").pack(pady=10)
        self.booking_id = tk.Entry(root)
        self.booking_id.pack()

        tk.Button(root, text="Cancel Ticket", command=self.cancel).pack(pady=10)

    def cancel(self):
        bid = self.booking_id.get()
        if not bid.isdigit():
            messagebox.showerror("Error", "Invalid booking ID!")
            return

        success = bookings.cancel_ticket(int(bid))
        if success:
            messagebox.showinfo("Success", "Ticket cancelled successfully!")
            self.root.destroy()
        else:
            messagebox.showerror("Error", "Booking not found!")
