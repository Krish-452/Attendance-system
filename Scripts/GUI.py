import csv
import tkinter as tk
from tkinter import messagebox




def add_placeholder(entry, placeholder, color='grey'):
    def on_focus_in(event):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg='black')

    def on_focus_out(event):
        if not entry.get():
            entry.insert(0, placeholder)
            entry.config(fg=color)

    entry.insert(0, placeholder)
    entry.config(fg=color)
    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)


def homepage() -> None:

    canvas.delete("all")

    canvas.create_rectangle(150, 70, 450, 470, fill='white')
    canvas.create_rectangle(150, 70, 450, 150, fill='#72BF6A')

    login_button = tk.Button(root, text="Login", font=("Arial", 14, "bold"), bg='#46923C', fg='white', borderwidth=0,
                       activebackground='#276221', activeforeground='white', width=18, height=2, command=login)
    create_account_button = tk.Button(root, text="Create Account", font=("Arial", 14, "bold"), bg='#46923C', fg='white', borderwidth=0,
                       activebackground='#276221', activeforeground='white', width=18, height=2, command=create_account)

    canvas.create_text(300, 110, text="Welcome", font=("Arial", 20, 'bold'))
    canvas.create_window(300, 250, window=login_button)
    canvas.create_window(300, 360, window=create_account_button)


def create_account() -> None:
    canvas.delete("all")

    user_name = tk.Entry(canvas, width=12, font=("Arial", 20, "bold"), bg='#ACD8A7')
    add_placeholder(user_name, "👤 Username")
    password = tk.Entry(canvas, width=12, font=("Arial", 20, "bold"), bg='#ACD8A7')
    add_placeholder(password, "🔑 Password")

    canvas.create_rectangle(150, 70, 450, 470, fill='white')
    canvas.create_rectangle(150, 70, 450, 150, fill='#72BF6A')

    back_button = tk.Button(canvas, text="← Back", font=("Arial", 12),
                            bg="#72BF6A", fg="white", borderwidth=0,
                            command=homepage)

    create_account_button = tk.Button(canvas, text="Create Account", font=("Arial", 14, "bold"),
                                      bg='#46923C', fg='white', borderwidth=0, width=18, height=2,
                                      command=lambda: check_validity(user_name.get(), password.get()))

    canvas.create_text(300, 110, text="Create Account", font=("Arial", 20, 'bold'))
    canvas.create_window(300, 210, window=user_name)
    canvas.create_window(300, 270, window=password)
    canvas.create_window(300, 430, window=back_button)
    canvas.create_window(300, 360, window=create_account_button)


def check_validity(username: str, password: str) -> None:
    special_chars: set = set("!@#$%^&*()-_=+[]{}|;:'\",.<>?/~`")
    valid_username = True
    valid_password = True

    with open('login_professor.csv', 'r') as login_data:
        for row in csv.reader(login_data):
            if row[0] == username:
                messagebox.showwarning("Username already exists", "Username already exists, please select a different username.")
                valid_username = False

    if username == "":
        valid_username = False

    if len(password) < 8:
        messagebox.showwarning("Invalid Password", "Password must be at least 8 characters long")
        valid_password = False

    if any(char.isupper() for char in password) == False or any(char.islower() for char in password) == False or any(
            char.isdigit() for char in password) == False or set(password).isdisjoint(special_chars) == True:
        messagebox.showwarning("Invalid Password", """Password must Contain at least one upper case and one lower case letter
Password must contain at least one number (1-9)
Password must Contain at least one special character""")
        valid_password = False

    if valid_username == True and valid_password == True:
        try:
            with open('../Users/login_professor.csv', 'a') as login_data: #storing username and password
                csv.writer(login_data).writerow([username, password]) #In a real world application, I would hash the passwords and store them in a secure environment
        except Exception as e:
            print("Error:",e)
            messagebox.showerror("Account creation failed", "Could not create your account, please try again or contact administrator if the problem persists.")
        else:
            messagebox.showinfo("Account created successfully","Your account has been created successfully, Please login to continue.")
            login()


def login() -> None:
    canvas.delete("all")

    canvas.create_rectangle(150, 70, 450, 470, fill='white')
    canvas.create_rectangle(150, 70, 450, 150, fill='#72BF6A')

    back_button = tk.Button(canvas, text="← Back", font=("Arial", 12),
                            bg="#72BF6A", fg="white", borderwidth=0,
                            command=homepage)

    login_button = tk.Button(canvas, text="Login", font=("Arial", 14, "bold"),
                             bg='#46923C', fg='white', borderwidth=0, width=18, height=2,
                             command=lambda: check_login(user_name.get(),password.get()))

    user_name = tk.Entry(canvas, width=12, font=("Arial", 20, "bold"), bg='#ACD8A7')
    add_placeholder(user_name, "👤 Username")
    password = tk.Entry(canvas, width=12, font=("Arial", 20, "bold"), bg='#ACD8A7')
    add_placeholder(password, "🔑 Password")

    canvas.create_window(300, 210, window=user_name)
    canvas.create_window(300, 270, window=password)
    canvas.create_text(300, 110, text="Login", font=("Arial", 20, 'bold'))
    canvas.create_window(300, 430, window=back_button)
    canvas.create_window(300, 360, window=login_button)


def check_login(username,password) -> None:
    with open('../Users/login_professor.csv', 'r') as login_data:
        valid = False
        for row in csv.reader(login_data):
            if row[0] == username and row[1] == password:
                valid = True
                messagebox.showinfo("Login Successful", "You have logged in Successfully")
                logged_in(username)

        if not valid:
            messagebox.showerror("Login Failed", "Invalid Username or Password")



def logged_in(username) -> None:
    canvas.delete("all")

    canvas.create_rectangle(150, 70, 450, 470, fill='white')
    canvas.create_rectangle(150, 70, 450, 150, fill='#72BF6A')

    quit_button = tk.Button(canvas, text="Quit", font=("Arial", 12),
                            bg="#72BF6A", fg="white", borderwidth=0,
                            command=lambda: quit())

    user_name = tk.Label(canvas, text=f'Welcome {username}', width=12, height=2, font=("Arial", 15, "bold"),
                         bg='#ACD8A7')

    canvas.create_window(300, 280, window=user_name)
    canvas.create_window(300, 430, window=quit_button)
    canvas.create_text(300, 110, text="Company Page", font=("Arial", 20, 'bold'))

def gui() -> None:
    global root, canvas
    root = tk.Tk()
    root.geometry("600x600")
    root.configure(bg='#72BF6A')
    root.title("Welcome")
    root.resizable(False, False)

    header = tk.Label(root, text="XYZ Solutions", font=("Arial", 30, 'bold'), bg='#72BF6A', fg='white')
    header.pack()

    canvas = tk.Canvas(root, width=600, height=600, bg='#8BFF84', highlightthickness=0)
    canvas.pack()
    homepage()
    root.mainloop()

if __name__ == "__main__":
    gui()