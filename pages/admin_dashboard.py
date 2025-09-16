import streamlit as st
from database.db_connection import get_connection
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="Bus Reservation - Admin", page_icon="🚌", layout="wide")

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        padding: 1rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    .success-message {
        padding: 1rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        color: #155724;
        margin: 1rem 0;
    }
    .error-message {
        padding: 1rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        color: #721c24;
        margin: 1rem 0;
    }
    .info-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #17a2b8;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Navigation with better styling
st.sidebar.markdown("""
    <div style='text-align: center; padding: 1rem; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                border-radius: 10px; color: white; margin-bottom: 2rem;'>
        <h2>⚙️ Admin Panel</h2>
    </div>
""", unsafe_allow_html=True)

menu = st.sidebar.radio(
    "Navigation", 
    ["📊 Dashboard", "🚌 Manage Buses", "👥 Manage Users", "📈 Reports"],
    key="navigation"
)

# Header
st.markdown("""
    <div class='main-header'>
        <h1>🚌 Bus Reservation Admin Dashboard</h1>
    </div>
""", unsafe_allow_html=True)

# ✅ Check if admin is logged in
if "admin_id" not in st.session_state or not st.session_state.admin_id:
    st.error("🔒 Access denied! Please login as admin first.")
    st.stop()

st.markdown(f"### Welcome back, **{st.session_state.admin_name}** 👋")

# Helper function for success/error messages
def show_success(message):
    st.success(f"✅ {message}")

def show_error(message):
    st.error(f"❌ {message}")

def show_info(message):
    st.info(f"ℹ️ {message}")

# ==============================
# DASHBOARD OVERVIEW
# ==============================
if menu == "📊 Dashboard":
    st.header("📊 Dashboard Overview")
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get statistics
        cursor.execute("SELECT COUNT(*) FROM Buses")
        total_buses = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM Users")
        total_users = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM Bookings")
        total_bookings = cursor.fetchone()[0]
        
        cursor.execute("SELECT SUM(total_seats - available_seats) FROM Buses")
        occupied_seats = cursor.fetchone()[0] or 0
        
        # Display metrics in columns
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🚌 Total Buses", total_buses)
        with col2:
            st.metric("👥 Total Users", total_users)
        with col3:
            st.metric("📝 Total Bookings", total_bookings)
        with col4:
            st.metric("🪑 Occupied Seats", occupied_seats)
        
        st.markdown("---")
        
        # Recent activities
        st.subheader("📋 Recent Activities")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🚌 Latest Buses")
            cursor.execute("SELECT name, source, destination, date FROM Buses ORDER BY id DESC LIMIT 5")
            recent_buses = cursor.fetchall()
            if recent_buses:
                for bus in recent_buses:
                    st.markdown(f"• **{bus[0]}** - {bus[1]} → {bus[2]} ({bus[3]})")
            else:
                st.info("No buses added yet")
        
        with col2:
            st.markdown("#### 📝 Latest Bookings")
            cursor.execute("""
                SELECT u.name, b.name, bs.date 
                FROM Bookings bk
                JOIN Users u ON bk.user_id = u.id
                JOIN Buses b ON bk.bus_id = b.id
                JOIN Buses bs ON bk.bus_id = bs.id
                ORDER BY bk.id DESC LIMIT 5
            """)
            recent_bookings = cursor.fetchall()
            if recent_bookings:
                for booking in recent_bookings:
                    st.markdown(f"• **{booking[0]}** booked {booking[1]} for {booking[2]}")
            else:
                st.info("No bookings made yet")
        
        conn.close()
        
    except Exception as e:
        show_error(f"Error loading dashboard: {str(e)}")

# ==============================
# TAB 1: Manage Buses
# ==============================
elif menu == "🚌 Manage Buses":
    st.header("🚌 Bus Management")
    
    # Create tabs for better organization
    tab1, tab2, tab3, tab4 = st.tabs(["📋 View Buses", "➕ Add Bus", "✏️ Edit Bus", "🗑️ Delete Bus"])
    
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # --- View Buses Tab ---
        with tab1:
            st.subheader("📋 All Buses")
            cursor.execute("SELECT * FROM Buses")
            buses = cursor.fetchall()
            
            if buses:
                df_buses = pd.DataFrame(
                    buses,
                    columns=["ID", "Name", "Source", "Destination", "Date", "Time", "Total Seats", "Available Seats"]
                )
                
                # Add search functionality
                search_term = st.text_input("🔍 Search buses by name, source, or destination:")
                if search_term:
                    mask = df_buses.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
                    df_buses = df_buses[mask]
                
                # Display dataframe with better formatting
                st.dataframe(
                    df_buses,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "ID": st.column_config.NumberColumn("Bus ID", width="small"),
                        "Name": st.column_config.TextColumn("Bus Name", width="medium"),
                        "Source": st.column_config.TextColumn("From", width="medium"),
                        "Destination": st.column_config.TextColumn("To", width="medium"),
                        "Date": st.column_config.DateColumn("Travel Date", width="medium"),
                        "Time": st.column_config.TimeColumn("Departure", width="small"),
                        "Total Seats": st.column_config.NumberColumn("Total", width="small"),
                        "Available Seats": st.column_config.NumberColumn("Available", width="small")
                    }
                )
                
                st.info(f"📊 Total buses: {len(df_buses)}")
            else:
                show_info("No buses available. Add your first bus using the 'Add Bus' tab.")

        # --- Add Bus Tab ---
        with tab2:
            st.subheader("➕ Add New Bus")
            
            with st.form("add_bus_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    name = st.text_input("🚌 Bus Name *", placeholder="e.g., Volvo AC Sleeper")
                    source = st.text_input("📍 Source City *", placeholder="e.g., Mumbai")
                    destination = st.text_input("🎯 Destination City *", placeholder="e.g., Delhi")
                
                with col2:
                    date = st.date_input("📅 Travel Date *", min_value=datetime.now().date())
                    time = st.time_input("⏰ Departure Time *")
                    total_seats = st.number_input("🪑 Total Seats *", min_value=1, max_value=100, value=40)
                
                submitted = st.form_submit_button("➕ Add Bus", type="primary", use_container_width=True)
                
                if submitted:
                    if not all([name, source, destination]):
                        show_error("Please fill in all required fields marked with *")
                    else:
                        try:
                            cursor.execute(
                                """INSERT INTO Buses (name, source, destination, date, time, total_seats, available_seats)
                                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                                (name, source, destination, str(date), str(time), total_seats, total_seats),
                            )
                            conn.commit()
                            show_success(f"Bus '{name}' added successfully!")
                            st.rerun()
                        except Exception as e:
                            show_error(f"Error adding bus: {str(e)}")

        # --- Edit Bus Tab ---
        with tab3:
            st.subheader("✏️ Edit Existing Bus")
            
            cursor.execute("SELECT id, name, source, destination FROM Buses ORDER BY name")
            buses = cursor.fetchall()
            
            if buses:
                bus_options = {f"{bus[1]} - {bus[2]} → {bus[3]} (ID: {bus[0]})": bus[0] for bus in buses}
                
                selected_bus = st.selectbox("Select Bus to Edit:", [""] + list(bus_options.keys()))
                
                if selected_bus:
                    bus_id = bus_options[selected_bus]
                    cursor.execute("SELECT * FROM Buses WHERE id=?", (bus_id,))
                    bus = cursor.fetchone()
                    
                    if bus:
                        with st.form("edit_bus_form"):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                name = st.text_input("🚌 Bus Name", value=bus[1])
                                source = st.text_input("📍 Source City", value=bus[2])
                                destination = st.text_input("🎯 Destination City", value=bus[3])
                            
                            with col2:
                                # Convert string date to datetime object if needed
                                try:
                                    bus_date = datetime.strptime(bus[4], '%Y-%m-%d').date()
                                except:
                                    bus_date = datetime.now().date()
                                
                                date = st.date_input("📅 Travel Date", value=bus_date)
                                
                                # Convert string time to datetime object if needed
                                try:
                                    bus_time = datetime.strptime(bus[5], '%H:%M:%S').time()
                                except:
                                    bus_time = datetime.now().time()
                                
                                time = st.time_input("⏰ Departure Time", value=bus_time)
                                total_seats = st.number_input("🪑 Total Seats", min_value=1, value=int(bus[6]))
                            
                            # Calculate available seats automatically
                            booked_seats = total_seats - int(bus[7]) if bus[7] is not None else 0
                            available_seats = total_seats - booked_seats
                            
                            st.info(f"📊 Currently booked seats: {booked_seats} | Available seats will be: {available_seats}")
                            
                            submitted = st.form_submit_button("💾 Update Bus", type="primary", use_container_width=True)
                            
                            if submitted:
                                try:
                                    cursor.execute(
                                        """UPDATE Buses SET name=?, source=?, destination=?, date=?, time=?, 
                                           total_seats=?, available_seats=? WHERE id=?""",
                                        (name, source, destination, str(date), str(time), total_seats, available_seats, bus_id),
                                    )
                                    conn.commit()
                                    show_success(f"Bus '{name}' updated successfully!")
                                    st.rerun()
                                except Exception as e:
                                    show_error(f"Error updating bus: {str(e)}")
            else:
                show_info("No buses available to edit.")

        # --- Delete Bus Tab ---
        with tab4:
            st.subheader("🗑️ Delete Bus")
            st.warning("⚠️ **Warning**: Deleting a bus will also remove all associated bookings!")
            
            cursor.execute("SELECT id, name, source, destination FROM Buses ORDER BY name")
            buses = cursor.fetchall()
            
            if buses:
                bus_options = {f"{bus[1]} - {bus[2]} → {bus[3]} (ID: {bus[0]})": bus[0] for bus in buses}
                
                selected_bus = st.selectbox("Select Bus to Delete:", [""] + list(bus_options.keys()), key="delete_bus")
                
                if selected_bus:
                    bus_id = bus_options[selected_bus]
                    
                    # Show bus details
                    cursor.execute("SELECT * FROM Buses WHERE id=?", (bus_id,))
                    bus = cursor.fetchone()
                    
                    if bus:
                        st.markdown("#### Bus Details:")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.write(f"**Name:** {bus[1]}")
                            st.write(f"**Route:** {bus[2]} → {bus[3]}")
                        with col2:
                            st.write(f"**Date:** {bus[4]}")
                            st.write(f"**Time:** {bus[5]}")
                        with col3:
                            st.write(f"**Total Seats:** {bus[6]}")
                            st.write(f"**Available:** {bus[7]}")
                        
                        # Confirmation checkbox
                        confirm = st.checkbox("I understand that this action cannot be undone")
                        
                        if st.button("🗑️ Delete Bus", type="secondary", disabled=not confirm):
                            try:
                                # First delete related bookings
                                cursor.execute("DELETE FROM Bookings WHERE bus_id=?", (bus_id,))
                                # Then delete the bus
                                cursor.execute("DELETE FROM Buses WHERE id=?", (bus_id,))
                                conn.commit()
                                show_success(f"Bus '{bus[1]}' and all related bookings deleted successfully!")
                                st.rerun()
                            except Exception as e:
                                show_error(f"Error deleting bus: {str(e)}")
            else:
                show_info("No buses available to delete.")

        conn.close()
        
    except Exception as e:
        show_error(f"Database connection error: {str(e)}")

# ==============================
# TAB 2: Manage Users
# ==============================
elif menu == "👥 Manage Users":
    st.header("👥 User Management")
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email FROM Users ORDER BY name")
        users = cursor.fetchall()
        conn.close()

        if users:
            df_users = pd.DataFrame(users, columns=["User ID", "Full Name", "Email Address"])
            
            # Add search functionality
            search_user = st.text_input("🔍 Search users by name or email:")
            if search_user:
                mask = df_users.astype(str).apply(lambda x: x.str.contains(search_user, case=False, na=False)).any(axis=1)
                df_users = df_users[mask]
            
            st.dataframe(
                df_users,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "User ID": st.column_config.NumberColumn("ID", width="small"),
                    "Full Name": st.column_config.TextColumn("Name", width="medium"),
                    "Email Address": st.column_config.TextColumn("Email", width="large")
                }
            )
            
            st.info(f"👥 Total registered users: {len(df_users)}")
        else:
            show_info("No users registered yet.")
            
    except Exception as e:
        show_error(f"Error loading users: {str(e)}")

# ==============================
# TAB 3: Reports & Charts
# ==============================
elif menu == "📈 Reports":
    st.header("📈 Reports & Analytics")
    
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Create tabs for different reports
        report_tab1, report_tab2, report_tab3 = st.tabs(["📊 Booking Analytics", "🪑 Occupancy Report", "💰 Revenue Report"])
        
        with report_tab1:
            st.subheader("📅 Daily Bookings Analysis")
            
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
                
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    # Interactive plotly chart
                    fig = px.line(df_bookings, x="Date", y="Total Bookings", 
                                title="Daily Bookings Trend",
                                markers=True)
                    fig.update_layout(
                        xaxis_title="Date",
                        yaxis_title="Number of Bookings",
                        hovermode='x unified'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.metric("📊 Total Booking Days", len(df_bookings))
                    st.metric("📈 Average Daily Bookings", f"{df_bookings['Total Bookings'].mean():.1f}")
                    st.metric("🏆 Peak Day Bookings", df_bookings['Total Bookings'].max())
                
                st.dataframe(df_bookings, use_container_width=True)
            else:
                show_info("No booking data available yet.")

        with report_tab2:
            st.subheader("🪑 Bus Occupancy Analysis")
            
            # --- Seat Occupancy Report ---
            cursor.execute(
                """
                SELECT name, total_seats, (total_seats - available_seats) as booked_seats,
                       ROUND(((total_seats - available_seats) * 100.0 / total_seats), 2) as occupancy_rate
                FROM Buses
                WHERE total_seats > 0
                """
            )
            occupancy = cursor.fetchall()

            if occupancy:
                df_occ = pd.DataFrame(occupancy, columns=["Bus Name", "Total Seats", "Booked Seats", "Occupancy %"])
                
                # Occupancy chart
                fig = px.bar(df_occ, x="Bus Name", y=["Booked Seats", "Total Seats"], 
                           title="Seat Occupancy per Bus",
                           barmode='group',
                           color_discrete_map={"Booked Seats": "#ff6b6b", "Total Seats": "#4ecdc4"})
                fig.update_layout(xaxis_title="Bus Name", yaxis_title="Number of Seats")
                st.plotly_chart(fig, use_container_width=True)
                
                # Occupancy rate pie chart
                if df_occ['Occupancy %'].sum() > 0:
                    fig_pie = px.pie(df_occ, values="Booked Seats", names="Bus Name", 
                                   title="Distribution of Booked Seats by Bus")
                    st.plotly_chart(fig_pie, use_container_width=True)
                
                st.dataframe(df_occ, use_container_width=True, hide_index=True)
                
                # Summary metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("🚌 Total Buses", len(df_occ))
                with col2:
                    st.metric("🪑 Total Seats", df_occ['Total Seats'].sum())
                with col3:
                    st.metric("📊 Average Occupancy", f"{df_occ['Occupancy %'].mean():.1f}%")
            else:
                show_info("No buses or booking data available yet.")

        with report_tab3:
            st.subheader("💰 Revenue Analytics")
            
            # This is a placeholder for revenue reporting
            # You'll need to add price fields to your database to implement this
            st.info("💡 **Coming Soon**: Revenue reporting will be available once ticket pricing is implemented in the system.")
            
            # Mock data for demonstration
            st.markdown("#### 📊 Planned Revenue Features:")
            st.markdown("- Daily revenue tracking")
            st.markdown("- Revenue by route analysis")
            st.markdown("- Monthly/quarterly reports")
            st.markdown("- Pricing trend analysis")

        conn.close()
        
    except Exception as e:
        show_error(f"Error generating reports: {str(e)}")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 1rem;'>
        🚌 Bus Reservation Admin Dashboard | Built with Streamlit
    </div>
    """, 
    unsafe_allow_html=True
)