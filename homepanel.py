import tkinter as tk
from tkinter import ttk
import importlib.util
import os

root = tk.Tk()
root.title("Home Panel")
root.geometry("1000x800")
root.resizable(False, False)
root.configure(bg="#1a2233")

BG_WINDOW   = "#202B43"
BG_HEADER   = "#232b3a"
BG_INPUT    = "#f5f7fa"
TEXT_ACCENT = "#aee938"

sidebar = tk.Frame(root, bg=BG_HEADER, width=200)
sidebar.pack(side="left", fill="y")

content_area = tk.Frame(root, bg=BG_WINDOW)
content_area.pack(side="right", fill="both", expand=True)

home_frame = tk.Frame(content_area, bg=BG_WINDOW)
main_panel_frame = tk.Frame(content_area, bg=BG_WINDOW)
graph_panel_frame = tk.Frame(content_area, bg=BG_WINDOW)

for frame in (home_frame, main_panel_frame, graph_panel_frame):
    frame.place(relx=0, rely=0, relwidth=1, relheight=1)

def show_home():
    home_frame.tkraise()
    for widget in home_frame.winfo_children():
        widget.destroy()
    tk.Label(home_frame, text="📊 Welcome to Expense Tracker!", font=("Calibri", 24, "bold"),
             bg=BG_WINDOW, fg=TEXT_ACCENT).pack(pady=50)
    tk.Label(home_frame, text="Use the sidebar to navigate through the application.",
             font=("Calibri", 16), bg=BG_WINDOW, fg="white").pack(pady=10)

def show_main_panel():
    main_panel_frame.tkraise()
    for widget in main_panel_frame.winfo_children():
        widget.destroy()
    try:
        path_to_main = os.path.abspath("mainpanel.py")
        spec = importlib.util.spec_from_file_location("mainpanel", path_to_main)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    except Exception as e:
        tk.Label(main_panel_frame, text=f"Error loading main panel:\n{e}", fg="red", bg=BG_WINDOW).pack()

def show_graph_panel():
    graph_panel_frame.tkraise()
    for widget in graph_panel_frame.winfo_children():
        widget.destroy()
    tk.Label(graph_panel_frame, text="📈 Graphs Panel (Coming Soon)", bg=BG_WINDOW, fg=TEXT_ACCENT,
             font=("Calibri", 24)).pack(pady=50)

btn_config = {"font": ("Calibri", 14, "bold"), "bg": TEXT_ACCENT, "fg": "black", "relief": "flat",
              "width": 20, "height": 2, "cursor": "hand2"}

tk.Button(sidebar, text="🏠 Home", command=show_home, **btn_config).pack(pady=(20, 10))
tk.Button(sidebar, text="📋 Main Panel", command=show_main_panel, **btn_config).pack(pady=10)
tk.Button(sidebar, text="📊 Graphs", command=show_graph_panel, **btn_config).pack(pady=10)
show_home()
root.mainloop()
