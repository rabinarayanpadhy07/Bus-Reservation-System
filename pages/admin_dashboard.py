import streamlit as st
from database.db_connection import get_connection
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Bus Reservation - Admin", page_icon="🚌", layout="wide")

# Sidebar Navigation
st.sidebar.title("⚙️ Admin Panel")
menu = st.sidebar.radio("Navigation", ["Dashboard", "Manage Buses", "Manage Users", "Reports"])

st.title("Admin Dashboard")

# ✅ Check if admin is logged in
if "admin_id" not in st.session_state or not st.session_state.admin_id:
    st.error("Access denied! Please login as admin first.")
    st.stop()

st.subheader(f"Welcome, {st.session_state.admin_name} 👋")

# ==============================
# DASHBOARD OVERVIEW
# ==============================
if menu == "Dashboard":
    st.info("📊 Overview: Bookings, Buses, Users summary will go here.")

# ==============================
# TAB 1: Manage Buses
# ==============================
elif menu == "Manage Buses":
    st.header("🚌 Bus Management")
    option = st.radio("Choose Action:", ["View Buses", "Add Bus", "Edit Bus", "Delete Bus"])

    conn = get_connection()
    cursor = conn.cursor()

    # --- View Buses ---
    if option == "View Buses":
        cursor.execute("SELECT * FROM Buses")
        buses = cursor.fetchall()
        if buses:
            df_buses = pd.DataFrame(
                buses,
                columns=["ID", "Name", "Source", "Destination", "Date", "Time", "Total Seats", "Available Seats"]
            )
            st.dataframe(df_buses)
        else:
            st.info("No buses available.")

    # --- Add Bus ---
    elif option == "Add Bus":
        with st.form("add_bus_form"):
            name = st.text_input("Bus Name")
            source = st.text_input("Source")
            destination = st.text_input("Destination")
            date = st.date_input("Date")
            time = st.time_input("Time")
            total_seats = st.number_input("Total Seats", min_value=1, value=40)
            submitted = st.form_submit_button("Add Bus")

            if submitted:
                cursor.execute(
                    """INSERT INTO Buses (name, source, destination, date, time, total_seats, available_seats)
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (name, source, destination, str(date), str(time), total_seats, total_seats),
                )
                conn.commit()
                st.success("✅ Bus added successfully!")

    # --- Edit Bus ---
    elif option == "Edit Bus":
        cursor.execute("SELECT id, name FROM Buses")
        buses = cursor.fetchall()
        bus_dict = {f"{bus[1]} (ID: {bus[0]})": bus[0] for bus in buses}

        if bus_dict:
            selected_bus = st.selectbox("Select Bus to Edit", list(bus_dict.keys()))
            bus_id = bus_dict[selected_bus]

            cursor.execute("SELECT * FROM Buses WHERE id=?", (bus_id,))
            bus = cursor.fetchone()

            if bus:
                with st.form("edit_bus_form"):
                    name = st.text_input("Bus Name", bus[1])
                    source = st.text_input("Source", bus[2])
                    destination = st.text_input("Destination", bus[3])
                    date = st.date_input("Date")
                    time = st.time_input("Time")
                    total_seats = st.number_input("Total Seats", min_value=1, value=bus[6])
                    available_seats = st.number_input("Available Seats", min_value=0, value=bus[7])
                    submitted = st.form_submit_button("Update Bus")

                    if submitted:
                        cursor.execute(
                            """UPDATE Buses SET name=?, source=?, destination=?, date=?, time=?, 
                               total_seats=?, available_seats=? WHERE id=?""",
                            (name, source, destination, str(date), str(time), total_seats, available_seats, bus_id),
                        )
                        conn.commit()
                        st.success("✅ Bus updated successfully!")
        else:
            st.warning("No buses available to edit.")

    # --- Delete Bus ---
    elif option == "Delete Bus":
        cursor.execute("SELECT id, name FROM Buses")
        buses = cursor.fetchall()
        bus_dict = {f"{bus[1]} (ID: {bus[0]})": bus[0] for bus in buses}

        if bus_dict:
            selected_bus = st.selectbox("Select Bus to Delete", list(bus_dict.keys()))
            bus_id = bus_dict[selected_bus]

            if st.button("Delete Bus"):
                cursor.execute("DELETE FROM Buses WHERE id=?", (bus_id,))
                conn.commit()
                st.success("❌ Bus deleted successfully!")
        else:
            st.warning("No buses available to delete.")

    conn.close()

# ==============================
# TAB 2: Manage Users
# ==============================
elif menu == "Manage Users":
    st.header("👥 User Management")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email FROM Users")
    users = cursor.fetchall()
    conn.close()

    if users:
        df_users = pd.DataFrame(users, columns=["ID", "Name", "Email"])
        st.dataframe(df_users)
    else:
        st.info("No users found.")

# ==============================
# TAB 3: Reports & Charts
# ==============================
elif menu == "Reports":
    st.header("Reports & Charts")
    conn = get_connection()
    cursor = conn.cursor()

    # --- Daily Bookings Report ---
    cursor.execute(
        """
        SELECT date, COUNT(*) as total_bookings
        FROM Bookings b
        JOIN Buses bs ON b.bus_id = bs.id
        GROUP BY date
        ORDER BY date
        """
    )
    daily_bookings = cursor.fetchall()

    if daily_bookings:
        df_bookings = pd.DataFrame(daily_bookings, columns=["Date", "Total Bookings"])
        st.subheader("📅 Daily Bookings Report")
        st.dataframe(df_bookings)

        # Plot bookings chart
        fig, ax = plt.subplots()
        ax.plot(df_bookings["Date"], df_bookings["Total Bookings"], marker="o")
        ax.set_xlabel("Date")
        ax.set_ylabel("Total Bookings")
        ax.set_title("Daily Bookings Trend")
        st.pyplot(fig)
    else:
        st.info("No booking data available yet.")

    # --- Seat Occupancy Report ---
    cursor.execute(
        """
        SELECT name, total_seats, (total_seats - available_seats) as booked_seats
        FROM Buses
        """
    )
    occupancy = cursor.fetchall()
    conn.close()

    if occupancy:
        df_occ = pd.DataFrame(occupancy, columns=["Bus Name", "Total Seats", "Booked Seats"])
        st.subheader("🪑 Seat Occupancy Report")
        st.dataframe(df_occ)

        # Plot occupancy chart
        fig, ax = plt.subplots()
        df_occ.set_index("Bus Name")[["Booked Seats", "Total Seats"]].plot(kind="bar", ax=ax)
        ax.set_ylabel("Seats")
        ax.set_title("Seat Occupancy per Bus")
        st.pyplot(fig)
    else:
        st.info("No buses or booking data available yet.")
