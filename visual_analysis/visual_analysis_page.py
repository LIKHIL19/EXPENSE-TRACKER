import datetime
from decimal import Decimal

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from database.queries import (
    get_user_files,
    get_spending_over_time,
    get_category_totals,
    execute_query
)

from visual_analysis.reports import get_expense_report
from utils.ui import top_bar, page_hero, section_title, metric_card, alert_card


# ---------------------------------------------------------
# Helper functions
# ---------------------------------------------------------
def safe_float(value):
    """
    Converts database numeric values safely into float.
    Handles Decimal, int, float, None, and string numbers.
    """
    if value is None:
        return 0.0

    if isinstance(value, Decimal):
        return float(value)

    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def clean_label(value, fallback="Uncategorized"):
    """
    Converts database labels into safe strings for charts.
    Prevents Matplotlib object dtype issues.
    """
    if value is None:
        return fallback

    value = str(value).strip()

    if not value:
        return fallback

    return value


def style_axis(ax):
    """
    Applies the same visual style to every chart.
    """
    ax.set_facecolor("#fffaf1")
    ax.tick_params(axis="x", colors="#18120f")
    ax.tick_params(axis="y", colors="#18120f")

    ax.xaxis.label.set_color("#18120f")
    ax.yaxis.label.set_color("#18120f")
    ax.title.set_color("#18120f")

    for spine in ax.spines.values():
        spine.set_color("#d8bfae")

    ax.grid(True, alpha=0.22)


def build_safe_dataframe(data, columns):
    """
    Builds a DataFrame and prevents chart crashes caused by dirty DB values.
    """
    df = pd.DataFrame(data, columns=columns)

    if "Amount" in df.columns:
        df["Amount"] = df["Amount"].apply(safe_float)

    if "Category" in df.columns:
        df["Category"] = df["Category"].apply(lambda x: clean_label(x, "Uncategorized"))

    if "Payment Mode" in df.columns:
        df["Payment Mode"] = df["Payment Mode"].apply(lambda x: clean_label(x, "Unknown"))

    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    return df


# ---------------------------------------------------------
# Main page
# ---------------------------------------------------------
def visual_analysis_page():
    user_id = st.session_state.user_id

    top_bar("Visual Analysis", "Spending Studio", "Charts and Reports")

    page_hero(
        "Visual Finance Exploration",
        "See where your money goes through clean charts and exportable reports.",
        "This section is read-only. It helps you analyze spending over time, category concentration, payment behavior, and report data."
    )

    files = get_user_files(user_id)

    if not files:
        alert_card(
            "No expense file available",
            "Create a file from the Expenses page before viewing charts.",
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

    today = datetime.date.today()
    default_start = today.replace(day=1)

    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input("Start Date", value=default_start)

    with col2:
        end_date = st.date_input("End Date", value=today)

    if start_date > end_date:
        alert_card(
            "Invalid date range",
            "Start date cannot be later than end date.",
            "danger"
        )
        return

    # ---------------------------------------------------------
    # Report data used for summary and export
    # ---------------------------------------------------------
    df_report = get_expense_report(
        user_id=user_id,
        file_id=file_id,
        start_date=start_date,
        end_date=end_date
    )

    if not df_report.empty:
        df_report["Amount"] = df_report["Amount"].apply(safe_float)
        df_report["Category"] = df_report["Category"].apply(
            lambda x: clean_label(x, "Uncategorized")
        )
        df_report["Payment_Mode"] = df_report["Payment_Mode"].apply(
            lambda x: clean_label(x, "Unknown")
        )

    # ---------------------------------------------------------
    # Summary metrics
    # ---------------------------------------------------------
    section_title("Visual Summary")

    if df_report.empty:
        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

        with metric_col1:
            metric_card("Total Spend", "Rs. 0.00", "No data")

        with metric_col2:
            metric_card("Entries", "0", "No expenses")

        with metric_col3:
            metric_card("Highest Expense", "Rs. 0.00", "No data")

        with metric_col4:
            metric_card("Average Expense", "Rs. 0.00", "No data")

        alert_card(
            "No analysis data found",
            "There are no expenses in the selected file and date range.",
            "info"
        )
        return

    total_spend = df_report["Amount"].sum()
    total_entries = len(df_report)
    highest_expense = df_report["Amount"].max()
    average_expense = df_report["Amount"].mean()

    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

    with metric_col1:
        metric_card("Total Spend", f"Rs. {total_spend:.2f}", "Selected period")

    with metric_col2:
        metric_card("Entries", total_entries, "Expense records")

    with metric_col3:
        metric_card("Highest Expense", f"Rs. {highest_expense:.2f}", "Largest single entry")

    with metric_col4:
        metric_card("Average Expense", f"Rs. {average_expense:.2f}", "Average per entry")

    # ---------------------------------------------------------
    # 1. Spending over time
    # ---------------------------------------------------------
    section_title("Spending Over Time")

    time_data = get_spending_over_time(
        user_id,
        file_id,
        start_date,
        end_date
    )

    if time_data:
        df_time = build_safe_dataframe(time_data, ["Date", "Amount"])
        df_time = df_time.dropna(subset=["Date"])
        df_time = df_time.sort_values("Date")

        if not df_time.empty:
            fig, ax = plt.subplots(figsize=(11, 4.8))
            fig.patch.set_facecolor("#fffaf1")

            ax.plot(
                df_time["Date"],
                df_time["Amount"],
                marker="o",
                linewidth=2.5,
                color="#f26a21"
            )

            ax.set_title("Daily Spending Trend", fontsize=15, pad=14)
            ax.set_xlabel("Date")
            ax.set_ylabel("Amount")
            ax.tick_params(axis="x", rotation=30)

            style_axis(ax)

            st.pyplot(fig)
        else:
            alert_card(
                "No valid date data",
                "The selected records do not contain valid expense dates.",
                "info"
            )
    else:
        alert_card(
            "No time-based data",
            "No spending data found for the selected date range.",
            "info"
        )

    # ---------------------------------------------------------
    # 2. Category-wise spending
    # ---------------------------------------------------------
    section_title("Category-Wise Spending")

    category_data = get_category_totals(
        user_id,
        file_id,
        start_date,
        end_date
    )

    if category_data:
        df_cat = build_safe_dataframe(category_data, ["Category", "Amount"])
        df_cat = df_cat.groupby("Category", as_index=False)["Amount"].sum()
        df_cat = df_cat.sort_values("Amount", ascending=False)

        if not df_cat.empty:
            x_positions = list(range(len(df_cat)))
            x_labels = df_cat["Category"].astype(str).tolist()
            y_values = df_cat["Amount"].astype(float).tolist()

            fig2, ax2 = plt.subplots(figsize=(11, 4.8))
            fig2.patch.set_facecolor("#fffaf1")

            ax2.bar(
                x_positions,
                y_values,
                color="#f26a21",
                width=0.55
            )

            ax2.set_xticks(x_positions)
            ax2.set_xticklabels(x_labels, rotation=25, ha="right")

            ax2.set_title("Category-Wise Total Spending", fontsize=15, pad=14)
            ax2.set_xlabel("Category")
            ax2.set_ylabel("Amount")

            style_axis(ax2)

            st.pyplot(fig2)

            top_category = df_cat.iloc[0]["Category"]
            top_amount = df_cat.iloc[0]["Amount"]

            alert_card(
                "Highest spending category",
                f"Your highest spending category is {top_category} with Rs. {top_amount:.2f}. This is the first place to control spending.",
                "info"
            )
        else:
            alert_card(
                "No category data",
                "No category-wise spending found for this period.",
                "info"
            )
    else:
        alert_card(
            "No category data",
            "No category-wise spending found for this period.",
            "info"
        )

    # ---------------------------------------------------------
    # 3. Category distribution
    # ---------------------------------------------------------
    section_title("Category Distribution")

    if category_data:
        df_pie = build_safe_dataframe(category_data, ["Category", "Amount"])
        df_pie = df_pie.groupby("Category", as_index=False)["Amount"].sum()
        df_pie = df_pie[df_pie["Amount"] > 0]
        df_pie = df_pie.sort_values("Amount", ascending=False)

        if not df_pie.empty:
            fig3, ax3 = plt.subplots(figsize=(7, 7))
            fig3.patch.set_facecolor("#fffaf1")
            ax3.set_facecolor("#fffaf1")

            ax3.pie(
                df_pie["Amount"].astype(float).tolist(),
                labels=df_pie["Category"].astype(str).tolist(),
                autopct="%1.1f%%",
                startangle=90,
                colors=[
                    "#f26a21",
                    "#18120f",
                    "#c94d12",
                    "#9d7d61",
                    "#f4c7b7",
                    "#678b48",
                    "#d8bfae"
                ]
            )

            ax3.set_title("Share of Spending by Category", fontsize=15, color="#18120f", pad=14)

            st.pyplot(fig3)
        else:
            alert_card(
                "No category distribution available",
                "Category distribution cannot be generated because all values are zero.",
                "info"
            )

    # ---------------------------------------------------------
    # 4. Payment mode analysis
    # ---------------------------------------------------------
    section_title("Payment Mode Analysis")

    payment_data = execute_query(
        """
        SELECT payment_mode, SUM(amount)
        FROM expenses
        WHERE user_id = %s
          AND file_id = %s
          AND expense_date BETWEEN %s AND %s
        GROUP BY payment_mode
        ORDER BY SUM(amount) DESC
        """,
        (user_id, file_id, start_date, end_date),
        fetchall=True
    )

    if payment_data:
        df_pay = build_safe_dataframe(payment_data, ["Payment Mode", "Amount"])
        df_pay = df_pay.groupby("Payment Mode", as_index=False)["Amount"].sum()
        df_pay = df_pay.sort_values("Amount", ascending=False)

        if not df_pay.empty:
            x_positions = list(range(len(df_pay)))
            x_labels = df_pay["Payment Mode"].astype(str).tolist()
            y_values = df_pay["Amount"].astype(float).tolist()

            fig4, ax4 = plt.subplots(figsize=(11, 4.8))
            fig4.patch.set_facecolor("#fffaf1")

            ax4.bar(
                x_positions,
                y_values,
                color="#18120f",
                width=0.55
            )

            ax4.set_xticks(x_positions)
            ax4.set_xticklabels(x_labels, rotation=0)

            ax4.set_title("Spending by Payment Mode", fontsize=15, pad=14)
            ax4.set_xlabel("Payment Mode")
            ax4.set_ylabel("Amount")

            style_axis(ax4)

            st.pyplot(fig4)

            top_payment = df_pay.iloc[0]["Payment Mode"]
            top_payment_amount = df_pay.iloc[0]["Amount"]

            alert_card(
                "Most used payment mode",
                f"Your highest spending payment mode is {top_payment} with Rs. {top_payment_amount:.2f}.",
                "info"
            )
        else:
            alert_card(
                "No payment mode data",
                "No payment mode records found for this period.",
                "info"
            )
    else:
        alert_card(
            "No payment mode data",
            "No payment mode records found for this period.",
            "info"
        )

    # ---------------------------------------------------------
    # 5. Top expenses table
    # ---------------------------------------------------------
    section_title("Top Expenses")

    df_top = df_report.copy()
    df_top = df_top.sort_values("Amount", ascending=False).head(10)

    display_columns = [
        "Date",
        "Title",
        "Category",
        "Amount",
        "Payment_Mode"
    ]

    available_columns = [col for col in display_columns if col in df_top.columns]

    st.dataframe(
        df_top[available_columns],
        use_container_width=True,
        hide_index=True
    )

    # ---------------------------------------------------------
    # 6. Export report
    # ---------------------------------------------------------
    section_title("Export Report")

    csv = df_report.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download CSV Report",
        data=csv,
        file_name=f"expense_report_{start_date}_to_{end_date}.csv",
        mime="text/csv"
    )

    with st.expander("Preview Full Report Data"):
        st.dataframe(
            df_report,
            use_container_width=True,
            hide_index=True
        )
