import streamlit as st
from pathlib import Path

# Import modules
from database import init_db, seed_admin
from auth import login_view, logout
from interns import admin_interns_view
from tasks import admin_tasks_view, intern_tasks_view
from dashboard import admin_dashboard_view, intern_dashboard_view
from reports import reports_view
from announcements import (
    admin_announcements_view,
    intern_announcements_view
)

# Page Configuration
st.set_page_config(
    page_title="Internship Task Tracker",
    page_icon="📌",
    layout="wide"
)

# Company Logo Path
logo_path = Path(__file__).parent.parent / "assets" / "company_logo.jpeg"

# Initialize Database
init_db()
seed_admin()


def main():

    # User Session
    if "user" not in st.session_state:
        st.session_state.user = None

    # Login Page
    if not st.session_state.user:

        st.title("Internship Task Tracker")

        if logo_path.exists():
            col1, col2, col3 = st.columns([1, 2, 1])

            with col2:
                st.image(str(logo_path), width=180)

        login_view()
        return

    # Logged-in User
    user = st.session_state.user

    # Sidebar
    with st.sidebar:

        if logo_path.exists():
            st.image(str(logo_path), width=160)

        st.title("📌 Internship Task Tracker")

        st.caption(f"Signed in as {user['name']}")
        st.caption(user["role"].title())

        # Admin Navigation
        if user["role"] == "admin":
            pages = [
                "Dashboard",
                "Manage Interns",
                "Manage Tasks",
                "Publish Announcements",
                "Reports"
            ]

        # Intern Navigation
        else:
            pages = [
                "My Dashboard",
                "My Tasks",
                "Announcements"
            ]

        page = st.radio(
            "Navigation",
            pages
        )

        st.divider()

        # Logout
        if st.button("Log out", use_container_width=True):
            logout()
            st.rerun()

    # Admin Pages
    if user["role"] == "admin":

        if page == "Dashboard":
            admin_dashboard_view()

        elif page == "Manage Interns":
            admin_interns_view()

        elif page == "Manage Tasks":
            admin_tasks_view()

        elif page == "Publish Announcements":
            admin_announcements_view()

        elif page == "Reports":
            reports_view()

    # Intern Pages
    else:

        if page == "My Dashboard":
            intern_dashboard_view(user["id"])

        elif page == "My Tasks":
            intern_tasks_view(user["id"])

        elif page == "Announcements":
            intern_announcements_view()


# Run Application
if __name__ == "__main__":
    main()
