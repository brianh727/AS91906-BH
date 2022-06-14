import sys

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
        start_widget = Start(self)
        self.widgets.addWidget(start_widget)
        self.setCentralWidget(self.widgets)
    
    def login(self):
        login_widget = Login(self)
        self.widgets.addWidget(login_widget)
        self.widgets.setCurrentWidget(login_widget)


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

        self.login_button.clicked.connect(self.parent().login)
        

class Login(QWidget):
    """Login menu for the user to log in"""
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.login_layout = QVBoxLayout()
        self.setLayout(self.login_layout)

        self.title = QLineEdit("Log into your account:")

        self.login_layout.addWidget(self.title)



def main():
    """Opens the main window"""
    application = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(application.exec_())

if __name__ == "__main__":
    main()