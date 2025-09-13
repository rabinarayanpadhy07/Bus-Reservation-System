import streamlit as st
from database.db_connection import get_connection
import bcrypt

st.title("Admin Login")

# Initialize session state
if "admin_id" not in st.session_state:
    st.session_state.admin_id = None
if "admin_name" not in st.session_state:
    st.session_state.admin_name = ""

# ---- Login Form ----
with st.form("admin_login_form"):
    email = st.text_input("Admin Email")
    password = st.text_input("Password", type="password")
    submit = st.form_submit_button("Login")

if submit:
    if not email or not password:
        st.error("Both fields are required!")
    else:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, password FROM Admins WHERE email=?", (email,))
        admin = cursor.fetchone()
        conn.close()
        
        if admin:
            admin_id, name, hashed_password = admin
            if bcrypt.checkpw(password.encode(), hashed_password):
                st.success(f"Welcome, Admin {name}!")
                st.session_state.admin_id = admin_id
                st.session_state.admin_name = name
            else:
                st.error("Incorrect password!")
        else:
            st.error("Admin not found! Please contact system administrator.")

# ---- Logout ----
if st.session_state.admin_id:
    if st.button("Logout"):
        st.session_state.admin_id = None
        st.session_state.admin_name = ""
        st.success("Logged out successfully!")
