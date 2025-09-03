import tkinter as tk
from tkinter import messagebox

def add_bus():
    messagebox.showinfo("Feature", "Add Bus feature coming soon!")

def view_buses():
    messagebox.showinfo("Feature", "View Buses feature coming soon!")

def remove_bus():
    messagebox.showinfo("Feature", "Remove Bus feature coming soon!")

root = tk.Tk()
root.title("Admin Dashboard")
root.geometry("400x300")

tk.Label(root, text="Welcome Admin", font=("Arial", 16)).pack(pady=10)

tk.Button(root, text="Add Bus", width=20, command=add_bus).pack(pady=5)
tk.Button(root, text="View Buses", width=20, command=view_buses).pack(pady=5)
tk.Button(root, text="Remove Bus", width=20, command=remove_bus).pack(pady=5)

root.mainloop()
