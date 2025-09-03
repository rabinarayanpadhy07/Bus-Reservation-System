from gui.home import Home
from database.db import create_tables
import tkinter as tk

def main():
    create_tables()  # Ensure DB is ready
    root = tk.Tk()
    app = Home(root)
    root.mainloop()

if __name__ == "__main__":
    main()
