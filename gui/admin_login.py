import tkinter as tk
from tkinter import messagebox

# Hardcoded admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

def login_admin():
    username = entry_username.get()
    password = entry_password.get()

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        messagebox.showinfo("Login Success", "Welcome Admin!")
        root.destroy()  # close login window
        import admin_dashboard  # open dashboard
    else:
        messagebox.showerror("Login Failed", "Invalid credentials")

root = tk.Tk()
root.title("Admin Login")
root.geometry("300x200")

tk.Label(root, text="Admin Username").pack(pady=5)
entry_username = tk.Entry(root)
entry_username.pack(pady=5)

tk.Label(root, text="Admin Password").pack(pady=5)
entry_password = tk.Entry(root, show="*")
entry_password.pack(pady=5)

tk.Button(root, text="Login", command=login_admin).pack(pady=10)

root.mainloop()
