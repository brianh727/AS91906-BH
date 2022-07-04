import sys
import re
import sqlite3
import os.path

from PyQt5.QtCore import Qt, QFile
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QLabel,
                             QMainWindow, QVBoxLayout, QWidget,
                             QTabWidget, QTableWidget, QPushButton,
                             QLineEdit, QStackedWidget)


class Main(QMainWindow):
    """The main window for all the menu widgets of each section"""
    def __init__(self, parent=None):
        """Initialize the settings of the main window"""
        super(Main, self).__init__(parent)
        self.setWindowTitle("FastCards")
        self.widgets = QStackedWidget()
        self.start_widget = Start(self)
        self.widgets.addWidget(self.start_widget)
        self.setCentralWidget(self.widgets)

    def main_menu(self):
        """Switch to the first start main menu"""
        self.widgets.setCurrentWidget(self.start_widget)

    def login_menu(self):
        """Switch to the login menu"""
        self.login_widget = Login(self)
        self.widgets.addWidget(self.login_widget)
        self.widgets.setCurrentWidget(self.login_widget)

    def signup_menu(self):
        """Switch to the signup menu"""
        self.signup_widget = Signup(self)
        self.widgets.addWidget(self.signup_widget)
        self.widgets.setCurrentWidget(self.signup_widget)

    def flash_menu(self):
        """Switch to the flashcards menu"""
        self.flash_main_widget = Flash_Main(self)
        self.widgets.addWidget(self.flash_main_widget)
        self.widgets.setCurrentWidget(self.flash_main_widget)
    
    def test_menu(self):
        """Switch to the flashcards testing menu"""
        self.flash_test_widget = Flash_Test()
        self.flash_test_widget.show()

    def disable_window(self):
        """Disable main window (when popup created)"""
        pass


class Start(QWidget):
    """Start menu for the login buttons"""
    def __init__(self, parent=None):
        super(Start, self).__init__(parent)
        self.start_layout = QVBoxLayout()
        self.setLayout(self.start_layout)

        self.title_label = QLabel("FastCards by Brian Huang")
        self.login_button = QPushButton("Login")
        self.signup_button = QPushButton("Sign Up")
        self.guest_button = QPushButton("Guest Login")

        self.start_layout.addWidget(self.title_label)
        self.start_layout.addWidget(self.login_button)
        self.start_layout.addWidget(self.signup_button)
        self.start_layout.addWidget(self.guest_button)

        self.login_button.clicked.connect(self.parent().login_menu)
        self.signup_button.clicked.connect(self.parent().signup_menu)
        self.guest_button.clicked.connect(self.parent().flash_menu)


class Login(QWidget):
    """Login menu for the user to log in to an existing account"""
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.login_layout = QVBoxLayout()
        self.setLayout(self.login_layout)

        self.title = QLabel("Log into your account:")
        self.user_line = QLineEdit()
        self.user_line.setPlaceholderText("Username")
        self.pass_line = QLineEdit()
        self.pass_line.setPlaceholderText("Password")
        self.pass_line.setEchoMode(QLineEdit.Password)
        self.error_message = QLabel("")
        self.login_button = QPushButton("Login")
        self.return_button = QPushButton("Return")

        self.login_button.clicked.connect(self.login_check)
        self.return_button.clicked.connect(self.parent().main_menu)

        self.login_layout.addWidget(self.title)
        self.login_layout.addWidget(self.user_line)
        self.login_layout.addWidget(self.pass_line)
        self.login_layout.addWidget(self.error_message)

        self.buttons_layout = QHBoxLayout()
        self.login_layout.addLayout(self.buttons_layout)
        self.buttons_layout.addWidget(self.login_button)
        self.buttons_layout.addWidget(self.return_button)

    def login_check(self):
        """Check that the login details match those in the database"""
        acc = (self.user_line.text().lower(), self.pass_line.text())
        acc_con = create_con(acc_db)
        acc_cur = acc_con.cursor()
        # check whether a username exists
        acc_cur.execute("select exists(select 1 "
                        "from accounts where username = ?)", [acc[0]])
        [exists_user] = acc_cur.fetchone()

        # check if there is a username and password that matches together
        acc_cur.execute("select 1 from accounts where username = ?"
                        "and password = ?", acc)
        if not exists_user:
            self.error_message.setText("Username does not exist")
        elif not acc_cur.fetchone():
            self.error_message.setText("Password is incorrect")
        else:            
            self.parent().parent().flash_menu()


class Signup(QWidget):
    """Signup menu for user to create an account"""
    def __init__(self, parent=None):
        super(Signup, self).__init__(parent)
        self.signup_layout = QVBoxLayout()
        self.setLayout(self.signup_layout)

        self.title = QLabel("Create a new account:")
        self.user_line = QLineEdit()
        self.user_line.setPlaceholderText("Username")
        self.pass_line = QLineEdit()
        self.pass_line.setPlaceholderText("Password")
        self.pass_line.setEchoMode(QLineEdit.Password)
        self.pass_confirm_line = QLineEdit()
        self.pass_confirm_line.setPlaceholderText("Confirm Password")
        self.pass_confirm_line.setEchoMode(QLineEdit.Password)
        self.confirm_text = QLabel("")
        self.signup_button = QPushButton("Signup")
        self.return_button = QPushButton("Return")

        self.signup_button.clicked.connect(self.signup_check)
        self.return_button.clicked.connect(self.parent().main_menu)

        self.signup_layout.addWidget(self.title)
        self.signup_layout.addWidget(self.user_line)
        self.signup_layout.addWidget(self.pass_line)
        self.signup_layout.addWidget(self.pass_confirm_line)
        self.signup_layout.addWidget(self.confirm_text)

        self.buttons_layout = QHBoxLayout()
        self.signup_layout.addLayout(self.buttons_layout)
        self.buttons_layout.addWidget(self.signup_button)
        self.buttons_layout.addWidget(self.return_button)

    def signup_check(self):
        """Check the username and password inputs to create an account"""
        acc = (self.user_line.text().lower(), self.pass_line.text())
        acc_con = create_con(acc_db)
        acc_cur = acc_con.cursor()
        # check whether a username exists
        acc_cur.execute("select exists(select 1 "
                        "from accounts where username = ?)", [acc[0]])
        [exists_acc] = acc_cur.fetchone()

        if not 3 <= len(self.user_line.text()) <= 16:
            self.confirm_text.setText("Username must be between "
                                      "3 and 16 characters long")
        elif exists_acc:
            self.confirm_text.setText("Username already exists")
        elif not 8 <= len(self.pass_line.text()) <= 24:
            self.confirm_text.setText("Password must be between "
                                      "8 and 24 characters long")
        # check for 1 of each capital, lowercase and digit for 8 characters
        elif not re.search("(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}",
                           self.pass_line.text()):
            self.confirm_text.setText("Password does not meet "
                                      "the requirements")
        elif self.pass_line.text() != self.pass_confirm_line.text():
            self.confirm_text.setText("Passwords do not match")
        else:
            insert_account(acc_con, acc)
            self.parent().parent().flash_menu()


class Flash_Main(QWidget):
    """The main menu to access the flashcards"""
    def __init__(self, parent=None):
        super(Flash_Main, self).__init__(parent)
        self.flash_layout = QVBoxLayout()
        self.setLayout(self.flash_layout)
        
        self.title = QLabel("FastCards")
        self.test_button = QPushButton("Test flashcards")
        self.edit_button = QPushButton("Edit flashcards")
        self.create_button = QPushButton("Create flashcards")
        self.exit_button = QPushButton("Sign out and exit")

        self.flash_layout.addWidget(self.title)
        self.flash_layout.addWidget(self.test_button)
        self.flash_layout.addWidget(self.edit_button)
        self.flash_layout.addWidget(self.create_button)
        self.flash_layout.addWidget(self.exit_button)

        self.test_button.clicked.connect(self.parent().test_menu)
        self.exit_button.clicked.connect(sys.exit)


class Flash_Test(QWidget):
    """A new window which tests the flashcards"""
    def __init__(self):
        super().__init__()
        self.test_layout = QVBoxLayout()
        self.setLayout(self.test_layout)
        
        self.title = QLabel("Testing")
        self.test_layout.addWidget(self.title)


class Flash_Create(QWidget):
    """A new window where the user can create flashcards"""
    pass


class Flash_Edit(QWidget):
    """A new window where the user can edit their flashcards"""
    pass


acc_db = r"accounts.db"
flash_db = r"flashcards.db"

acc_table = """CREATE TABLE IF NOT EXISTS accounts (
                   id integer PRIMARY KEY,
                   username text NOT NULL,
                   password text NOT NULL);"""

flash_table = """CREATE TABLE IF NOT EXISTS flashcards (
                     id integer PRIMARY KEY,
                     frontside text NOT NULL,
                     backside text NOT NULL);"""

def insert_account(con, acc):
    """
    Insert the account into the accounts databases
    -------
    con: sqlite class
        SQLite connection to a database 
    acc: tuple
        Account username and password
    """
    sql = "INSERT INTO accounts(username, password) VALUES(?,?)"
    cur = con.cursor()
    cur.execute(sql, acc)
    con.commit()

def create_table(con, tab):
    """
    Create a table in a database
    -------
    con: sqlite class
        SQLite connection to a database
    tab: str
        SQLite table creation function
    """
    try:
        cur = con.cursor()
        cur.execute(tab)
    except Error as er:
        print(er)

def create_con(db):
    """
    Create a connection to a database
    -------
    db: str
        Filename and path of a database
    -------
    con: sqlite class
        Connection to an existing SQLite database
    """
    con = None
    try:
        con = sqlite3.connect(db)
        return con
    except Error as er:
        print(er)
    return con

def main():
    """Opens the main window and creates databases if needed"""
    acc_con = create_con(acc_db)
    if acc_con is not None:
        create_table(acc_con, acc_table)
    else:
        print("Couldn't create acc connection")

    flash_con = create_con(flash_db)
    if flash_con is not None:
        create_table(flash_con, flash_table)
    else:
        print("Couldn't create flash connection")

    application = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(application.exec_())

if __name__ == "__main__":
    main()
