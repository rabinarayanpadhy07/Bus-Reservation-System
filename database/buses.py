from database.db import get_connection

def add_bus(bus_name, source, destination, total_seats):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO buses (bus_name, source, destination, total_seats, available_seats) VALUES (?, ?, ?, ?, ?)",
        (bus_name, source, destination, total_seats, total_seats)
    )
    conn.commit()
    conn.close()

def get_all_buses():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM buses")
    rows = cursor.fetchall()
    conn.close()
    return rows
def search_buses(source, destination):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM buses WHERE source=? AND destination=?", (source, destination))
    rows = cursor.fetchall()
    conn.close()
    return rows
