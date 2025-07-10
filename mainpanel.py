import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
import csv

root = tk.Tk()
root.title("Expense Tracker")
root.geometry("750x800")
root.resizable(False, False)
root.configure(bg="#1a2233")

# Color Palette
BG_WINDOW   = "#202B43"
BG_HEADER   = "#232b3a"
BG_INPUT    = "#f5f7fa"
TEXT_ACCENT = "#aee938"

# Style Configuration
style = ttk.Style()
style.theme_use("default")
style.configure("Treeview",
    background=BG_HEADER,
    foreground="white",
    rowheight=30,
    fieldbackground=BG_HEADER,
    font=("Calibri", 15, "normal")
)
style.configure("Treeview.Heading",
    font=("Calibri", 17, "bold"),
    background="#1a2233",
    foreground=BG_INPUT,
    relief="flat"
)
style.map("Treeview",
    background=[("selected", "#3399FF")],
    foreground=[("selected", "white")]
)

# Variables
budget_var = tk.StringVar()
total_var = tk.StringVar(value="Total: ₹0")
balance_var = tk.StringVar(value="Balance: ₹0")

# Display Frame
display_frame = tk.Frame(root, bg=BG_HEADER, width=655, height=400, bd=2, relief=tk.SUNKEN)
display_frame.pack(pady=(20, 5))
display_frame.pack_propagate(False)

tree_view = ttk.Treeview(display_frame, columns=("Num", "Purpose", "Amount", "Date", "Category"), show="headings")
tree_view.heading("Num", text="Num")
tree_view.heading("Purpose", text="Purpose")
tree_view.heading("Amount", text="Amount")
tree_view.heading("Date", text="Date")
tree_view.heading("Category", text="Category")

tree_view.column("Num", width=50, anchor=tk.CENTER)
tree_view.column("Purpose", width=225, anchor=tk.W)
tree_view.column("Amount", width=115, anchor=tk.E)
tree_view.column("Date", width=125, anchor=tk.CENTER)
tree_view.column("Category", width=155, anchor=tk.W)
tree_view.pack(fill=tk.BOTH, expand=True)

# Totals Frame
totals_frame = tk.Frame(root, bg=BG_WINDOW)
totals_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

tk.Label(totals_frame, textvariable=total_var, font=("Calibri", 16, "bold"), bg=BG_WINDOW, fg=TEXT_ACCENT).pack(side=tk.LEFT, padx=20)
tk.Label(totals_frame, textvariable=balance_var, font=("Calibri", 16, "bold"), bg=BG_WINDOW, fg=TEXT_ACCENT).pack(side=tk.RIGHT, padx=20)

# Entry Frame
entry_frame = tk.Frame(root, bg=BG_WINDOW, bd=2, relief=tk.SUNKEN)
entry_frame.pack(fill=tk.X, padx=10, pady=10)

def create_labeled_entry(row, column, label, var_name, width):
    tk.Label(entry_frame, text=label, font=("Calibri", 20, "bold"), bg=BG_WINDOW, fg=TEXT_ACCENT).grid(row=row, column=column, padx=5, pady=5, sticky="w")
    entry = tk.Entry(entry_frame, font=("Calibri", 15), width=width, bg=BG_INPUT, relief="flat")
    entry.grid(row=row, column=column+1, padx=5, pady=5, sticky="w")
    return entry

num_entry = create_labeled_entry(0, 0, "Number:", "num", 10)
purpose_entry = create_labeled_entry(1, 0, "Purpose:", "purpose", 30)
amount_entry = create_labeled_entry(2, 0, "Amount:", "amount", 15)
date_entry = create_labeled_entry(2, 2, "Date:", "date", 15)
category_entry = create_labeled_entry(3, 0, "Category:", "category", 20)
budget_entry = create_labeled_entry(3, 2, "Budget:", "budget", 15)

# Button Functions
def update_totals():
    total = 0
    for child in tree_view.get_children():
        amount = tree_view.item(child)['values'][2]
        try:
            total += float(amount)
        except:
            continue
    total_var.set(f"Total: ₹{total:.2f}")
    try:
        budget = float(budget_entry.get())
        balance = budget - total
        balance_var.set(f"Balance: ₹{balance:.2f}")
    except:
        balance_var.set("Balance: ₹0")

def add_item():
    num = num_entry.get().strip()
    purpose = purpose_entry.get().strip()
    amount = amount_entry.get().strip()
    date = date_entry.get().strip()
    category = category_entry.get().strip()

    if not (num and purpose and amount and date and category):
        messagebox.showwarning("Incomplete", "Please fill all fields.")
        return

    tree_view.insert("", "end", values=(num, purpose, amount, date, category))
    clear_entries()
    update_totals()

def delete_item():
    selected = tree_view.selection()
    if not selected:
        messagebox.showwarning("Selection Error", "Please select an item to delete.")
        return
    for item in selected:
        tree_view.delete(item)
    update_totals()

def clear_entries():
    for entry in [num_entry, purpose_entry, amount_entry, date_entry, category_entry]:
        entry.delete(0, tk.END)

def clear_all():
    tree_view.delete(*tree_view.get_children())
    update_totals()

# Buttons
button_frame = tk.Frame(root, bg=BG_WINDOW, padx=10, pady=10)
button_frame.pack(fill=tk.X, padx=10, pady=10)

btn_config = {"font": ("Calibri", 12, "bold"), "width": 15, "relief": "flat", "cursor": "hand2"}

tk.Button(button_frame, text="Add Item", command=add_item, bg=TEXT_ACCENT, fg="black", **btn_config).grid(row=0, column=0, padx=5, pady=5)
tk.Button(button_frame, text="Delete Item", command=delete_item, bg=TEXT_ACCENT, fg="black", **btn_config).grid(row=0, column=1, padx=5, pady=5)
tk.Button(button_frame, text="Clear Entries", command=clear_entries, bg=TEXT_ACCENT, fg="black", **btn_config).grid(row=0, column=2, padx=5, pady=5)
tk.Button(button_frame, text="Clear List", command=clear_all, bg=TEXT_ACCENT, fg="black", **btn_config).grid(row=0, column=3, padx=5, pady=5)

# File saving and opening
def save_to_csv():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                             filetypes=[("CSV files", "*.csv")])
    if file_path:
        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Number", "Purpose", "Amount", "Date", "Category"])
            for child in tree_view.get_children():
                writer.writerow(tree_view.item(child)["values"])
        messagebox.showinfo("Success", "Expenses saved successfully!")

def load_from_csv():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        clear_all()  # Clear current entries
        with open(file_path, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                if len(row) == 5:
                    tree_view.insert("", "end", values=row)
        update_totals()
        messagebox.showinfo("Loaded", "Expenses loaded successfully!")

# Menu Bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=False)
file_menu.add_command(label="New Budget", command=lambda: budget_entry.delete(0, tk.END))
file_menu.add_command(label="Clear Expenses", command=clear_all)
file_menu.add_separator()
file_menu.add_command(label="Save to File", command=save_to_csv)
file_menu.add_command(label="Open Previous File", command=load_from_csv)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

# Center Window
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - root.winfo_reqwidth()) // 2
y = (screen_height - root.winfo_reqheight()) // 2
root.geometry(f"+{x}+{y}")

root.mainloop()
