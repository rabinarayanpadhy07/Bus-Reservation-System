import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
from database.db import connect_db

def launch_dashboard():
    root = tk.Tk()
    root.title("Admin Dashboard")
    root.geometry("400x400")

    tk.Label(root, text="Welcome Admin", font=("Arial", 16)).pack(pady=10)

    # Add Bus
    def add_bus():
        add_window = tk.Toplevel(root)
        add_window.title("Add Bus")
        add_window.geometry("300x400")

        fields = ["Bus Name", "Source", "Destination", "Date (YYYY-MM-DD)", "Time (HH:MM)", "Seats", "Price"]
        entries = {}

        for field in fields:
            tk.Label(add_window, text=field).pack(pady=2)
            entry = tk.Entry(add_window)
            entry.pack(pady=2)
            entries[field] = entry

        def save_bus():
            try:
                name = entries["Bus Name"].get()
                source = entries["Source"].get()
                destination = entries["Destination"].get()
                date = entries["Date (YYYY-MM-DD)"].get()
                time = entries["Time (HH:MM)"].get()
                seats = int(entries["Seats"].get())
                price = float(entries["Price"].get())

                if not (name and source and destination and date and time):
                    raise ValueError("All fields required")

                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO buses (name, source, destination, date, time, seats, price)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (name, source, destination, date, time, seats, price))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Bus added successfully!")
                add_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(add_window, text="Add Bus", command=save_bus).pack(pady=10)

    # View Buses
    def view_buses():
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM buses")
        buses = cursor.fetchall()
        conn.close()

        view_window = tk.Toplevel(root)
        view_window.title("All Buses")
        view_window.geometry("500x400")

        for bus in buses:
            tk.Label(view_window, text=f"ID:{bus[0]} {bus[1]} {bus[2]}→{bus[3]}, Date:{bus[4]}, Time:{bus[5]}, Seats:{bus[6]}, Price:{bus[7]}").pack(pady=2)

    # Remove Bus
    def remove_bus():
        bus_id = simpledialog.askinteger("Remove Bus", "Enter Bus ID to remove:")
        if bus_id is None:
            return
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM buses WHERE id=?", (bus_id,))
        if cursor.rowcount == 0:
            messagebox.showerror("Error", "Bus ID not found")
        else:
            messagebox.showinfo("Success", "Bus removed successfully!")
        conn.commit()
        conn.close()

    tk.Button(root, text="Add Bus", width=20, command=add_bus).pack(pady=5)
    tk.Button(root, text="View Buses", width=20, command=view_buses).pack(pady=5)
    tk.Button(root, text="Remove Bus", width=20, command=remove_bus).pack(pady=5)

    root.mainloop()
