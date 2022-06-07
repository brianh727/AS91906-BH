import sys

from PyQt5.QtCore import Qt, QFile
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QAction, QApplication, QHBoxLayout, QLabel, 
                             QMainWindow, QToolBar, QVBoxLayout, QWidget,
                             QTabWidget, QTableWidget, QAbstractItemView,
                             QPushButton, QGridLayout, QLineEdit)


class Main(QMainWindow):
    """Create the main window for all the widgets"""

    def __init__(self):
        """Initialize the settings of the main window"""
        super().__init__()
        self.setWindowTitle("FastCards")
        self.setCentralWidget(Start())


class Start(QWidget):
    def __init__(self):
        super().__init__()
        self.start_layout = QVBoxLayout()
        self.setLayout(self.start_layout)
        
        self.login_button = QPushButton("Login")
        self.signup_button = QPushButton("Sign Up")
        self.guest_button = QPushButton("Guest Login")

        self.start_layout.addWidget(self.login_button)
        self.start_layout.addWidget(self.signup_button)
        self.start_layout.addWidget(self.guest_button)


def main():
    """Opens the main window"""
    application = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(application.exec_())

if __name__ == "__main__":
    main()