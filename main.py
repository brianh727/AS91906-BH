import sys
import re
import sqlite3

from PyQt5.QtCore import Qt, QFile
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QAction, QApplication, QHBoxLayout, QLabel, 
                             QMainWindow, QToolBar, QVBoxLayout, QWidget,
                             QTabWidget, QTableWidget, QAbstractItemView,
                             QPushButton, QGridLayout, QLineEdit, QStackedWidget)


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
        self.widgets.setCurrentWidget(self.start_widget)
    
    def login_menu(self):
        self.login_widget = Login(self)
        self.widgets.addWidget(self.login_widget)
        self.widgets.setCurrentWidget(self.login_widget)

    def signup_menu(self):
        self.signup_widget = Signup(self)
        self.widgets.addWidget(self.signup_widget)
        self.widgets.setCurrentWidget(self.signup_widget)


class Start(QWidget):
    """Start menu for the login buttons"""
    def __init__(self, parent=None):
        super(Start, self).__init__(parent)
        self.start_layout = QVBoxLayout()
        self.setLayout(self.start_layout)
        
        self.login_button = QPushButton("Login")
        self.signup_button = QPushButton("Sign Up")
        self.guest_button = QPushButton("Guest Login")

        self.start_layout.addWidget(self.login_button)
        self.start_layout.addWidget(self.signup_button)
        self.start_layout.addWidget(self.guest_button)

        self.login_button.clicked.connect(self.parent().login_menu)
        self.signup_button.clicked.connect(self.parent().signup_menu)
        

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
        self.login_button = QPushButton("Login")
        self.return_button = QPushButton("Return")

        self.login_button.clicked.connect(self.login_check)
        self.return_button.clicked.connect(self.parent().main_menu)

        self.login_layout.addWidget(self.title)
        self.login_layout.addWidget(self.user_line)
        self.login_layout.addWidget(self.pass_line)

        self.buttons_layout = QHBoxLayout()
        self.login_layout.addLayout(self.buttons_layout)
        self.buttons_layout.addWidget(self.login_button)
        self.buttons_layout.addWidget(self.return_button)

    def login_check(self):
        """Check that the login details match those in the database"""
        pass


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
        if not 3 <= len(self.user_line.text()) <= 16:
            self.confirm_text.setText("Username must be between "
                                      "3 and 16 characters long")
        elif not 4 <= len(self.pass_line.text()) <= 20:
            self.confirm_text.setText("Password must be between "
                                      "4 and 20 characters long")
        elif self.pass_line.text() != self.pass_confirm_line.text():
            self.confirm_text.setText("Passwords do not match")


def main():
    con = sqlite3.connect("accounts.db")
    """Opens the main window"""
    application = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(application.exec_())


if __name__ == "__main__":
    main()