import tkinter as tk
from tkinter import messagebox
from database import buses

class AdminDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Dashboard")
        self.root.geometry("400x300")

        tk.Label(root, text="Admin Dashboard", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Button(root, text="Add Bus", width=20, command=self.add_bus_window).pack(pady=5)
        tk.Button(root, text="View Buses", width=20, command=self.view_buses).pack(pady=5)

    def add_bus_window(self):
        win = tk.Toplevel(self.root)
        win.title("Add Bus")
        win.geometry("300x300")

        tk.Label(win, text="Bus Name:").pack()
        bus_name = tk.Entry(win)
        bus_name.pack()

        tk.Label(win, text="Source:").pack()
        source = tk.Entry(win)
        source.pack()

        tk.Label(win, text="Destination:").pack()
        destination = tk.Entry(win)
        destination.pack()

        tk.Label(win, text="Total Seats:").pack()
        seats = tk.Entry(win)
        seats.pack()

        def save_bus():
            if not (bus_name.get() and source.get() and destination.get() and seats.get().isdigit()):
                messagebox.showerror("Error", "Invalid input!")
                return
            buses.add_bus(bus_name.get(), source.get(), destination.get(), int(seats.get()))
            messagebox.showinfo("Success", "Bus Added Successfully!")
            win.destroy()

        tk.Button(win, text="Save", command=save_bus).pack(pady=10)

    def view_buses(self):
        bus_list = buses.get_all_buses()
        win = tk.Toplevel(self.root)
        win.title("All Buses")
        win.geometry("500x300")

        text = tk.Text(win)
        text.pack(fill=tk.BOTH, expand=True)

        if bus_list:
            for b in bus_list:
                text.insert(tk.END, f"ID: {b[0]}, Name: {b[1]}, From: {b[2]} To: {b[3]}, Seats: {b[4]}, Available: {b[5]}\n")
        else:
            text.insert(tk.END, "No buses found.")
