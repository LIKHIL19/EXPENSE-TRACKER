import datetime
import streamlit as st

from auth.session import init_session
from auth.login import authenticate_user
from auth.register import register_user

from database.queries import (
    get_user_files,
    get_monthly_summary,
    get_top_category,
    get_recent_expenses,
    get_recent_files,
    get_user_budget,
    get_file_total
)

from expenses.expenses_page import expenses_page
from overview.overview_page import overview_page
from visual_analysis.visual_analysis_page import visual_analysis_page
from notifications.notifications_page import notifications_page
from profile.profile_page import profile_page
from settings.settings_page import settings_page
from utils.ui import apply_theme, top_bar, page_hero, section_title, metric_card, alert_card


st.set_page_config(
    page_title="Expense Tracker",
    layout="wide"
)

apply_theme()


def login_page():
    top_bar("Secure Login", "Expense Tracker", "Private Ledger Access")

    page_hero(
        "Account Access",
        "Welcome back to your finance dashboard.",
        "Log in to view your ledgers, spending summaries, reports, budget alerts, and visual analysis."
    )

    with st.container(border=True):
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            success, user_id = authenticate_user(username, password)

            if success:
                st.session_state.logged_in = True
                st.session_state.user_id = user_id
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Invalid username or password.")


def register_page():
    top_bar("Create Account", "Expense Tracker", "Start Tracking Clearly")

    page_hero(
        "New User",
        "Create your personal expense workspace.",
        "Register once, then manage multiple expense files with isolated data and clear budget tracking."
    )

    with st.container(border=True):
        username = st.text_input("Username", key="reg_user")
        password = st.text_input("Password", type="password", key="reg_pass")

        if st.button("Register"):
            if not username.strip() or not password.strip():
                st.error("Username and password are required.")
                return

            success, msg = register_user(username, password)

            if success:
                st.success(msg)
            else:
                st.error(msg)


def unauthenticated_view():
    col = st.columns([1, 1.25, 1])[1]

    with col:
        tab1, tab2 = st.tabs(["Login", "Register"])

        with tab1:
            login_page()

        with tab2:
            register_page()


def home_page():
    user_id = st.session_state.user_id
    files = get_user_files(user_id)

    top_bar("Home", "Expense Tracker", "Snapshot Dashboard")

    page_hero(
        "Financial Overview",
        "A clean snapshot of your current spending position.",
        "Home is read-only. Use it to understand your active file, monthly spending, top category, and budget balance."
    )

    if not files:
        alert_card(
            "No expense file found",
            "Create an expense file from the Expenses page before using the dashboard.",
            "warning"
        )
        return

    if st.session_state.get("active_file_id"):
        active_file_id = st.session_state.active_file_id
        active_file_name = st.session_state.active_file_name
    else:
        active_file_id = files[0][0]
        active_file_name = files[0][1]
        st.session_state.active_file_id = active_file_id
        st.session_state.active_file_name = active_file_name

    today = datetime.date.today()
    month_names = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    col_a, col_b, col_c = st.columns([2, 1, 1])

    with col_a:
        st.info(f"Active file: {active_file_name}")

    with col_b:
        selected_month_name = st.selectbox(
            "Month",
            month_names,
            index=today.month - 1
        )

    with col_c:
        selected_year = st.number_input(
            "Year",
            min_value=2000,
            max_value=2100,
            value=today.year,
            step=1
        )

    selected_month = month_names.index(selected_month_name) + 1

    total_spend, expense_count = get_monthly_summary(
        user_id,
        active_file_id,
        int(selected_year),
        selected_month
    )

    top_category = get_top_category(
        user_id,
        active_file_id,
        int(selected_year),
        selected_month
    )

    budget = get_user_budget(user_id)
    file_total = get_file_total(user_id, active_file_id)
    remaining_budget = budget - file_total

    recent_expenses = get_recent_expenses(user_id)
    recent_files = get_recent_files(user_id)

    section_title("Monthly Snapshot")

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        metric_card("Total Spend", f"Rs. {total_spend}", f"{selected_month_name} {selected_year}")

    with m2:
        metric_card("Expenses", expense_count, "Number of entries")

    with m3:
        metric_card("Top Category", top_category, "Highest spending area")

    with m4:
        metric_card("Remaining Budget", f"Rs. {remaining_budget}", "Budget minus file total")

    section_title("Recent Activity")

    left, right = st.columns(2)

    with left:
        st.subheader("Recent Expenses")

        if recent_expenses:
            st.table({
                "Date": [row[0] for row in recent_expenses],
                "Category": [row[1] for row in recent_expenses],
                "Amount": [row[2] for row in recent_expenses],
            })
        else:
            alert_card("No recent expenses", "No expense entries have been added yet.", "info")

    with right:
        st.subheader("Recent Files")

        if recent_files:
            st.table({
                "File Name": [row[0] for row in recent_files],
                "Last Modified": [row[1] for row in recent_files],
            })
        else:
            alert_card("No recent files", "Create a ledger from the Expenses page.", "info")


def authenticated_view():
    with st.sidebar:
        st.markdown("## Expense Tracker")
        st.caption(f"Logged in as {st.session_state.username}")

        st.markdown("---")

        page = st.radio(
            "Navigation",
            [
                "Home",
                "Expenses",
                "Overview",
                "Visual Analysis",
                "Notifications",
                "Profile",
                "Settings"
            ],
            label_visibility="collapsed"
        )

        st.markdown("---")

        if st.button("Logout", key="logout_btn"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]

            st.rerun()

    if page == "Home":
        home_page()
    elif page == "Expenses":
        expenses_page()
    elif page == "Overview":
        overview_page()
    elif page == "Visual Analysis":
        visual_analysis_page()
    elif page == "Notifications":
        notifications_page()
    elif page == "Profile":
        profile_page()
    elif page == "Settings":
        settings_page()


def main():
    init_session()

    if not st.session_state.logged_in:
        unauthenticated_view()
    else:
        authenticated_view()


if __name__ == "__main__":
    main()
