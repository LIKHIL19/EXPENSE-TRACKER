import streamlit as st

from database.queries import get_user_settings, upsert_user_settings
from expenses.entries import fetch_categories
from utils.ui import top_bar, page_hero, section_title, alert_card


def settings_page():
    user_id = st.session_state.user_id

    top_bar("Settings", "Application Controls", "Defaults and Behavior")

    page_hero(
        "Application Behavior Settings",
        "Control defaults and workflow behavior without touching financial logic.",
        "Settings should not own budget, spending calculations, or analytics. Those belong to Profile, Expenses, Overview, and Visual Analysis."
    )

    settings = get_user_settings(user_id)

    if settings:
        (
            default_payment,
            default_category,
            date_format,
            auto_open,
            read_only,
            confirm_delete
        ) = settings
    else:
        default_payment = "Cash"
        default_category = None
        date_format = "YYYY-MM-DD"
        auto_open = True
        read_only = False
        confirm_delete = True

    section_title("Expense Defaults")

    categories = fetch_categories(user_id)
    cat_names = [category[1] for category in categories]

    with st.container(border=True):
        col1, col2, col3 = st.columns(3)

        with col1:
            payment_options = ["Cash", "UPI", "Card", "Bank Transfer"]
            payment_index = payment_options.index(default_payment) if default_payment in payment_options else 0

            default_payment = st.selectbox(
                "Default Payment Mode",
                payment_options,
                index=payment_index
            )

        with col2:
            category_options = cat_names if cat_names else ["None"]

            if default_category in category_options:
                category_index = category_options.index(default_category)
            else:
                category_index = 0

            default_category = st.selectbox(
                "Default Category",
                category_options,
                index=category_index
            )

        with col3:
            date_options = ["YYYY-MM-DD", "DD-MM-YYYY", "MM-DD-YYYY"]
            date_index = date_options.index(date_format) if date_format in date_options else 0

            date_format = st.selectbox(
                "Date Format",
                date_options,
                index=date_index
            )

    section_title("Application Behavior")

    with st.container(border=True):
        auto_open = st.checkbox(
            "Auto-open last file on login",
            value=bool(auto_open)
        )

        read_only = st.checkbox(
            "Enable read-only mode for closed files",
            value=bool(read_only)
        )

        confirm_delete = st.checkbox(
            "Confirm before delete",
            value=bool(confirm_delete)
        )

    section_title("Save Changes")

    if st.button("Save Settings"):
        upsert_user_settings(
            user_id=user_id,
            default_payment_mode=default_payment,
            default_category=default_category,
            date_format=date_format,
            auto_open_last_file=auto_open,
            read_only_closed_files=read_only,
            confirm_before_delete=confirm_delete
        )

        st.success("Settings updated successfully.")

    alert_card(
        "Design rule",
        "Settings controls application behavior only. Do not put budget or spending logic here.",
        "info"
    )
