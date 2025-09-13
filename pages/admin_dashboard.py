import streamlit as st
from database.db_connection import get_connection

st.title("Admin Dashboard")

# ✅ Check if admin is logged in
if "admin_id" not in st.session_state or not st.session_state.admin_id:
    st.error("Access denied! Please login as admin first.")
    st.stop()

st.subheader(f"Welcome, {st.session_state.admin_name} 👋")

# --- Tabs for Bus Management and User Management ---
tab1, tab2 = st.tabs(["🚌 Manage Buses", "👤 Manage Users"])

# ==============================
# TAB 1: Manage Buses
# ==============================
with tab1:
    st.header("Bus Management")

    option = st.radio("Choose Action:", ["View Buses", "Add Bus", "Edit Bus", "Delete Bus"])

    conn = get_connection()
    cursor = conn.cursor()

    # --- View Buses ---
    if option == "View Buses":
        cursor.execute("SELECT * FROM Buses")
        buses = cursor.fetchall()
        if buses:
            st.table(buses)
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
                cursor.execute("""INSERT INTO Buses (name, source, destination, date, time, total_seats, available_seats)
                                  VALUES (?, ?, ?, ?, ?, ?, ?)""",
                               (name, source, destination, str(date), str(time), total_seats, total_seats))
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
                        cursor.execute("""UPDATE Buses SET name=?, source=?, destination=?, date=?, time=?, 
                                          total_seats=?, available_seats=? WHERE id=?""",
                                       (name, source, destination, str(date), str(time),
                                        total_seats, available_seats, bus_id))
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
with tab2:
    st.header("User Management")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email FROM Users")
    users = cursor.fetchall()
    conn.close()

    if users:
        st.table(users)
    else:
        st.info("No users found.")
