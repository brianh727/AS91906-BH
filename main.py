import sys
import re
import sqlite3
import os.path
import random

from PyQt5.QtCore import Qt, QFile
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QLabel,
                             QMainWindow, QVBoxLayout, QWidget,
                             QTabWidget, QTableWidget, QPushButton,
                             QLineEdit, QStackedWidget, QMessageBox,
                             QStackedLayout, QTableWidgetItem, QHeaderView,
                             QAbstractItemView)


class Main(QMainWindow):
    """The main window for all the menu widgets of each section"""
    def __init__(self, parent=None):
        """Initialize the settings of the main window"""
        super(Main, self).__init__(parent)
        self.setWindowTitle("FastCards")
        self.setFixedSize(300, 200)
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
        """Create the flashcard testing menu"""
        self.flash_test_widget = Flash_Test()
        self.flash_test_widget.show()

    def create_menu(self):
        """Create the flashcard creation menu"""
        self.flash_create_widget = Flash_Create()
        self.flash_create_widget.show()

    def remove_menu(self):
        """Create the flashcard removal menu"""
        self.flash_remove_widget = Flash_Remove()
        self.flash_remove_widget.show()


class Start(QWidget):
    """Start menu for the login buttons"""
    def __init__(self, parent=None):
        super(Start, self).__init__(parent)
        self.start_layout = QVBoxLayout()
        self.setLayout(self.start_layout)

        self.title_label = QLabel("FastCards by Brian Huang")
        self.title_label.setStyleSheet("font-weight: bold")
        self.login_button = QPushButton("Login")
        self.signup_button = QPushButton("Sign Up")
        self.guest_button = QPushButton("Guest Login")
        self.exit_button = QPushButton("Exit")

        self.start_layout.addWidget(self.title_label)
        self.start_layout.addWidget(self.login_button)
        self.start_layout.addWidget(self.signup_button)
        self.start_layout.addWidget(self.guest_button)
        self.start_layout.addWidget(self.exit_button)

        self.login_button.clicked.connect(self.parent().login_menu)
        self.signup_button.clicked.connect(self.parent().signup_menu)
        self.guest_button.clicked.connect(self.parent().flash_menu)
        self.exit_button.clicked.connect(sys.exit)


class Login(QWidget):
    """Login menu for the user to log in to an existing account"""
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.login_layout = QVBoxLayout()
        self.setLayout(self.login_layout)

        self.title = QLabel("Log into your account:")
        self.title.setStyleSheet("font-weight: bold")
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
        self.title.setStyleSheet("font-weight: bold")
        self.user_line = QLineEdit()
        self.user_line.setPlaceholderText("Username")
        self.pass_line = QLineEdit()
        self.pass_line.setPlaceholderText("Password (*hover)")
        self.pass_line.setEchoMode(QLineEdit.Password)
        self.pass_line.setToolTip("Password must be 8-24 characters long \n"
                                  "And must contain \n"
                                  " - atleast 1 capital letter \n"
                                  " - atleast 1 lowercase letter \n"
                                  " - atleast 1 number")
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

        self.title = QLabel("FastCards Main Menu")
        self.title.setStyleSheet("font-weight: bold")
        self.test_button = QPushButton("Test flashcards")
        self.remove_button = QPushButton("Remove flashcards")
        self.create_button = QPushButton("Create flashcards")
        self.exit_button = QPushButton("Sign out and exit")

        self.flash_layout.addWidget(self.title)
        self.flash_layout.addWidget(self.test_button)
        self.flash_layout.addWidget(self.remove_button)
        self.flash_layout.addWidget(self.create_button)
        self.flash_layout.addWidget(self.exit_button)

        self.test_button.clicked.connect(self.flash_check)
        self.remove_button.clicked.connect(self.parent().remove_menu)
        self.create_button.clicked.connect(self.parent().create_menu)
        self.exit_button.clicked.connect(sys.exit)

    def flash_check(self):
        """
        Check whether there are flashcards to be tested
        Show warning if there aren't flashcards
        Open flashcard testing menu if there are
        """
        flash_con = create_con(flash_db)
        flash_cur = flash_con.cursor()
        flash_cur.execute("SELECT frontside, backside FROM flashcards")
        if not flash_cur.fetchall():  # create a popup if there are no cards
            warning_popup = QMessageBox()
            warning_popup.setIcon(QMessageBox.Warning)
            warning_popup.setWindowTitle("No FastCards")
            warning_popup.setText("There are no FastCards to test... \n"
                                  "Please create some FastCards first.")
            x = warning_popup.exec_()
        else:
            self.parent().parent().test_menu()


class Flash_Test(QWidget):
    """
    A new window which tests the flashcards
    A new set of flashcards will be created from the database every time
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FastCard Test")
        test_layout = QVBoxLayout()
        self.setFixedSize(400, 0)
        self.setLayout(test_layout)
        self.setWindowModality(Qt.ApplicationModal)
        self.flashcards = self.create_flash_list()
        self.current_card = self.flashcards[0]

        title = QLabel("Test FastCards")
        title.setStyleSheet("font-weight: bold")
        front_label = QLabel("Frontside:")
        self.flash_frontside = QLabel(self.current_card[0])
        flash_separator = QLabel("---")
        back_label = QLabel("Backside:")
        self.flash_backside = QLabel("???")

        show_button = QPushButton("Show Backside")
        show_button.clicked.connect(self.show_backside)
        good_button = QPushButton("Know")
        good_button.clicked.connect(self.good_response)
        bad_button = QPushButton("Don't Know")
        bad_button.clicked.connect(self.bad_response)
        good_button.setToolTip("For if you knew the answer \n"
                               "You will not be tested on this card again.")
        bad_button.setToolTip("For if you didn't know the answer \n"
                              "You will be retested on this card soon.")

        self.buttons_widget = QStackedWidget()
        self.show_container = QWidget()
        self.answer_container = QWidget()
        show_layout = QHBoxLayout()
        answer_layout = QHBoxLayout()
        self.show_container.setLayout(show_layout)
        self.answer_container.setLayout(answer_layout)
        self.buttons_widget.addWidget(self.show_container)
        self.buttons_widget.addWidget(self.answer_container)

        show_layout.addWidget(show_button)
        answer_layout.addWidget(good_button)
        answer_layout.addWidget(bad_button)
        self.buttons_widget.setCurrentWidget(self.show_container)

        test_layout.addWidget(title)
        test_layout.addWidget(front_label)
        test_layout.addWidget(self.flash_frontside)
        test_layout.addWidget(flash_separator)
        test_layout.addWidget(back_label)
        test_layout.addWidget(self.flash_backside)
        test_layout.addWidget(self.buttons_widget)

    def create_flash_list(self):
        """
        Create a list of flashcards to be tested and randomise order
        List will be created with flashcards in flashcard database
        """
        flash_con = create_con(flash_db)
        flash_cur = flash_con.cursor()
        flash_cur.execute("SELECT frontside, backside FROM flashcards")
        flashcards = flash_cur.fetchall()
        random.shuffle(flashcards)
        return flashcards

    def show_backside(self):
        """Show the backside of the current flashcard"""
        self.flash_backside.setText(self.current_card[1])
        self.buttons_widget.setCurrentWidget(self.answer_container)

    def good_response(self):
        """
        Remove the current card from the list and show next card
        Card will not be tested again in the testing session
        """
        # will completely remove current card from test
        if len(self.flashcards) > 1:
            self.flashcards.pop(0)
            self.current_card = self.flashcards[0]
            self.flash_frontside.setText(self.current_card[0])
            self.flash_backside.setText("???")
            self.buttons_widget.setCurrentWidget(self.show_container)
        else:
            popup = QMessageBox()
            popup.setWindowTitle("FastCards Complete")
            popup.setIcon(QMessageBox.Information)
            popup.setText("You have finished testing yourself on your cards")
            x = popup.exec_()
            self.close()

    def bad_response(self):
        """
        Move the current card down the list and show next card
        Repeat current card if there aren't any other ones available
        """
        if len(self.flashcards) > 1:
            # new position of card is random from next to end
            new_position = random.randint(1, len(self.flashcards))
            self.flashcards.insert(new_position, self.flashcards.pop(0))
            self.current_card = self.flashcards[0]
            self.flash_frontside.setText(self.current_card[0])
            self.flash_backside.setText("???")
            self.buttons_widget.setCurrentWidget(self.show_container)
        else:  # repeat current card if there are no other
            self.flash_backside.setText("???")
            self.buttons_widget.setCurrentWidget(self.show_container)


class Flash_Create(QWidget):
    """A new window where the user can create flashcards"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FastCard Create")
        create_layout = QVBoxLayout()
        self.setLayout(create_layout)
        self.setFixedSize(400, 0)
        self.setWindowModality(Qt.ApplicationModal)

        title = QLabel("Create FastCards")
        title.setStyleSheet("font-weight: bold")
        front_label = QLabel("FastCard Front")
        self.front_input = QLineEdit()
        self.front_input.setPlaceholderText("Front")
        back_label = QLabel("FastCard Back")
        self.back_input = QLineEdit()
        self.back_input.setPlaceholderText("Back")
        hint_label = QLabel("FastCard Hint")
        create_button = QPushButton("Create FastCard")
        back_button = QPushButton("Return")

        create_layout.addWidget(title)
        create_layout.addStretch()
        create_layout.addWidget(front_label)
        create_layout.addWidget(self.front_input)
        create_layout.addWidget(back_label)
        create_layout.addWidget(self.back_input)

        buttons_layout = QHBoxLayout()
        create_layout.addLayout(buttons_layout)
        buttons_layout.addWidget(create_button)
        buttons_layout.addWidget(back_button)
        create_button.clicked.connect(self.create_card)
        back_button.clicked.connect(self.close)

    def create_card(self):
        """
        Create the flashcard with inputs providided
        Remove current inputs to make space for next flashcard
        """
        popup_box = QMessageBox()
        popup_box.setWindowTitle("FastCard Confirmation")
        popup_box.setIcon(QMessageBox.Information)
        if not self.front_input.text():
            popup_box.setText("Please input a front side for the FastCard")
        elif not self.back_input.text():
            popup_box.setText("Please input a back side for the FastCard")
        else:
            flashcard = (self.front_input.text(), self.back_input.text())
            flash_con = create_con(flash_db)
            insert_flashcard(flash_con, flashcard)
            # Remove the current inputs to make space for next
            self.front_input.clear()
            self.back_input.clear()
            popup_box.setText("FastCard created")
        x = popup_box.exec_()


class Flash_Remove(QWidget):
    """A new window where the user can remove their flashcards"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FastCards Remove")
        remove_layout = QVBoxLayout()
        self.setLayout(remove_layout)
        self.setFixedSize(400, 250)
        self.setWindowModality(Qt.ApplicationModal)

        # create list of flashcards from database to be put into table
        flash_con = create_con(flash_db)
        flash_cur = flash_con.cursor()
        flash_cur.execute("SELECT frontside, backside FROM flashcards")
        flashcards = flash_cur.fetchall()

        title = QLabel("Remove FastCards")
        title.setStyleSheet("font-weight: bold")
        self.cards_table = QTableWidget(len(flashcards), 1)
        remove_button = QPushButton("Remove FastCard")
        remove_button.clicked.connect(self.remove_card)

        # remove visible headers from table
        self.cards_table.horizontalHeader().setVisible(False)
        self.cards_table.verticalHeader().setVisible(False)
        # set interaction options of table
        self.cards_table.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.cards_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.cards_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.cards_table.selectRow(0)
        self.cards_header = self.cards_table.horizontalHeader()
        self.cards_header.setSectionResizeMode(0, QHeaderView.Stretch)
        # fills table with all flashcard frontsides
        for row, card in enumerate(flashcards):
            self.cards_table.setItem(row, 0, QTableWidgetItem(card[0]))

        remove_layout.addWidget(title)
        remove_layout.addWidget(self.cards_table)
        remove_layout.addWidget(remove_button)

    def remove_card(self):
        """Remove selected card in the cards table"""
        row = self.cards_table.currentRow()
        popup = QMessageBox()
        if row >= 0:  # check if there are any rows left
            selected_card = self.cards_table.item(row, 0).text()
            flash_con = create_con(flash_db)
            flash_cur = flash_con.cursor()
            flash_cur.execute("DELETE FROM flashcards WHERE frontside = ?",
                              [selected_card])
            flash_con.commit()  # commit the removal of the card
            # is necessary, would not remove without it
            self.cards_table.removeRow(row)
            popup.setWindowTitle("FastCard Removed")
            popup.setIcon(QMessageBox.Information)
            popup.setText("FastCard sucessfully removed")
        else:  # changes info on popup if there are no flashcards selected
            popup.setWindowTitle("No FastCard Selected")
            popup.setIcon(QMessageBox.Warning)
            popup.setText("Please select a FastCard")
        x = popup.exec_()


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
    Insert the account into the accounts database
    -------
    con: sqlite class
        SQLite connection to account database
    acc: tuple
        Account username and password
    """
    sql = "INSERT INTO accounts(username, password) VALUES(?, ?)"
    cur = con.cursor()
    cur.execute(sql, acc)
    con.commit()


def insert_flashcard(con, flash):
    """
    Insert the flashcard into the accounts database
    -------
    con: sqlite class
        SQLite connection to flashcard database
    flash: tiple
        Flashcard front and back
    """
    sql = "INSERT INTO flashcards(frontside, backside) VALUES(?, ?)"
    cur = con.cursor()
    cur.execute(sql, flash)
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
        pass
    except:
        print("er")


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
    if acc_con is not None:  # will create account db if it doesnt exist
        create_table(acc_con, acc_table)
    else:
        print("Couldn't create acc connection")

    flash_con = create_con(flash_db)
    if flash_con is not None:  # will create flashcards db if it doesnt exist
        create_table(flash_con, flash_table)
    else:
        print("Couldn't create flash connection")

    # Start the GUI up
    application = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(application.exec_())

if __name__ == "__main__":
    main()
