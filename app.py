import streamlit as st

st.set_page_config(page_title="Bus Reservation System", page_icon="🚌", layout="centered")

st.markdown("""
    <div style='text-align: center; padding: 2rem;'>
        <h1 style='color: #667eea;'>Bus Reservation System</h1>
        <p style='font-size: 1.2rem; color: #444;'>
            Welcome to the Bus Reservation System.<br>
            Please use the sidebar to navigate between booking, admin, and user pages.
        </p>
    </div>
""", unsafe_allow_html=True)

st.info("Use the sidebar to access booking, admin dashboard, and user management features.")
