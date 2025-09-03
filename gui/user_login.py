import tkinter as tk
from tkinter import messagebox
from database.users import create_user_table, register_user, login_user

def login_window():
    root = tk.Tk()
    root.title("Login / Signup")

    tk.Label(root, text="Username").grid(row=0, column=0)
    tk.Label(root, text="Password").grid(row=1, column=0)

    username_entry = tk.Entry(root)
    password_entry = tk.Entry(root, show="*")
    username_entry.grid(row=0, column=1)
    password_entry.grid(row=1, column=1)

    def handle_login():
        username = username_entry.get()
        password = password_entry.get()
        user = login_user(username, password)
        if user:
            messagebox.showinfo("Success", f"Welcome {username}")
            root.destroy()
            open_dashboard(username)  # 🚀 Go to dashboard
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def handle_signup():
        username = username_entry.get()
        password = password_entry.get()
        if register_user(username, password):
            messagebox.showinfo("Success", "Account created! Please login.")
        else:
            messagebox.showerror("Error", "Username already exists")

    tk.Button(root, text="Login", command=handle_login).grid(row=2, column=0)
    tk.Button(root, text="Signup", command=handle_signup).grid(row=2, column=1)

    root.mainloop()

def open_dashboard(username):
    dash = tk.Tk()
    dash.title(f"Dashboard - {username}")
    tk.Label(dash, text=f"Welcome, {username}").pack()
    dash.mainloop()

if __name__ == "__main__":
    create_user_table()
    login_window()
