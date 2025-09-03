import tkinter as tk
from tkinter import messagebox
from gui.admin_dashboard import AdminDashboard

class AdminLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Login")
        self.root.geometry("300x200")

        tk.Label(root, text="Admin Login", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(root, text="Username:").pack()
        self.username = tk.Entry(root)
        self.username.pack()

        tk.Label(root, text="Password:").pack()
        self.password = tk.Entry(root, show="*")
        self.password.pack()

        tk.Button(root, text="Login", command=self.login).pack(pady=10)

    def login(self):
        user = self.username.get()
        pwd = self.password.get()

        if user == "admin" and pwd == "admin123":   # Simple hardcoded login
            self.root.destroy()
            dash = tk.Tk()
            AdminDashboard(dash)
            dash.mainloop()
        else:
            messagebox.showerror("Error", "Invalid Credentials!")
