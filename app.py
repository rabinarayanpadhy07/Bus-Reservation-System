import streamlit as st
from database.db_connection import get_connection

st.set_page_config(page_title="Bus Reservation System", page_icon="🚌", layout="centered")

st.markdown("""
    <div style='text-align: center; padding: 2rem;'>
        <h1 style='color: #667eea;'>Bus Reservation System</h1>
        <p style='font-size: 1.2rem; color: #444;'>
            Welcome to the Bus Reservation System.<br>
            Browse available buses and book your journey today!
        </p>
    </div>
""", unsafe_allow_html=True)

# Fetch latest/newly added bus only
try:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, source, destination, date, time, total_seats, available_seats 
        FROM Buses 
        WHERE available_seats > 0
        ORDER BY id DESC
        LIMIT 1
    """)
    bus = cursor.fetchone()
    conn.close()
    
    if bus:
        bus_id, name, source, destination, date, time, total_seats, available_seats = bus
        st.info(" recently added bus")
        
        # Create a card-like container for the bus
        with st.container():
            col1, col2 = st.columns([4, 1])
            
            with col1:
                st.markdown(f"### 🚌 {name}")
                detail_col1, detail_col2, detail_col3, detail_col4 = st.columns(4)
                
                with detail_col1:
                    st.markdown(f"**📍 Route:**\n{source} ➡️ {destination}")
                
                with detail_col2:
                    st.markdown(f"**📅 Date:**\n{date}")
                
                with detail_col3:
                    st.markdown(f"**🕐 Time:**\n{time}")
                
                with detail_col4:
                    if available_seats > 0:
                        st.markdown(f"**💺 Seats:**\n{available_seats}/{total_seats} available")
                    else:
                        st.markdown(f"**❌ Fully Booked**")
            
            with col2:
                st.write("")  # Add some spacing
                st.write("")  # Add some spacing
                if st.button(" Book Now", key=f"book_{bus_id}", type="primary", use_container_width=True):
                    # Store the selected bus ID in session state
                    st.session_state.selected_bus_id = bus_id
                    # Redirect to signup page
                    st.switch_page("pages/signup.py")
    else:
        st.info("😔 No buses with available seats at the moment. Please check back later!")
        
except Exception as e:
    st.error(f"Error loading buses: {str(e)}")

st.markdown("---")
st.info("💡 **Note:** To book a bus, click 'Book Now' and sign up for an account. Use the sidebar to access user dashboard.")
