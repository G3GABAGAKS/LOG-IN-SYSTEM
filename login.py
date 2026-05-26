import tkinter as tk
from tkinter import font as tkFont
from tkinter import messagebox
import sqlite3

# ---------------- WINDOW ----------------
root = tk.Tk()
root.title("Facebook Login")
root.geometry("900x400")
root.configure(bg="#F5F6F7")

# ---------------- FONTS ----------------
facebook_font = tkFont.Font(family="Arial", size=36, weight="bold")
label_font = tkFont.Font(family="Arial", size=16)
entry_font = tkFont.Font(family="Arial", size=14)
button_font = tkFont.Font(family="Arial", size=14, weight="bold")

# ---------------- DATABASE ----------------
conn = sqlite3.connect("fb.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS member (
    mem_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")
conn.commit()

# ---------------- FUNCTIONS ----------------
def AddUser(username, password):
    try:
        cursor.execute(
            "INSERT INTO member (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        return True
    except:
        return False

def signup():
    sign_up_window = tk.Toplevel(root)
    sign_up_window.title("Sign Up")
    sign_up_window.geometry("400x300")

    tk.Label(sign_up_window, text="Username", font=label_font).pack(pady=10)

    username_entry = tk.Entry(sign_up_window, font=entry_font)
    username_entry.pack(pady=5)

    tk.Label(sign_up_window, text="Password", font=label_font).pack(pady=10)

    password_entry = tk.Entry(sign_up_window, font=entry_font, show="*")
    password_entry.pack(pady=5)

    def CreateAccount():
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        if username == "" or password == "":
            messagebox.showerror("Error", "Please fill all fields")
            return

        if AddUser(username, password):
            messagebox.showinfo("Success", "Account created successfully")
            sign_up_window.destroy()
        else:
            messagebox.showerror("Error", "Username already exists")

    tk.Button(
        sign_up_window,
        text="Create Account",
        bg='#1877F2',
        fg='white',
        font=button_font,
        command=CreateAccount
    ).pack(pady=20)

def Login():
    username = USERNAME.get().strip()
    password = PASSWORD.get().strip()

    if username == "" or password == "":
        lbl_text.config(text="Please complete the fields!", fg="red")
        return

    cursor.execute(
        "SELECT * FROM member WHERE username=? AND password=?",
        (username, password)
    )

    if cursor.fetchone():
        HomeWindow()
        lbl_text.config(text="")
    else:
        lbl_text.config(text="Invalid username or password", fg="red")

def HomeWindow():
    root.withdraw()

    home = tk.Toplevel()
    home.title("Home")
    home.geometry("500x300")

    tk.Label(
        home,
        text="Successfully Logged In!",
        font=("Arial", 18)
    ).pack(pady=80)

    tk.Button(
        home,
        text="Back",
        bg="#1877F2",
        fg="white",
        command=lambda: Back(home)
    ).pack()

def Back(home):
    home.destroy()
    root.deiconify()

# ---------------- VARIABLES ----------------
USERNAME = tk.StringVar()
PASSWORD = tk.StringVar()

# ---------------- LEFT SIDE ----------------
tk.Label(
    root,
    text="facebook",
    font=facebook_font,
    fg="#1877F2",
    bg="#F5F6F7"
).place(x=50, y=50)

tk.Label(
    root,
    text="Recent Logins",
    font=label_font,
    bg="#F5F6F7"
).place(x=50, y=120)

# ---------------- LOGIN FORM ----------------
email_entry = tk.Entry(
    root,
    textvariable=USERNAME,
    font=entry_font,
    width=30
)
email_entry.place(x=500, y=150)

password_entry = tk.Entry(
    root,
    textvariable=PASSWORD,
    font=entry_font,
    width=30,
    show="*"
)
password_entry.place(x=500, y=200)

login_button = tk.Button(
    root,
    text="Log In",
    font=button_font,
    bg="#1877F2",
    fg="white",
    width=20,
    command=Login
)
login_button.place(x=540, y=250)

tk.Button(
    root,
    text="Create Account",
    font=button_font,
    bg="#42B72A",
    fg="white",
    width=20,
    command=signup
).place(x=540, y=320)

lbl_text = tk.Label(root, text="", bg="#F5F6F7", font=entry_font)
lbl_text.place(x=520, y=360)

root.mainloop()