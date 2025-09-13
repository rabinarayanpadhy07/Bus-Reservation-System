import streamlit as st
from database.db_connection import get_connection
from datetime import date

st.title("User Dashboard")

# Check if user is logged in
if "user_id" not in st.session_state or not st.session_state.user_id:
    st.error("Access denied! Please login first.")
    st.stop()

st.subheader(f"Welcome, {st.session_state.user_name} 👋")

# --- Bus Search Filters ---
st.header("Search Available Buses")

conn = get_connection()
cursor = conn.cursor()

# --- Filter Inputs ---
source = st.text_input("Source")
destination = st.text_input("Destination")
travel_date = st.date_input("Travel Date", min_value=date.today())
search = st.button("Search Buses")

# --- Display Buses ---
if search:
    query = "SELECT id, name, source, destination, date, time, available_seats FROM Buses WHERE 1=1"
    params = []

    if source:
        query += " AND source LIKE ?"
        params.append(f"%{source}%")
    if destination:
        query += " AND destination LIKE ?"
        params.append(f"%{destination}%")
    if travel_date:
        query += " AND date = ?"
        params.append(str(travel_date))

    cursor.execute(query, tuple(params))
    buses = cursor.fetchall()

    if buses:
        st.subheader("Available Buses")
        for bus in buses:
            bus_id, name, src, dest, b_date, b_time, seats = bus
            st.markdown(f"**{name}** | {src} → {dest} | Date: {b_date} | Time: {b_time} | Seats Available: {seats}")
            # Button for booking (optional for now)
            if seats > 0:
                if st.button(f"Book {name}", key=bus_id):
                    st.success(f"Proceed to booking for {name}")
            else:
                st.warning("No seats available")
    else:
        st.info("No buses found matching your criteria.")

conn.close()
