import streamlit as st
from database.db_connection import get_connection
import bcrypt

st.title("User Login")

# Initialize session state
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

# ---- Login Form ----
with st.form("login_form"):
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    submit = st.form_submit_button("Login")

if submit:
    if not email or not password:
        st.error("Both fields are required!")
    else:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, password FROM Users WHERE email=?", (email,))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            user_id, name, hashed_password = user
            if bcrypt.checkpw(password.encode(), hashed_password):
                st.success(f"Welcome, {name}!")
                st.session_state.user_id = user_id
                st.session_state.user_name = name
            else:
                st.error("Incorrect password!")
        else:
            st.error("User not found! Please sign up first.")

# ---- Logout ----
if st.session_state.user_id:
    if st.button("Logout"):
        st.session_state.user_id = None
        st.session_state.user_name = ""
        st.success("Logged out successfully!")
