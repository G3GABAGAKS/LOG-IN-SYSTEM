<<<<<<< HEAD
# LogIn-System
import tkinter as tk
from tkinter import font as tkFont
import sqlite3

root = tk.Tk()
root.title("Facebook Login")
root.geometry("900x400")
root.configure(bg="#F5F6F7")

facebook_font = tkFont.Font(family="Arial", size=36, weight="bold")
label_font = tkFont.Font(family="Arial", size=16)
entry_font = tkFont.Font(family="Arial", size=14)
button_font = tkFont.Font(family="Arial", size=14, weight="bold")


# DATABASE - (mag assign ta og kinsa mag explain for each category)

def Database():
    global conn, cursor
    conn = sqlite3.connect("fb.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS member (
            mem_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    """)

    conn.commit()


def AddUser(username, password):
    cursor.execute(
        "INSERT INTO member (username, password) VALUES (?, ?)",
        (username, password)
    )
    conn.commit()


Database()


# SIGNUP

def signup():
    global sign_up_window

    sign_up_window = tk.Toplevel(root)
    sign_up_window.title("Facebook Sign Up")
    sign_up_window.geometry("400x300")

    tk.Label(
        sign_up_window,
        text="Username",
        font=label_font
    ).pack(pady=10)

    username_entry = tk.Entry(
        sign_up_window,
        font=entry_font
    )
    username_entry.pack(pady=5)

    tk.Label(
        sign_up_window,
        text="Password",
        font=label_font
    ).pack(pady=10)

    password_entry = tk.Entry(
        sign_up_window,
        font=entry_font,
        show="*"
    )
    password_entry.pack(pady=5)

    def CreateAccount():
        try:
            username = username_entry.get().strip()
            password = password_entry.get().strip()

            if username == "" or password == "":
                lbl_text.config(
                    text="Please fill in all fields!",
                    fg="red"
                )
                return

            AddUser(username, password)

            sign_up_window.destroy()

            lbl_text.config(
                text="Account created successfully!",
                fg="green"
            )

        except sqlite3.Error as e:
            lbl_text.config(
                text=f"Database error: {e}",
                fg="red"
            )

        except Exception as e:
            lbl_text.config(
                text=f"Error: {e}",
                fg="red"
            )

    tk.Button(
        sign_up_window,
        text="Create Account",
        bg='#1877F2',
        fg='white',
        font=button_font,
        command=CreateAccount
    ).pack(pady=20)


# LOGIN

def Login(event=None):
    try:
        username = USERNAME.get().strip()
        password = PASSWORD.get().strip()

        # Prevent empty fields
        if username == "" or password == "":
            lbl_text.config(
                text="Please fill in all fields!",
                fg="red"
            )
            return

        Database()

        cursor.execute(
            "SELECT * FROM member WHERE username=? AND password=?",
            (username, password)
        )

        if cursor.fetchone():

            HomeWindow()

            USERNAME.set("")
            PASSWORD.set("")

            lbl_text.config(text="")

        else:
            lbl_text.config(
                text="Invalid username or password",
                fg="red"
            )

            USERNAME.set("")
            PASSWORD.set("")

    except sqlite3.Error as e:
        lbl_text.config(
            text=f"Database error: {e}",
            fg="red"
        )

    except Exception as e:
        lbl_text.config(
            text=f"Error: {e}",
            fg="red"
        )


# HOME WINDOW

def HomeWindow():
    global Home

    root.withdraw()

    Home = tk.Toplevel()

    Home.title("Facebook Login")
    Home.geometry("500x300")

    label = tk.Label(
        Home,
        text="Successfully Logged In!",
        font=('Arial', 16)
    )

    label.pack(pady=80)

    back_button = tk.Button(
        Home,
        text='Back',
        command=Back,
        bg='#1877F2',
        fg='white',
        font=('Arial', 10),
        width=10,
        height=2
    )

    back_button.pack()


def Back():
    Home.destroy()
    root.deiconify()


# ENTRY EVENTS

def on_password_click(event):

    password_entry.config(show="*")

    if password_entry.get() == "Password":
        password_entry.delete(0, tk.END)
        password_entry.config(fg="black")


def on_email_click(event):

    email_entry.config(show="")

    if email_entry.get() == "Email or phone number":
        email_entry.delete(0, tk.END)
        email_entry.config(fg="black")


# VARIABLES 

USERNAME = tk.StringVar()
PASSWORD = tk.StringVar()


# UI

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

tk.Label(
    root,
    text="Click your name or add an account.",
    font=entry_font,
    fg="#606770",
    bg="#F5F6F7"
).place(x=50, y=150)

user_frame = tk.Frame(
    root,
    width=100,
    height=100,
    bg="#F5F6F7",
    bd=1,
    relief="solid"
)

user_frame.place(x=50, y=180)

tk.Label(
    user_frame,
    text="Group 3",
    font=entry_font,
    bg="#F5F6F7"
).pack(side="bottom", pady=5)

add_account_frame = tk.Frame(
    root,
    width=100,
    height=100,
    bg="#F5F6F7",
    bd=1,
    relief="solid"
)

add_account_frame.place(x=200, y=180)

tk.Label(
    add_account_frame,
    text="Add Account",
    font=entry_font,
    fg="#1877F2",
    bg="#F5F6F7"
).pack(side="bottom", pady=5)

email_entry = tk.Entry(
    root,
    textvariable=USERNAME,
    font=entry_font,
    width=30,
    bd=1,
    relief="solid"
)

email_entry.place(x=500, y=150)

email_entry.insert(0, "Email or phone number")

email_entry.bind("<FocusIn>", on_email_click)

password_entry = tk.Entry(
    root,
    textvariable=PASSWORD,
    font=entry_font,
    width=30,
    bd=1,
    relief="solid"
)

password_entry.place(x=500, y=200)

password_entry.insert(0, "Password")

password_entry.bind("<FocusIn>", on_password_click)

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

login_button.bind('<Return>', Login)

tk.Label(
    root,
    text="Forgot password?",
    font=entry_font,
    fg="#1877F2",
    bg="#F5F6F7"
).place(x=580, y=290)

tk.Button(
    root,
    text="Create Account",
    font=button_font,
    bg="#42B72A",
    fg="white",
    width=20,
    command=signup
).place(x=540, y=320)

lbl_text = tk.Label(
    root,
    font=entry_font,
    bg="#F5F6F7"
)

lbl_text.place(x=500, y=370)

root.mainloop()
=======
# LOG-IN-SYSTEM
>>>>>>> fd4055734d15ffbe992c532b1e3f5a3c7e55d6c0
