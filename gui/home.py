import tkinter as tk
from tkinter import messagebox
from gui.admin_login import AdminLogin
from gui.user_dashboard import UserDashboard

class Home:
    def __init__(self, root):
        self.root = root
        self.root.title("Bus Reservation System")
        self.root.geometry("400x300")

        tk.Label(root, text="Bus Reservation System", font=("Arial", 16, "bold")).pack(pady=20)

        tk.Button(root, text="Admin Login", width=20, command=self.open_admin).pack(pady=10)
        tk.Button(root, text="User Dashboard", width=20, command=self.open_user).pack(pady=10)

    def open_admin(self):
        win = tk.Toplevel(self.root)
        AdminLogin(win)

    def open_user(self):
        win = tk.Toplevel(self.root)
        UserDashboard(win)
