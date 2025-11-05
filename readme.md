# Bus Reservation System

Streamlit-based web app for browsing buses, booking seats, and managing routes via an admin dashboard. Uses SQLite for storage.

## Tech Stack
- Python 3.10+ (recommended)
- Streamlit (UI)
- SQLite (embedded DB)
- bcrypt (password hashing)

## Prerequisites
- Python 3.10 or newer installed and available on PATH
- Git (optional, for cloning)

## 1) Get the code
```
git clone https://github.com/your-username/Bus-Reservation-System.git
cd Bus-Reservation-System
```

## 2) Create and activate a virtual environment
Windows (PowerShell):
```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Windows (Command Prompt):
```
python -m venv .venv
.\.venv\Scripts\activate.bat
```

macOS/Linux:
```
python3 -m venv .venv
source .venv/bin/activate
```

## 3) Install dependencies
```
pip install --upgrade pip
pip install -r requirements.txt
```

## 4) Initialize the database
Creates the SQLite file at `database/bus_reservation.db` and required tables.
```
python init_db.py
```

## 5) (Optional) Seed sample data
Adds a sample admin and a demo bus.
```
python seed.py
```

Default admin (after seeding):
- Email: `admin@example.com`
- Password: `adminpass`

## 6) Run the app
```
streamlit run app.py
```
Then open the URL displayed in the terminal (usually `http://localhost:8501`).

## Using the app
- Home: Shows the most recently added bus and a quick CTA to sign up.
- Signup/Login: Create a user account (passwords are hashed) or log in.
- User Dashboard (`pages/user_dashboard.py`):
  - Search buses by source, destination, and date
  - Book seats and view/cancel your bookings
- Admin Login (`pages/admin_login.py`): Log in with the seeded admin or your own
- Admin Dashboard (`pages/admin_dashboard.py`):
  - View metrics and recent activity
  - Add/Edit/Delete buses
  - View users and reports

Tip: Streamlit automatically lists the pages found in the `pages/` folder in the sidebar.

## Project structure (abridged)
```
Bus-Reservation-System/
  app.py                      # Streamlit entry point
  requirements.txt
  init_db.py                  # Creates tables from database/setup.sql
  seed.py                     # Inserts sample admin + bus
  database/
    db_connection.py         # SQLite connection helper
    setup.sql                # Schema (Users, Admins, Buses, Bookings)
    bus_reservation.db       # Created after init
  modules/
    booking.py               # Booking logic
  pages/
    signup.py                # User sign up
    user_login.py            # User login
    user_dashboard.py        # User features
    admin_login.py           # Admin login
    admin_dashboard.py       # Admin features
  utils/
    helpers.py, validators.py
```

## Running the console test (optional)
Adjust the IDs inside `test_booking_console.py` to match existing rows, then:
```
python test_booking_console.py
```

## Troubleshooting
- Cannot import Streamlit: Ensure your venv is active and `pip install -r requirements.txt` succeeded.
- Database errors / missing tables: Run `python init_db.py` again. Delete `database/bus_reservation.db` if you want a fresh start.
- Admin login fails: Ensure you ran `seed.py` or created an admin manually in the `Admins` table.
- Port already in use: `streamlit run app.py --server.port 8502` (or another free port).
- Unicode/locale issues on Windows PowerShell: Try running from Command Prompt (`cmd.exe`) or Windows Terminal.

## Notes
- The app uses SQLite by default; no external DB is required.
- `mysql-connector-python` is in `requirements.txt` for potential future use but is not required for SQLite.
