import tkinter as tk
from gui import admin_login, user_login, user_signup


def open_admin_login():
    # Open Admin Login in a new window
    admin_login.main(root)


def open_user_window():
    # Create a popup for choosing login/signup
    user_window = tk.Toplevel(root)
    user_window.title("User Access")
    user_window.geometry("300x200")

    tk.Label(user_window, text="Choose an option:", font=("Arial", 14)).pack(pady=10)

    tk.Button(
        user_window,
        text="Login",
        width=20,
        command=lambda: (user_window.destroy(), user_login.main(root))
    ).pack(pady=5)

    tk.Button(
        user_window,
        text="Signup",
        width=20,
        command=lambda: (user_window.destroy(), user_signup.main(root))
    ).pack(pady=5)

    # Ensure when user window closes, we go back to root
    user_window.protocol("WM_DELETE_WINDOW", lambda: user_window.destroy())


# ---------------- Main Window ----------------
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Bus Reservation System")
    root.geometry("300x200")

    tk.Label(root, text="Welcome to Bus Reservation", font=("Arial", 14)).pack(pady=20)
    tk.Button(root, text="Admin Login", width=20, command=open_admin_login).pack(pady=5)
    tk.Button(root, text="User Login/Signup", width=20, command=open_user_window).pack(pady=5)

    root.mainloop()
