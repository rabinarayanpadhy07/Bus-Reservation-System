import tkinter as tk
from tkinter import messagebox
from database.db import connect_db

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
        root.destroy()
        # user_dashboard.launch_dashboard()  # To be implemented in Day 5
    else:
        messagebox.showerror("Login Failed", "Invalid email or password")

root = tk.Tk()
root.title("User Login")
root.geometry("300x200")

tk.Label(root, text="Email").pack(pady=5)
entry_email = tk.Entry(root)
entry_email.pack(pady=5)

tk.Label(root, text="Password").pack(pady=5)
entry_password = tk.Entry(root, show="*")
entry_password.pack(pady=5)

tk.Button(root, text="Login", command=login_user).pack(pady=10)

root.mainloop()
