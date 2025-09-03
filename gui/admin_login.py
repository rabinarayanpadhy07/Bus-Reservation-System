import tkinter as tk
from tkinter import messagebox
from gui import admin_dashboard  # Correct package import

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

def main(root):  # now accepts root
    admin_window = tk.Toplevel(root)
    admin_window.title("Admin Login")
    admin_window.geometry("300x200")

    def login_admin():
        username = entry_username.get()
        password = entry_password.get()

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            messagebox.showinfo("Login Success", "Welcome Admin!")
            admin_window.destroy()
            admin_dashboard.launch_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")

    tk.Label(admin_window, text="Admin Username").pack(pady=5)
    entry_username = tk.Entry(admin_window)
    entry_username.pack(pady=5)

    tk.Label(admin_window, text="Admin Password").pack(pady=5)
    entry_password = tk.Entry(admin_window, show="*")
    entry_password.pack(pady=5)

    tk.Button(admin_window, text="Login", command=login_admin).pack(pady=10)
