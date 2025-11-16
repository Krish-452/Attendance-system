from typing import Dict, Optional
import tkinter as tk
from tkinter import messagebox
import Utils.account_manager as account_manager
import Utils.class_manager as class_manager

# Declaring colours and fonts for multiple uses
BG_ROOT = "#72BF6A"
CANVAS_BG = "#8BFF84"
PANEL_FILL = "white"
PANEL_HEADER = "#72BF6A"
BUTTON_BG = "#46923C"
BUTTON_ACTIVE = "#276221"
ENTRY_BG = "#ACD8A7"
FONT_HEADER = ("Arial", 20, "bold")
FONT_TITLE = ("Arial", 30, "bold")
FONT_BUTTON = ("Arial", 14, "bold")
FONT_SMALL = ("Arial", 12)


# Ghost text for username and password fields
def add_placeholder(entry: tk.Entry, placeholder: str, color: str = "grey") -> None:
    def on_focus_in(event) -> None:
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg="black")

    def on_focus_out(event) -> None:
        if not entry.get():
            entry.insert(0, placeholder)
            entry.config(fg=color)

    entry.insert(0, placeholder)
    entry.config(fg=color)
    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)


# Defining the main app as a class
class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Attendance System")
        self.geometry("600x600")
        self.configure(bg=BG_ROOT)
        self.resizable(False, False)

        # container for pages
        container = tk.Frame(self, bg=BG_ROOT)
        container.pack(fill="both", expand=True)

        # store pages
        self.frames: Dict[str, tk.Frame] = {}
        self.current_user_type: Optional[str] = None
        self.current_username: Optional[str] = None

        # Page list for switching frames
        for P in (
                HomePage,
                LoginPage,
                CreateAccountPage,
                DeleteAccountPage,
                AdminDashboard,
                ProfessorDashboard,
                TADashboard,
        ):
            page_name = P.__name__
            frame = P(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        header = tk.Label(self, text="Attendance System", font=FONT_TITLE, bg=BG_ROOT, fg="white")
        header.pack(pady=(0, 10))

        self.show_frame("HomePage")  # Starting on the HomePage

    def show_frame(self, page_name: str) -> None: # To switch between pages using the predefined list above
        frame = self.frames[page_name]

        if hasattr(frame, "on_show"): #This part makes sure that the Class list gets refreshed when a professor or TA logs in
            frame.on_show()

        frame.tkraise()

    def show_login_for(self, user_type: str) -> None:
        self.current_user_type = user_type  # As the program uses a common login page, we must define the user for different logins
        login_page: LoginPage = self.frames["LoginPage"]  # type: ignore
        login_page.set_user_type(user_type)
        self.show_frame("LoginPage")

    def on_login_success(self, username: str, user_type: str) -> None:  # Different dashboards for different users
        self.current_username = username
        if user_type == "admin":
            self.show_frame("AdminDashboard")
        elif user_type == "prof":
            self.show_frame("ProfessorDashboard")
        else:
            self.show_frame("TADashboard")


# We used a canvas styled on a frame
# Canvas allows better customization
# While the frame allows for seamless transitions
class StyledCanvasFrame(tk.Frame):
    def __init__(self, parent: tk.Widget, controller: App) -> None:
        super().__init__(parent, bg=BG_ROOT)
        self.controller = controller
        self.canvas = tk.Canvas(self, width=600, height=520, bg=CANVAS_BG, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_rectangle(150, 70, 450, 470, fill=PANEL_FILL, outline="")
        self.canvas.create_rectangle(150, 70, 450, 150, fill=PANEL_HEADER, outline="")

    def place_title(self, text: str) -> None:
        self.canvas.create_text(300, 110, text=text, font=FONT_HEADER)


class HomePage(StyledCanvasFrame):
    def __init__(self, parent: tk.Widget, controller: App) -> None:
        super().__init__(parent, controller)
        self.place_title("Welcome")

        login_prof = tk.Button(self, text="Login as Professor", font=FONT_BUTTON, bg=BUTTON_BG, fg="white",
                               borderwidth=0, activebackground=BUTTON_ACTIVE, activeforeground="white",
                               width=18, height=2, command=lambda: controller.show_login_for("prof"))
        login_TA = tk.Button(self, text="Login as TA", font=FONT_BUTTON, bg=BUTTON_BG, fg="white",
                             borderwidth=0, activebackground=BUTTON_ACTIVE, activeforeground="white",
                             width=18, height=2, command=lambda: controller.show_login_for("TA"))
        login_admin = tk.Button(self, text="Login as Admin", font=FONT_BUTTON, bg=BUTTON_BG, fg="white",
                                borderwidth=0, activebackground=BUTTON_ACTIVE, activeforeground="white",
                                width=18, height=2, command=lambda: controller.show_login_for("admin"))
        quit_button = tk.Button(self, text="Quit", font=FONT_SMALL, bg=BG_ROOT, fg="white", borderwidth=0,
                                command=self.controller.quit)

        self.canvas.create_window(300, 210, window=login_prof)
        self.canvas.create_window(300, 290, window=login_TA)
        self.canvas.create_window(300, 370, window=login_admin)
        self.canvas.create_window(300, 430, window=quit_button)


class LoginPage(StyledCanvasFrame):
    def __init__(self, parent: tk.Widget, controller: App) -> None:
        super().__init__(parent, controller)
        self._user_type: Optional[str] = None
        self.place_title("Login")

        self.username_entry = tk.Entry(self, width=18, font=("Arial", 18, "bold"), bg=ENTRY_BG)
        add_placeholder(self.username_entry, "👤 Username")
        self.password_entry = tk.Entry(self, width=18, font=("Arial", 18, "bold"), bg=ENTRY_BG)
        add_placeholder(self.password_entry, "🔑 Password")

        self.login_button = tk.Button(self, text="Login", font=FONT_BUTTON, bg=BUTTON_BG, fg="white",
                                      borderwidth=0, activebackground=BUTTON_ACTIVE, activeforeground="white",
                                      width=18, height=2, command=self.attempt_login)
        self.back_button = tk.Button(self, text="← Back", font=FONT_SMALL, bg=BG_ROOT, fg="white", borderwidth=0,
                                     command=lambda: self.back())

        self.canvas.create_window(300, 210, window=self.username_entry)
        self.canvas.create_window(300, 270, window=self.password_entry)
        self.canvas.create_window(300, 360, window=self.login_button)
        self.canvas.create_window(300, 430, window=self.back_button)

    def clear_fields(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        add_placeholder(self.username_entry, "👤 Username")
        add_placeholder(self.password_entry, "🔑 Password")
        self.controller.focus_set()

    def back(self):
        self.clear_fields()
        self.controller.show_frame("HomePage")

    def set_user_type(self, user_type: str) -> None:
        self._user_type = user_type

        display = {"prof": "Login (Professor)", "TA": "Login (TA)", "admin": "Login (Admin)"}
        self.canvas.create_rectangle(150, 70, 450, 150, fill=PANEL_HEADER, outline="")
        self.canvas.create_text(300, 110, text=display.get(user_type, "Login"), font=FONT_HEADER)

    def attempt_login(self) -> None:
        username = self.username_entry.get()
        password = self.password_entry.get()
        user_type = self._user_type or "prof"

        if account_manager.login(username, password, user_type):
            self.controller.on_login_success(username, user_type)
            messagebox.showinfo("Login Successful", "You have logged in Successfully")
            self.clear_fields()
        else:
            messagebox.showerror("Login Failed", "Invalid Username or Password")


class CreateAccountPage(StyledCanvasFrame):
    def __init__(self, parent: tk.Widget, controller: App) -> None:
        super().__init__(parent, controller)
        self.place_title("Create Account")

        self.username_entry = tk.Entry(self, width=18, font=("Arial", 18, "bold"), bg=ENTRY_BG)
        add_placeholder(self.username_entry, "👤 Username")
        self.password_entry = tk.Entry(self, width=18, font=("Arial", 18, "bold"), bg=ENTRY_BG)
        add_placeholder(self.password_entry, "🔑 Password")

        self.create_prof_acc = tk.Button(self, text="For Prof.", font=FONT_BUTTON, bg=BUTTON_BG, fg="white",
                                         borderwidth=0, activebackground=BUTTON_ACTIVE, activeforeground="white",
                                         width=10, height=2, command=lambda: self.attempt_create("prof"))
        self.create_TA_acc = tk.Button(self, text="For TA", font=FONT_BUTTON, bg=BUTTON_BG, fg="white",
                                       borderwidth=0, activebackground=BUTTON_ACTIVE, activeforeground="white",
                                       width=10, height=2, command=lambda: self.attempt_create("TA"))
        self.back_button = tk.Button(self, text="← Back", font=FONT_SMALL, bg=BG_ROOT, fg="white", borderwidth=0,
                                     command=lambda: self.back())

        self.canvas.create_window(300, 210, window=self.username_entry)
        self.canvas.create_window(300, 270, window=self.password_entry)
        self.canvas.create_window(230, 360, window=self.create_prof_acc)
        self.canvas.create_window(370, 360, window=self.create_TA_acc)
        self.canvas.create_window(300, 430, window=self.back_button)

    def clear_fields(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        add_placeholder(self.username_entry, "👤 Username")
        add_placeholder(self.password_entry, "🔑 Password")
        self.controller.focus_set()

    def back(self):
        self.clear_fields()
        self.controller.show_frame("AdminDashboard")

    def attempt_create(self, account_type: str) -> None:
        username: str = self.username_entry.get()
        password: str = self.password_entry.get()

        if account_manager.create_account(username, password, account_type):
            messagebox.showinfo("Account created", "Account created successfully.")
            self.controller.show_frame("AdminDashboard")
            self.clear_fields()
        else:
            messagebox.showwarning("Account Creation failed", "Account could not be created, please try again.")


class DeleteAccountPage(StyledCanvasFrame):
    def __init__(self, parent: tk.Widget, controller: App) -> None:
        super().__init__(parent, controller)
        self.place_title("Delete Account")

        self.account_type: tk.StringVar = tk.StringVar()
        self.account_type.set("")

        self.user_list_frame = None  # Pre-declaring the list so we don't get any error while trying to delete the old list in show accounts
        self.user_list = None  # Not necessary but makes the program more reliable

        self.select_prof = tk.Radiobutton(self, text="Professor", font=FONT_BUTTON, bg='white', value="prof",
                                          variable=self.account_type, command=self.show_accounts)
        self.select_TA = tk.Radiobutton(self, text="TA", font=FONT_BUTTON, bg='white', value="TA",
                                        variable=self.account_type, command=self.show_accounts)
        self.delete_button = tk.Button(self, text="Delete", font=FONT_BUTTON, bg=BUTTON_BG, fg="white",
                                       borderwidth=0, activebackground=BUTTON_ACTIVE, activeforeground="white",
                                       width=18, height=2, command=self.attempt_delete)
        self.back_button = tk.Button(self, text="← Back", font=FONT_SMALL, bg=BG_ROOT, fg="white", borderwidth=0,
                                     command=lambda: self.controller.show_frame("AdminDashboard"))

        self.canvas.create_window(300, 370, window=self.delete_button)
        self.canvas.create_window(250, 180, window=self.select_prof)
        self.canvas.create_window(380, 180, window=self.select_TA)
        self.canvas.create_window(300, 430, window=self.back_button)

    def show_accounts(self) -> None:
        users = account_manager.retrieve_accounts(self.account_type.get().strip())

        if self.user_list_frame:
            self.user_list_frame.destroy()  # Destroy any previously loaded list

        self.user_list_frame = tk.Frame(self, bg='white')  # creating a frame to hold both list and scroll bar

        scrollbar = tk.Scrollbar(self.user_list_frame, orient="vertical")
        self.user_list = tk.Listbox(self.user_list_frame, width=17, height=5, font=("Arial", 12, "bold"),
                                    yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.user_list.yview)

        scrollbar.pack(side="right", fill="y")
        self.user_list.pack(side="left", fill="both", expand=True)

        for i, user in enumerate(users, start=1):  # Enumerate to create a numbered list (looks better)
            self.user_list.insert(tk.END, f"{i}. {user}")

        # Place the entire frame on canvas
        self.canvas.create_window(300, 260, window=self.user_list_frame)

    def attempt_delete(self) -> None:
        selection = self.user_list.curselection()

        if not selection:
            messagebox.showwarning("Warning", "No account selected.")
        else:
            if account_manager.delete_account(selection[0], self.account_type.get().strip()):
                messagebox.showinfo("Account deleted", "Account deleted successfully.")
            else:
                messagebox.showwarning("Warning", "Account could not be deleted, please try again.")
            self.show_accounts()


class AdminDashboard(StyledCanvasFrame):
    def __init__(self, parent: tk.Widget, controller: App) -> None:
        super().__init__(parent, controller)
        self.place_title("Admin Dashboard")

        create_account_btn = tk.Button(self, text="Create Account", font=FONT_BUTTON, bg=BUTTON_BG, fg="white",
                                       borderwidth=0, activebackground=BUTTON_ACTIVE, activeforeground="white",
                                       width=18, height=2, command=lambda: controller.show_frame("CreateAccountPage"))
        delete_account_btn = tk.Button(self, text="Delete Account", font=FONT_BUTTON, bg=BUTTON_BG, fg="white",
                                       borderwidth=0, activebackground=BUTTON_ACTIVE, activeforeground="white",
                                       width=18, height=2, command=lambda: controller.show_frame("DeleteAccountPage"))
        logout_btn = tk.Button(self, text="Logout", font=FONT_SMALL, bg=BG_ROOT, fg="white", borderwidth=0,
                               command=lambda: controller.show_frame("HomePage"))

        self.canvas.create_window(300, 240, window=create_account_btn)
        self.canvas.create_window(300, 340, window=delete_account_btn)
        self.canvas.create_window(300, 430, window=logout_btn)


class ProfessorDashboard(StyledCanvasFrame):
    def __init__(self, parent: tk.Widget, controller: App) -> None:
        super().__init__(parent, controller)
        self.place_title("Professor Dashboard")

        self.class_list_frame = None  # Pre-declaring the list so we don't get any error while trying to delete the old list in show accounts
        self.class_list = None  # Not necessary but makes the program more reliable

        logout_btn = tk.Button(self, text="Logout", font=FONT_SMALL, bg=BG_ROOT, fg="white", borderwidth=0,
                               command=lambda: controller.show_frame("HomePage"))
        self.start_button = tk.Button(self, text="View", font=FONT_BUTTON, bg=BUTTON_BG, fg="white",
                                      borderwidth=0, activebackground=BUTTON_ACTIVE, activeforeground="white",
                                      width=18, height=2, command=lambda: self.show_classes())

        self.canvas.create_window(300, 430, window=logout_btn)
        self.canvas.create_window(300, 370, window=self.start_button)
        self.show_classes()

    def on_show(self):  # Refreshes the list everytime the frame gets loaded
        self.show_classes()

    def show_classes(self) -> None:  # Almost the same as show accounts in DeleteAccountPage
        classes = list((list(value.values())[0: 2] for value in
                        class_manager.retrieve_classes(self.controller.current_username, "Professor")))

        if self.class_list_frame:
            self.class_list_frame.destroy()  # Destroy any previously loaded list

        self.class_list_frame = tk.Frame(self, bg='white')  # creating a frame to hold both list and scroll bar

        scrollbar = tk.Scrollbar(self.class_list_frame, orient="vertical")
        self.class_list = tk.Listbox(self.class_list_frame, width=25, height=7, font=("Arial", 12, "bold"),
                                     yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.class_list.yview)

        scrollbar.pack(side="right", fill="y")
        self.class_list.pack(side="left", fill="both", expand=True)

        for i in range(len(classes)):
            self.class_list.insert(tk.END, f"{classes[i][0]}: {classes[i][1]}")

        # Place the entire frame on canvas
        self.canvas.create_window(300, 245, window=self.class_list_frame)


class TADashboard(StyledCanvasFrame):
    def __init__(self, parent: tk.Widget, controller: App) -> None:
        super().__init__(parent, controller)
        self.place_title("TA Dashboard")

        self.class_list_frame = None  # Pre-declaring the list so we don't get any error while trying to delete the old list in show accounts
        self.class_list = None  # Not necessary but makes the program more reliable

        logout_btn = tk.Button(self, text="Logout", font=FONT_SMALL, bg=BG_ROOT, fg="white", borderwidth=0,
                               command=lambda: controller.show_frame("HomePage"))
        self.start_button = tk.Button(self, text="View", font=FONT_BUTTON, bg=BUTTON_BG, fg="white",
                                      borderwidth=0, activebackground=BUTTON_ACTIVE, activeforeground="white",
                                      width=18, height=2, command=lambda: self.show_classes())

        self.canvas.create_window(300, 430, window=logout_btn)
        self.canvas.create_window(300, 370, window=self.start_button)
        self.show_classes()

    def on_show(self): #Refreshes the list everytime the frame gets loaded
        self.show_classes()

    def show_classes(self) -> None: #Almost the same as show accounts in DeleteAccountPage
        classes = list((list(value.values())[0: 2] for value in class_manager.retrieve_classes(self.controller.current_username, "TA")))

        if self.class_list_frame:
            self.class_list_frame.destroy()  # Destroy any previously loaded list

        self.class_list_frame = tk.Frame(self, bg='white')  # creating a frame to hold both list and scroll bar

        scrollbar = tk.Scrollbar(self.class_list_frame, orient="vertical")
        self.class_list = tk.Listbox(self.class_list_frame, width=25, height=7, font=("Arial", 12, "bold"),
                                    yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.class_list.yview)

        scrollbar.pack(side="right", fill="y")
        self.class_list.pack(side="left", fill="both", expand=True)

        for i in range(len(classes)):
            self.class_list.insert(tk.END, f"{classes[i][0]}: {classes[i][1]}")

        # Place the entire frame on canvas
        self.canvas.create_window(300, 245, window=self.class_list_frame)


if __name__ == "__main__":
    app = App()
    app.mainloop()
