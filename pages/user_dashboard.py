import streamlit as st
from database.db_connection import get_connection
from datetime import date
from modules import booking

st.title("🚌 Bus Reservation System")

# --- Session Check ---
if "user_id" not in st.session_state or not st.session_state.user_id:
    st.error("🚫 Access denied! Please login first.")
    st.stop()

# Welcome message with better formatting
st.success(f"👋 Welcome back, **{st.session_state.user_name}**! Ready to plan your next trip?")

# Tabs with emojis and better formatting
tab1, tab2 = st.tabs(["🔍 Search & Book Buses", "📖 My Booking History"])

# --- TAB 1: SEARCH & BOOK ---
with tab1:
    st.header("🎯 Find Your Perfect Bus")
    
    # Better organized search form
    with st.form("search_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            source = st.text_input("📍 From City", placeholder="Enter departure city")
        with col2:
            destination = st.text_input("🎯 To City", placeholder="Enter destination city")
        with col3:
            travel_date = st.date_input("📅 Travel Date", min_value=date.today())
        
        search = st.form_submit_button("🔍 Search Available Buses", type="primary", use_container_width=True)
    
    # Store search parameters in session state to maintain them after booking
    if search:
        st.session_state.search_source = source
        st.session_state.search_destination = destination
        st.session_state.search_date = travel_date
        st.session_state.search_performed = True
    
    # Perform search if search button was clicked or if we have stored search parameters
    buses = []
    if search or st.session_state.get('search_performed', False):
        # Use stored search parameters if available
        search_source = st.session_state.get('search_source', source)
        search_destination = st.session_state.get('search_destination', destination)
        search_date = st.session_state.get('search_date', travel_date)
        
        conn = get_connection()
        cursor = conn.cursor()
        
        query = "SELECT id, name, source, destination, date, time, available_seats FROM Buses WHERE 1=1"
        params = []
        
        if search_source:
            query += " AND source LIKE ?"
            params.append(f"%{search_source}%")
        if search_destination:
            query += " AND destination LIKE ?"
            params.append(f"%{search_destination}%")
        if search_date:
            query += " AND date = ?"
            params.append(str(search_date))
        
        cursor.execute(query, tuple(params))
        buses = cursor.fetchall()
        conn.close()
    
    if buses:
        st.subheader(f"🚍 Available Buses ({len(buses)} found)")
        
        for i, bus in enumerate(buses):
            bus_id, name, src, dest, b_date, b_time, seats = bus
            
            # Create an expander for each bus for better organization
            with st.expander(f"🚌 **{name}** - {src} ➡️ {dest}", expanded=True):
                
                # Bus details in columns
                detail_col1, detail_col2, detail_col3 = st.columns(3)
                
                with detail_col1:
                    st.info(f"📅 **Date:** {b_date}")
                
                with detail_col2:
                    st.info(f"🕐 **Time:** {b_time}")
                
                with detail_col3:
                    if seats > 0:
                        st.success(f"💺 **Available Seats:** {seats}")
                    else:
                        st.error(f"❌ **Fully Booked**")
                
                # Booking section
                if seats > 0:
                    st.markdown("---")
                    booking_col1, booking_col2, booking_col3 = st.columns([2, 1, 2])
                    
                    with booking_col1:
                        st.write("**Select number of seats:**")
                    
                    with booking_col2:
                        seats_to_book = st.number_input(
                            "Seats",
                            min_value=1,
                            max_value=seats,
                            key=f"seats_{bus_id}",
                            value=1,
                            label_visibility="collapsed"
                        )
                    
                    with booking_col3:
                        if st.button(f"🎫 Book {seats_to_book} Seat(s)", key=f"book_{bus_id}", type="primary", use_container_width=True):
                            success, msg = booking.book_seats(
                                st.session_state.user_id, bus_id, seats_to_book
                            )
                            if success:
                                st.success(f"🎉 {msg}")
                                # Clear the search results to force refresh
                                if 'search_performed' in st.session_state:
                                    del st.session_state['search_performed']
                                st.rerun()
                            else:
                                st.error(f"❌ {msg}")
                else:
                    st.markdown("---")
                    st.warning("😔 This bus is fully booked. Try searching for other dates or buses.")
                
    elif st.session_state.get('search_performed', False):
        st.info("😔 No buses found matching your criteria. Try different cities or dates.")

# --- TAB 2: BOOKING HISTORY ---
with tab2:
    st.header("📋 Your Booking History")
    
    bookings_list = booking.get_user_bookings(st.session_state.user_id)
    
    if bookings_list:
        st.success(f"You have **{len(bookings_list)}** active booking(s)")
        
        for i, b in enumerate(bookings_list, 1):
            booking_id, bus_name, src, dest, b_date, b_time, seats, b_time_stamp = b
            
            # Each booking in its own container
            with st.container():
                st.markdown("---")
                
                # Main booking info
                booking_col1, booking_col2 = st.columns([4, 1])
                
                with booking_col1:
                    st.subheader(f"🎫 Booking #{i}: {bus_name}")
                    
                    # Booking details in columns
                    detail_col1, detail_col2, detail_col3, detail_col4 = st.columns(4)
                    
                    with detail_col1:
                        st.write(f"📍 **Route:**")
                        st.write(f"{src} ➡️ {dest}")
                    
                    with detail_col2:
                        st.write(f"📅 **Date:**")
                        st.write(f"{b_date}")
                    
                    with detail_col3:
                        st.write(f"🕐 **Time:**")
                        st.write(f"{b_time}")
                    
                    with detail_col4:
                        st.write(f"💺 **Seats:**")
                        st.write(f"{seats} seat(s)")
                    
                    st.caption(f"📝 Booked on: {b_time_stamp}")
                
                with booking_col2:
                    st.write("")  # Add some space
                    if st.button("🗑️ Cancel Booking", key=f"cancel_{booking_id}", type="secondary", use_container_width=True):
                        success, msg = booking.cancel_booking(booking_id, st.session_state.user_id)
                        if success:
                            st.success(f"✅ {msg}")
                            st.rerun()
                        else:
                            st.error(f"❌ {msg}")
    else:
        st.info("📝 No bookings found. Start your journey by booking a bus!")
        
        # Show a helpful message
        st.markdown("""
        ### 🚀 Ready to travel?
        
        1. Go to the **Search & Book** tab
        2. Enter your departure and destination cities
        3. Select your travel date
        4. Choose from available buses and book your seats!
        """)

# Footer
st.markdown("---")
st.info("🚌 **Bus Reservation System** - Safe travels and happy journey!")