import pandas as pd
import streamlit as st

from database.queries import (
    get_user_files,
    create_file,
    rename_file,
    soft_delete_file,
    get_file_expenses,
    add_expense,
    delete_expense,
    update_expense,
    duplicate_expense,
    get_file_total
)

from expenses.entries import fetch_categories, add_category
from utils.ui import top_bar, page_hero, section_title, metric_card, alert_card


def expenses_page():
    user_id = st.session_state.user_id

    top_bar("Expenses", "Ledger Studio", "Create. Edit. Track.")

    page_hero(
        "Core Workspace",
        "Manage your expense files and daily spending entries.",
        "Every important calculation in this app starts here. File total is the single source of truth for budget usage and analysis."
    )

    files = get_user_files(user_id)

    section_title("File Management")

    left, right = st.columns([1, 1])

    with left:
        with st.container(border=True):
            st.subheader("Create New File")
            name = st.text_input("File Name")
            desc = st.text_input("Description")

            if st.button("Create File"):
                if name.strip():
                    create_file(user_id, name.strip(), desc.strip())
                    st.success("File created successfully.")
                    st.rerun()
                else:
                    st.error("File name is required.")

    with right:
        with st.container(border=True):
            st.subheader("File Rules")
            st.write("Files act like separate ledgers.")
            st.write("Each file has its own expenses and total.")
            st.write("Deleting a file uses soft delete, not permanent deletion.")

    if not files:
        alert_card(
            "No files available",
            "Create your first expense file to start adding entries.",
            "warning"
        )
        return

    file_map = {file[1]: file[0] for file in files}

    active_file_name = st.session_state.get("active_file_name")
    default_index = 0

    if active_file_name in file_map:
        default_index = list(file_map.keys()).index(active_file_name)

    selected_file = st.selectbox(
        "Open Expense File",
        list(file_map.keys()),
        index=default_index
    )

    file_id = file_map[selected_file]
    st.session_state.active_file_id = file_id
    st.session_state.active_file_name = selected_file

    total = get_file_total(user_id, file_id)

    section_title("Active File Summary")

    m1, m2 = st.columns(2)

    with m1:
        metric_card("Active File", selected_file, "Currently opened ledger")

    with m2:
        metric_card("File Total", f"Rs. {total}", "Total amount in this file")

    with st.expander("Rename or Delete Current File"):
        new_name = st.text_input("New File Name", value=selected_file)
        new_desc = st.text_input("New Description")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Rename File"):
                if new_name.strip():
                    rename_file(file_id, user_id, new_name.strip(), new_desc.strip())
                    st.success("File updated successfully.")
                    st.rerun()
                else:
                    st.error("New file name cannot be empty.")

        with col2:
            if st.button("Soft Delete File"):
                soft_delete_file(file_id, user_id)
                st.warning("File deactivated.")
                st.session_state.active_file_id = None
                st.session_state.active_file_name = None
                st.rerun()

    section_title("Categories")

    categories = fetch_categories(user_id)
    cat_map = {category[1]: category[0] for category in categories}

    with st.expander("Manage Categories"):
        new_cat = st.text_input("New Category")

        if st.button("Add Category"):
            if new_cat.strip():
                add_category(user_id, new_cat.strip())
                st.success("Category added.")
                st.rerun()
            else:
                st.error("Category name is required.")

    section_title("Add Expense")

    with st.container(border=True):
        with st.form("add_expense_form"):
            col1, col2 = st.columns(2)

            with col1:
                title = st.text_input("Title")
                amount = st.number_input("Amount", min_value=0.0, step=1.0)

            with col2:
                category_options = list(cat_map.keys()) if cat_map else ["Uncategorized"]
                category = st.selectbox("Category", category_options)
                payment_mode = st.selectbox(
                    "Payment Mode",
                    ["Cash", "UPI", "Card", "Bank Transfer"]
                )

            expense_date = st.date_input("Date")
            description = st.text_area("Description")

            submitted = st.form_submit_button("Add Expense")

            if submitted:
                if not title.strip():
                    st.error("Title is required.")
                elif amount <= 0:
                    st.error("Amount must be greater than zero.")
                else:
                    add_expense(
                        user_id=user_id,
                        file_id=file_id,
                        category_id=cat_map.get(category),
                        title=title.strip(),
                        description=description.strip(),
                        amount=amount,
                        payment_mode=payment_mode,
                        expense_date=expense_date
                    )
                    st.success("Expense added successfully.")
                    st.rerun()

    section_title("Expense Entries")

    expenses = get_file_expenses(user_id, file_id)

    if not expenses:
        alert_card(
            "No expenses in this file",
            "Add your first expense using the form above.",
            "info"
        )
        return

    df = pd.DataFrame(
        expenses,
        columns=["ID", "Date", "Title", "Description", "Amount", "Payment Mode"]
    )

    st.dataframe(
        df.drop(columns=["ID"]),
        use_container_width=True,
        hide_index=True
    )

    section_title("Edit, Duplicate, or Delete")

    exp_map = {
        f"{expense[2]} | Rs. {expense[4]} | {expense[1]}": expense
        for expense in expenses
    }

    selected_expense_label = st.selectbox(
        "Select Expense",
        list(exp_map.keys())
    )

    selected_expense = exp_map[selected_expense_label]

    with st.expander("Edit Selected Expense"):
        edit_title = st.text_input("Edit Title", value=selected_expense[2])
        edit_description = st.text_area("Edit Description", value=selected_expense[3])
        edit_amount = st.number_input(
            "Edit Amount",
            value=float(selected_expense[4]),
            min_value=0.0,
            step=1.0
        )

        payment_options = ["Cash", "UPI", "Card", "Bank Transfer"]
        current_payment = selected_expense[5]

        payment_index = payment_options.index(current_payment) if current_payment in payment_options else 0

        edit_payment_mode = st.selectbox(
            "Edit Payment Mode",
            payment_options,
            index=payment_index
        )

        edit_expense_date = st.date_input("Edit Date", value=selected_expense[1])

        edit_category_options = list(cat_map.keys()) if cat_map else ["Uncategorized"]
        edit_category = st.selectbox("Edit Category", edit_category_options)

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("Update Expense"):
                if not edit_title.strip():
                    st.error("Title cannot be empty.")
                elif edit_amount <= 0:
                    st.error("Amount must be greater than zero.")
                else:
                    update_expense(
                        expense_id=selected_expense[0],
                        user_id=user_id,
                        title=edit_title.strip(),
                        description=edit_description.strip(),
                        amount=edit_amount,
                        payment_mode=edit_payment_mode,
                        expense_date=edit_expense_date,
                        category_id=cat_map.get(edit_category)
                    )
                    st.success("Expense updated.")
                    st.rerun()

        with col2:
            if st.button("Duplicate Expense"):
                duplicate_expense(selected_expense[0], user_id)
                st.success("Expense duplicated.")
                st.rerun()

        with col3:
            if st.button("Delete Expense"):
                delete_expense(selected_expense[0], user_id)
                st.warning("Expense deleted.")
                st.rerun()

    section_title("Bulk Delete")

    bulk_map = {
        f"{expense[2]} | Rs. {expense[4]} | {expense[1]}": expense[0]
        for expense in expenses
    }

    to_delete = st.multiselect(
        "Select expenses to delete",
        list(bulk_map.keys())
    )

    if st.button("Delete Selected Expenses"):
        if not to_delete:
            st.error("Select at least one expense.")
        else:
            for label in to_delete:
                delete_expense(bulk_map[label], user_id)

            st.warning("Selected expenses deleted.")
            st.rerun()
