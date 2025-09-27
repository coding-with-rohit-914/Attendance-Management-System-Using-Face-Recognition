import tkinter as tk
from tkinter import messagebox
import csv
import hashlib
import os
import attendance  # This must now have a start_main_ui() function

USER_DATA_FILE = "user_data.csv"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_user(username, password):
    if not os.path.exists(USER_DATA_FILE):
        return False
    with open(USER_DATA_FILE, mode='r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == username and row[1] == hash_password(password):
                return True
    return False

def add_user(username, password):
    with open(USER_DATA_FILE, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([username, hash_password(password)])

def signup():
    def register_user():
        user = entry_user.get()
        pwd = entry_pwd.get()
        if not user or not pwd:
            messagebox.showerror("Error", "All fields are required!")
            return
        add_user(user, pwd)
        messagebox.showinfo("Success", "User registered! Please login.")
        signup_win.destroy()

    signup_win = tk.Toplevel()
    signup_win.title("Sign Up")
    signup_win.geometry("300x200")
    tk.Label(signup_win, text="Username").pack(pady=5)
    entry_user = tk.Entry(signup_win)
    entry_user.pack()
    tk.Label(signup_win, text="Password").pack(pady=5)
    entry_pwd = tk.Entry(signup_win, show="*")
    entry_pwd.pack()
    tk.Button(signup_win, text="Register", command=register_user).pack(pady=10)

def login():
    user = entry_user.get()
    pwd = entry_pwd.get()
    if check_user(user, pwd):
        messagebox.showinfo("Login Success", f"Welcome {user}!")
        login_win.destroy()
        attendance.start_main_ui()  # <-- Launch attendance UI
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

# Main Login Window
login_win = tk.Tk()
login_win.title("Login")
login_win.geometry("300x200")

tk.Label(login_win, text="Username").pack(pady=5)
entry_user = tk.Entry(login_win)
entry_user.pack()

tk.Label(login_win, text="Password").pack(pady=5)
entry_pwd = tk.Entry(login_win, show="*")
entry_pwd.pack()

tk.Button(login_win, text="Login", command=login).pack(pady=5)
tk.Button(login_win, text="Sign Up", command=signup).pack(pady=5)

login_win.mainloop()
