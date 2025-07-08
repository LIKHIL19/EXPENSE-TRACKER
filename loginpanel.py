import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("Expense Tracker - Login & Register")
root.geometry("520x410")
root.config(bg="#ffffff")
root.resizable(False, False)

# Colors and Styles 
BG_WINDOW   = "#202B43"  
BG_HEADER   = "#232b3a"  
BG_INPUT    = "#f5f7fa"  
TEXT_ACCENT = "#aee938"  
BUTTON_FONT = ("Calibri", 15, "bold")
LABEL_FONT = ("Calibri", 15)
ENTRY_FONT = ("Calibri", 15)

# Register Fram
register_frame = tk.Frame(root, bg=BG_WINDOW)
register_frame.pack(fill="both", expand=True)

tk.Label(register_frame, text="Register", font=("Calibri", 20, "bold"), bg=BG_HEADER, fg="white", width=520, pady=10).pack()

tk.Label(register_frame, text="New Username:", font=LABEL_FONT, bg=BG_WINDOW, fg=TEXT_ACCENT).pack(pady=(10, 0))
entry_new_user = tk.Entry(register_frame, font=ENTRY_FONT, bg=BG_INPUT, width=30, relief="flat")
entry_new_user.pack(pady=5)

tk.Label(register_frame, text="New Password:", font=LABEL_FONT, bg=BG_WINDOW, fg=TEXT_ACCENT).pack(pady=(10, 0))
entry_new_password = tk.Entry(register_frame, font=ENTRY_FONT, show="*", bg=BG_INPUT, width=30, relief="flat")
entry_new_password.pack(pady=5)

tk.Label(register_frame, text="Confirm Password:", font=LABEL_FONT, bg=BG_WINDOW, fg=TEXT_ACCENT).pack(pady=(10, 0))
entry_confirm_password = tk.Entry(register_frame, font=ENTRY_FONT, show="*", bg=BG_INPUT, width=30, relief="flat")
entry_confirm_password.pack(pady=5)

def go_to_login():
    register_frame.pack_forget()
    login_frame.pack(fill="both", expand=True)

def register_fnc():
    user = entry_new_user.get().strip()
    pw1 = entry_new_password.get().strip()
    pw2 = entry_confirm_password.get().strip()
    if not user or not pw1 or not pw2:
        messagebox.showwarning("Incomplete", "Please fill all fields.")
    elif pw1 != pw2:
        messagebox.showerror("Password Mismatch", "Passwords do not match.")
    else:
        messagebox.showinfo("Success", "Registered successfully! You can now log in.")
        go_to_login()

tk.Button(register_frame, text="Register", bg=TEXT_ACCENT, fg="white", font=BUTTON_FONT, width=20, command=register_fnc, cursor="hand2").pack(pady=(15, 5))
tk.Button(register_frame, text="Already registered? Login", command=go_to_login, bg=BG_INPUT, fg=TEXT_ACCENT, font=BUTTON_FONT, width=25, cursor="hand2").pack(pady=5)

# Login Frame
login_frame = tk.Frame(root, bg=BG_WINDOW)

tk.Label(login_frame, text="Login", font=("Calibri", 20, "bold"), bg=BG_HEADER, fg="white", width=520, pady=10).pack()

tk.Label(login_frame, text="Username:", font=LABEL_FONT, bg=BG_WINDOW, fg=TEXT_ACCENT).pack(pady=(10, 0))
entry_user = tk.Entry(login_frame, font=ENTRY_FONT, bg=BG_INPUT, width=30, relief="flat")
entry_user.pack(pady=5)

tk.Label(login_frame, text="Password:", font=LABEL_FONT, bg=BG_WINDOW, fg=TEXT_ACCENT).pack(pady=(10, 0))
entry_password = tk.Entry(login_frame, font=ENTRY_FONT, show="*", bg=BG_INPUT, width=30, relief="flat")
entry_password.pack(pady=5)

def login_fnc():
    username = entry_user.get()
    password = entry_password.get()
    if username == "admin" and password == "password":
        root.destroy()
        import mainpanel
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def go_to_register():
    login_frame.pack_forget()
    register_frame.pack(fill="both", expand=True)

tk.Button(login_frame, text="Login", command=login_fnc, bg=TEXT_ACCENT, fg="white", font=BUTTON_FONT, width=20, cursor="hand2").pack(pady=(15, 5))
tk.Button(login_frame, text="New user? Register", command=go_to_register, bg=BG_INPUT, fg=TEXT_ACCENT, font=BUTTON_FONT, width=25, cursor="hand2").pack(pady=5)

root.mainloop()
