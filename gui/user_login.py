import tkinter as tk
from tkinter import messagebox
from database.db import connect_db
from gui.user_dashboard import launch_dashboard

def main(root):  # now accepts root
    user_window = tk.Toplevel(root)
    user_window.title("User Login")
    user_window.geometry("300x200")

    def login_user():
        email = entry_email.get()
        password = entry_password.get()

        if not email or not password:
            messagebox.showerror("Error", "Please enter email and password")
            return

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            messagebox.showinfo("Login Success", f"Welcome {user[1]}!")
            user_window.destroy()
            launch_dashboard(user[0])
        else:
            messagebox.showerror("Login Failed", "Invalid email or password")

    tk.Label(user_window, text="Email").pack(pady=5)
    entry_email = tk.Entry(user_window)
    entry_email.pack(pady=5)

    tk.Label(user_window, text="Password").pack(pady=5)
    entry_password = tk.Entry(user_window, show="*")
    entry_password.pack(pady=5)

    tk.Button(user_window, text="Login", width=20, command=login_user).pack(pady=10)
