import sys
from pathlib import Path

import streamlit as st

# Add project root to Python path
ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Import project modules
from src.database import init_db, seed_admin
from src.auth import login_view, logout
from src.interns import admin_interns_view
from src.tasks import admin_tasks_view, intern_tasks_view
from src.dashboard import admin_dashboard_view, intern_dashboard_view
from src.reports import reports_view
from src.announcements import (
    admin_announcements_view,
    intern_announcements_view
)

# Page Configuration
st.set_page_config(
    page_title="Internship Task Tracker",
    page_icon="📌",
    layout="wide"
)

# Company Logo
logo_path = ROOT_DIR / "assets" / "company_logo.jpeg"

if logo_path.exists():
    st.sidebar.image(str(logo_path), use_container_width=True)

# Initialize Database
init_db()
seed_admin()

# Login
if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user is None:
    login_view()
    st.stop()

# User Details
user = st.session_state.user
role = user.get("role", "")

# Sidebar
st.sidebar.title("Smart Internship Task Tracker")
st.sidebar.write(f"Welcome, {user.get('name', 'User')}")

if st.sidebar.button("Logout"):
    logout()
    st.rerun()

# Admin Dashboard
if role == "admin":

    menu = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "Manage Interns",
            "Manage Tasks",
            "Reports",
            "Announcements"
        ]
    )

    if menu == "Dashboard":
        admin_dashboard_view()

    elif menu == "Manage Interns":
        admin_interns_view()

    elif menu == "Manage Tasks":
        admin_tasks_view()

    elif menu == "Reports":
        reports_view()

    elif menu == "Announcements":
        admin_announcements_view()

# Intern Dashboard
elif role == "intern":

    menu = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "My Tasks",
            "Announcements"
        ]
    )

    if menu == "Dashboard":
        intern_dashboard_view()

    elif menu == "My Tasks":
        intern_tasks_view()

    elif menu == "Announcements":
        intern_announcements_view()

else:
    st.error("Invalid user role. Please contact admin.")
