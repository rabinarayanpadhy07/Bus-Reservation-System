import tkinter as tk
from gui import admin_login, user_login, user_signup

def open_admin_login():
    root.withdraw()  # hide main window
    admin_login.main()  # launch admin login
    root.deiconify()   # show main window again after admin login closes

def open_user_window():
    root.withdraw()  # hide main window
    user_window = tk.Toplevel(root)
    user_window.title("User Access")
    user_window.geometry("300x200")

    tk.Label(user_window, text="Choose an option:", font=("Arial", 14)).pack(pady=10)

    tk.Button(
        user_window,
        text="Login",
        width=20,
        command=lambda: user_window.destroy() or user_login.main()
    ).pack(pady=5)

    tk.Button(
        user_window,
        text="Signup",
        width=20,
        command=lambda: user_window.destroy() or user_signup.main()
    ).pack(pady=5)

    # When user window closes, show main window again
    user_window.protocol("WM_DELETE_WINDOW", lambda: (user_window.destroy(), root.deiconify()))

# ---------------- Main Window ----------------
root = tk.Tk()
root.title("Bus Reservation System")
root.geometry("300x200")

tk.Label(root, text="Welcome to Bus Reservation", font=("Arial", 14)).pack(pady=20)
tk.Button(root, text="Admin Login", width=20, command=open_admin_login).pack(pady=5)
tk.Button(root, text="User Login/Signup", width=20, command=open_user_window).pack(pady=5)

root.mainloop()
