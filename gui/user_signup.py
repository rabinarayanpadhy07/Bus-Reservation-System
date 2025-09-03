import tkinter as tk
from tkinter import messagebox
from database.db import connect_db

def main(root):  # now accepts root
    signup_window = tk.Toplevel(root)
    signup_window.title("User Signup")
    signup_window.geometry("300x350")

    def signup_user():
        name = entry_name.get()
        age = entry_age.get()
        email = entry_email.get()
        phone = entry_phone.get()
        password = entry_password.get()

        if not name or not age or not email or not password:
            messagebox.showerror("Error", "Please fill all required fields")
            return

        try:
            age = int(age)
        except ValueError:
            messagebox.showerror("Error", "Age must be a number")
            return

        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO users (name, age, email, phone, password)
                VALUES (?, ?, ?, ?, ?)
            """, (name, age, email, phone, password))
            conn.commit()
            messagebox.showinfo("Success", "User registered successfully!")
            signup_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    tk.Label(signup_window, text="Name").pack(pady=5)
    entry_name = tk.Entry(signup_window)
    entry_name.pack(pady=5)

    tk.Label(signup_window, text="Age").pack(pady=5)
    entry_age = tk.Entry(signup_window)
    entry_age.pack(pady=5)

    tk.Label(signup_window, text="Email").pack(pady=5)
    entry_email = tk.Entry(signup_window)
    entry_email.pack(pady=5)

    tk.Label(signup_window, text="Phone").pack(pady=5)
    entry_phone = tk.Entry(signup_window)
    entry_phone.pack(pady=5)

    tk.Label(signup_window, text="Password").pack(pady=5)
    entry_password = tk.Entry(signup_window, show="*")
    entry_password.pack(pady=5)

    tk.Button(signup_window, text="Signup", width=20, command=signup_user).pack(pady=10)
