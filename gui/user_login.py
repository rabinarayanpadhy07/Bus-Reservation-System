import tkinter as tk
from tkinter import messagebox
from database.db import connect_db
from gui.user_dashboard import launch_dashboard  # Import user dashboard

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
        root.destroy()  # Close login window
        launch_dashboard(user[0])  # Launch dashboard with user_id
    else:
        messagebox.showerror("Login Failed", "Invalid email or password")

# ---------------- GUI ----------------
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
