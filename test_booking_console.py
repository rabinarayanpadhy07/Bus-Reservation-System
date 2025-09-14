# test_booking_console.py

from modules import booking
from database.db_connection import get_connection

# Parameters
user_id = 1       # replace with an existing user id from Users table
bus_id = 1        # replace with an existing bus id from Buses table
seats_to_book = 2 # number of seats to book

print("🔹 Starting booking test...")

# 1️⃣ Attempt booking
success, msg = booking.book_seats(user_id, bus_id, seats_to_book)
print("Booking attempt:", msg)

# 2️⃣ Check bus availability after booking
conn = get_connection()
cursor = conn.cursor()
cursor.execute("SELECT id, name, available_seats FROM Buses WHERE id = ?", (bus_id,))
bus = cursor.fetchone()
print("Bus availability after booking:", bus)

# 3️⃣ Check bookings table for this bus
cursor.execute("SELECT id, user_id, bus_id, seats_booked FROM Bookings WHERE bus_id = ?", (bus_id,))
bookings = cursor.fetchall()
print("Bookings for this bus:", bookings)

conn.close()
print("✅ Test finished.")
