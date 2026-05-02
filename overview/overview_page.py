import datetime
import streamlit as st

from database.queries import (
    get_user_files,
    get_period_spending,
    get_highest_expense_day,
    get_monthly_total,
    get_user_budget
)

from utils.ui import top_bar, page_hero, section_title, metric_card, alert_card


def overview_page():
    user_id = st.session_state.user_id

    top_bar("Overview", "Expense Analytics", "Read-Only Insights")

    page_hero(
        "Analytical Summary",
        "Understand your spending behavior without modifying data.",
        "Overview converts your expense entries into budget usage, average spending, highest expense day, and month-over-month comparison."
    )

    files = get_user_files(user_id)

    if not files:
        alert_card(
            "No expense file available",
            "Create a file from the Expenses page before using Overview.",
            "warning"
        )
        return

    file_map = {file[1]: file[0] for file in files}

    active_file_name = st.session_state.get("active_file_name")
    default_index = 0

    if active_file_name in file_map:
        default_index = list(file_map.keys()).index(active_file_name)

    selected_file = st.selectbox(
        "Select File",
        list(file_map.keys()),
        index=default_index
    )

    file_id = file_map[selected_file]
    st.session_state.active_file_id = file_id
    st.session_state.active_file_name = selected_file

    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input(
            "Start Date",
            datetime.date.today().replace(day=1)
        )

    with col2:
        end_date = st.date_input(
            "End Date",
            datetime.date.today()
        )

    if start_date > end_date:
        alert_card(
            "Invalid date range",
            "Start date cannot be later than end date.",
            "danger"
        )
        return

    total_spend, active_days = get_period_spending(
        user_id,
        file_id,
        start_date,
        end_date
    )

    avg_daily_spend = round(total_spend / active_days, 2) if active_days else 0

    highest_day = get_highest_expense_day(
        user_id,
        file_id,
        start_date,
        end_date
    )

    section_title("Spending Summary")

    m1, m2, m3 = st.columns(3)

    with m1:
        metric_card("Total Spend", f"Rs. {total_spend}", "Selected period")

    with m2:
        metric_card("Average Daily Spend", f"Rs. {avg_daily_spend}", f"{active_days} active days")

    with m3:
        if highest_day:
            metric_card("Highest Expense Day", str(highest_day[0]), f"Rs. {highest_day[1]}")
        else:
            metric_card("Highest Expense Day", "None", "No spending found")

    section_title("Budget Monitoring")

    budget = get_user_budget(user_id)
    usage_pct = round((total_spend / budget) * 100, 2) if budget else 0
    status = "Exceeded" if budget and total_spend > budget else "Within Budget"

    b1, b2, b3 = st.columns(3)

    with b1:
        metric_card("Monthly Budget", f"Rs. {budget}", "Set from Profile")

    with b2:
        metric_card("Budget Used", f"{usage_pct}%", "Based on selected period")

    with b3:
        metric_card("Status", status, "Budget condition")

    if not budget:
        alert_card(
            "Budget not set",
            "Go to Profile and set your monthly budget for accurate analysis.",
            "warning"
        )
    elif total_spend > budget:
        alert_card(
            "Budget exceeded",
            "Your spending for the selected period is higher than your monthly budget.",
            "danger"
        )
    elif usage_pct >= 80:
        alert_card(
            "Budget usage is high",
            "You have used more than 80 percent of your monthly budget.",
            "warning"
        )
    else:
        alert_card(
            "Budget condition is stable",
            "Your spending is currently within the safe budget range.",
            "success"
        )

    section_title("Month-over-Month Comparison")

    today = datetime.date.today()

    current_month_total = get_monthly_total(
        user_id,
        file_id,
        today.year,
        today.month
    )

    previous_month = today.replace(day=1) - datetime.timedelta(days=1)

    previous_month_total = get_monthly_total(
        user_id,
        file_id,
        previous_month.year,
        previous_month.month
    )

    if previous_month_total > 0:
        mom_change = round(
            ((current_month_total - previous_month_total) / previous_month_total) * 100,
            2
        )
    else:
        mom_change = 0

    metric_card(
        "Monthly Change",
        f"{mom_change}%",
        "Current month compared with previous month"
    )
