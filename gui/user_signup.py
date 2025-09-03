import tkinter as tk
from tkinter import messagebox
from database.db import connect_db

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
        root.destroy()
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        conn.close()

root = tk.Tk()
root.title("User Signup")
root.geometry("300x350")

tk.Label(root, text="Name").pack(pady=5)
entry_name = tk.Entry(root)
entry_name.pack(pady=5)

tk.Label(root, text="Age").pack(pady=5)
entry_age = tk.Entry(root)
entry_age.pack(pady=5)

tk.Label(root, text="Email").pack(pady=5)
entry_email = tk.Entry(root)
entry_email.pack(pady=5)

tk.Label(root, text="Phone").pack(pady=5)
entry_phone = tk.Entry(root)
entry_phone.pack(pady=5)

tk.Label(root, text="Password").pack(pady=5)
entry_password = tk.Entry(root, show="*")
entry_password.pack(pady=5)

tk.Button(root, text="Signup", command=signup_user).pack(pady=10)

root.mainloop()
