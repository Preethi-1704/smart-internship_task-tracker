import sys
from pathlib import Path

import streamlit as st

# --------------------------------
# PROJECT ROOT PATH
# --------------------------------

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


# --------------------------------
# IMPORT MODULES
# --------------------------------

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


# --------------------------------
# PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="Smart Internship Task Tracker",
    page_icon="📌",
    layout="wide"
)


# --------------------------------
# COMPANY LOGO
# --------------------------------

st.sidebar.title("DefineInfoTech Pvt. Ltd.")

# Correct company logo path
logo_path = ROOT_DIR / "src" / "company_logo.jpeg"

if logo_path.is_file():

    st.sidebar.image(
        str(logo_path),
        width=180
    )

else:

    st.sidebar.error("Company logo not found!")

    st.sidebar.write("Logo path checked:")

    st.sidebar.code(str(logo_path))

    st.sidebar.warning(
        "Please check company_logo.jpeg location."
    )


st.sidebar.divider()


# --------------------------------
# DATABASE INITIALIZATION
# --------------------------------

init_db()
seed_admin()


# --------------------------------
# SESSION STATE
# --------------------------------

if "user" not in st.session_state:
    st.session_state.user = None


# --------------------------------
# LOGIN PAGE
# --------------------------------

if st.session_state.user is None:

    login_view()
    st.stop()


# --------------------------------
# CURRENT USER
# --------------------------------

user = st.session_state.user

role = user.get("role", "")


# --------------------------------
# SIDEBAR USER DETAILS
# --------------------------------

st.sidebar.subheader("Smart Internship Task Tracker")

st.sidebar.write(
    f"Welcome, {user.get('name', 'User')}"
)

st.sidebar.divider()


# --------------------------------
# LOGOUT
# --------------------------------

if st.sidebar.button("Logout"):

    logout()
    st.rerun()


# --------------------------------
# ADMIN DASHBOARD
# --------------------------------

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


# --------------------------------
# INTERN DASHBOARD
# --------------------------------

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


# --------------------------------
# INVALID ROLE
# --------------------------------

else:

    st.error(
        "Invalid user role. Please contact admin."
    )
