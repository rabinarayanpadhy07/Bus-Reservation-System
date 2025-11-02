import streamlit as st
from database.db_connection import get_connection
import bcrypt
import re

# Initialize session state
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

# ---- Helper function to validate email ----
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

# ---- Helper function to validate password ----
def is_strong_password(password):
    return len(password) >= 6  # you can add more rules

# ---- Streamlit Signup Form ----
st.title("User Signup")

with st.form("signup_form"):
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    submit = st.form_submit_button("Sign Up")

if submit:
    if not name or not email or not password:
        st.error("All fields are required!")
    elif not is_valid_email(email):
        st.error("Invalid email address!")
    elif not is_strong_password(password):
        st.error("Password must be at least 6 characters!")
    else:
        # Check if email already exists
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            # Check if email already exists
            cursor.execute("SELECT id FROM Users WHERE email = ?", (email,))
            existing_user = cursor.fetchone()
            
            if existing_user:
                st.error("This email is already registered! Please use a different email or try logging in.")
            else:
                # Hash password
                hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
                
                # Insert into SQLite DB
                cursor.execute(
                    "INSERT INTO Users (name, email, password) VALUES (?, ?, ?)",
                    (name, email, hashed_password)
                )
                conn.commit()
                
                # Get the newly created user ID (using lastrowid is more efficient)
                user_id = cursor.lastrowid
                
                # Automatically log in the user
                st.session_state.user_id = user_id
                st.session_state.user_name = name
                
                st.success(f"🎉 Account created successfully! Welcome, {name}!")
                st.info("You have been automatically logged in. Redirecting to dashboard...")
                st.balloons()  # Celebration animation
                
                # Redirect to user dashboard
                st.switch_page("pages/user_dashboard.py")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}. Please try again.")
        finally:
            conn.close()
