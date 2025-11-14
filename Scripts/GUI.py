import csv
import tkinter as tk
from tkinter import messagebox
import Utils.account_manager as account_manager

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

    login_prof = tk.Button(root, text="Login as Professor", font=("Arial", 14, "bold"), bg='#46923C', fg='white', borderwidth=0,
                       activebackground='#276221', activeforeground='white', width=18, height=2, command=lambda: login("prof"))
    login_TA = tk.Button(root, text="Login as TA", font=("Arial", 14, "bold"), bg='#46923C', fg='white', borderwidth=0,
                             activebackground='#276221', activeforeground='white', width=18, height=2, command=lambda: login("TA"))
    login_admin = tk.Button(root, text="Login as Admin", font=("Arial", 14, "bold"), bg='#46923C', fg='white', borderwidth=0,
                       activebackground='#276221', activeforeground='white', width=18, height=2, command=lambda: login("admin"))
    quit_button = tk.Button(canvas, text="Quit", font=("Arial", 12), bg="#72BF6A", fg="white", borderwidth=0, command=lambda: quit())

    canvas.create_text(300, 110, text="Welcome", font=("Arial", 20, 'bold'))
    canvas.create_window(300, 210, window=login_prof)
    canvas.create_window(300, 290, window=login_TA)
    canvas.create_window(300, 370, window=login_admin)
    canvas.create_window(300, 440, window=quit_button)


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
                                      command=lambda: account_manager.create_account(user_name.get(), password.get()))

    canvas.create_text(300, 110, text="Create Account", font=("Arial", 20, 'bold'))
    canvas.create_window(300, 210, window=user_name)
    canvas.create_window(300, 270, window=password)
    canvas.create_window(300, 430, window=back_button)
    canvas.create_window(300, 360, window=create_account_button)





def login(user) -> None:
    canvas.delete("all")

    canvas.create_rectangle(150, 70, 450, 470, fill='white')
    canvas.create_rectangle(150, 70, 450, 150, fill='#72BF6A')

    back_button = tk.Button(canvas, text="← Back", font=("Arial", 12),
                            bg="#72BF6A", fg="white", borderwidth=0,
                            command=homepage)

    login_button = tk.Button(canvas, text="Login", font=("Arial", 14, "bold"),
                             bg='#46923C', fg='white', borderwidth=0, width=18, height=2,
                             command=lambda: account_manager.login(user_name.get(),password.get(),user))

    user_name = tk.Entry(canvas, width=12, font=("Arial", 20, "bold"), bg='#ACD8A7')
    add_placeholder(user_name, "👤 Username")
    password = tk.Entry(canvas, width=12, font=("Arial", 20, "bold"), bg='#ACD8A7')
    add_placeholder(password, "🔑 Password")

    canvas.create_window(300, 210, window=user_name)
    canvas.create_window(300, 270, window=password)
    canvas.create_text(300, 110, text="Login", font=("Arial", 20, 'bold'))
    canvas.create_window(300, 430, window=back_button)
    canvas.create_window(300, 360, window=login_button)



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



if __name__ == "__main__":
    gui()