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
        pass


def main():
    """Opens the main window"""
    application = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(application.exec_())

if __name__ == "__main__":
    main()