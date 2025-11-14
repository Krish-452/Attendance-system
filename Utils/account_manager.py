import csv
import tkinter as tk
from tkinter import messagebox

def create_account(username: str, password: str) -> bool | None:
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
                return True
        except Exception as e:
            print("Error:",e)
            messagebox.showerror("Account creation failed", "Could not create your account, please try again or contact administrator if the problem persists.")
        else:
            messagebox.showinfo("Account created successfully","Your account has been created successfully, Please login to continue.")
    return None


def login(username,password,user) -> bool | None:
    if user == "prof":
        file_path = "../Users/login_professor.csv"
    elif user == "TA":
        file_path = "../Users/login_TA.csv"
    else:
        file_path = "../Users/login_admin.csv"

    with open(file_path, 'r') as login_data:
        valid = False
        for row in csv.reader(login_data):
            if row[0] == username and row[1] == password:
                valid = True
                messagebox.showinfo("Login Successful", "You have logged in Successfully")
                return True

        if not valid:
            messagebox.showerror("Login Failed", "Invalid Username or Password")
        return None