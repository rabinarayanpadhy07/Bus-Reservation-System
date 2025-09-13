import sqlite3

def get_connection():
    # This will create 'bus_reservation.db' if it doesn't exist
    conn = sqlite3.connect("database/bus_reservation.db")
    return conn
