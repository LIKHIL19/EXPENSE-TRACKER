import datetime
import streamlit as st

from database.queries import (
    get_user_profile,
    get_user_budget,
    upsert_budget,
    get_usage_stats,
    get_file_total
)

from database.connection import execute_query
from auth.login import authenticate_user
from utils.hashing import hash_password
from utils.ui import top_bar, page_hero, section_title, metric_card, alert_card


def profile_page():
    user_id = st.session_state.user_id
    username = st.session_state.username

    top_bar("Profile", "Account Center", "Identity and Budget")

    page_hero(
        "Profile and Budget Ownership",
        "Manage your account identity, budget, usage, and security.",
        "Profile owns the monthly budget. Other pages only read the budget value for analysis and warnings."
    )

    section_title("Account Information")

    profile = get_user_profile(user_id)

    if profile:
        uname, created_at = profile
    else:
        uname, created_at = username, "-"

    c1, c2 = st.columns(2)

    with c1:
        metric_card("Username", uname, "Current account")

    with c2:
        created_display = str(created_at).split(" ")[0] if created_at else "-"
        metric_card("Account Created", created_display, "Registration date")

    section_title("Monthly Budget")

    current_budget = get_user_budget(user_id)

    total_spent_this_file = 0

    if st.session_state.get("active_file_id"):
        total_spent_this_file = get_file_total(
            user_id,
            st.session_state.active_file_id
        )

    remaining = current_budget - total_spent_this_file

    b1, b2, b3 = st.columns(3)

    with b1:
        metric_card("Budget", f"Rs. {current_budget}", "Monthly limit")

    with b2:
        metric_card("Used", f"Rs. {total_spent_this_file}", "Active file total")

    with b3:
        metric_card("Remaining", f"Rs. {remaining}", "Budget balance")

    with st.expander("Update Monthly Budget"):
        new_budget = st.number_input(
            "Monthly Budget Amount",
            min_value=0,
            step=500,
            value=int(current_budget)
        )

        if st.button("Update Budget"):
            upsert_budget(user_id, new_budget)
            st.success("Budget updated successfully.")
            st.rerun()

    section_title("Usage Statistics")

    stats = get_usage_stats(user_id)

    if stats:
        total_files, total_expenses, active_days = stats
    else:
        total_files, total_expenses, active_days = 0, 0, 0

    s1, s2, s3 = st.columns(3)

    with s1:
        metric_card("Total Files", total_files, "Ledgers created")

    with s2:
        metric_card("Total Expenses", total_expenses, "Entries logged")

    with s3:
        metric_card("Active Days", active_days, "Unique spending days")

    section_title("Security")

    with st.expander("Change Password"):
        old_pwd = st.text_input("Current Password", type="password")
        new_pwd = st.text_input("New Password", type="password")
        confirm_pwd = st.text_input("Confirm New Password", type="password")

        if st.button("Change Password"):
            if not old_pwd or not new_pwd or not confirm_pwd:
                st.error("All password fields are required.")
            elif new_pwd != confirm_pwd:
                st.error("New passwords do not match.")
            else:
                ok, _ = authenticate_user(username, old_pwd)

                if not ok:
                    st.error("Current password is incorrect.")
                else:
                    new_hash = hash_password(new_pwd)

                    execute_query(
                        "UPDATE users SET password_hash = %s WHERE id = %s",
                        (new_hash, user_id)
                    )

                    st.success("Password changed successfully.")

    if st.button("Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]

        st.rerun()
