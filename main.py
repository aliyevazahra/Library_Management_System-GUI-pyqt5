import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sqlite3
import addbook, addmember, givebook


con = sqlite3.connect('library.db')
cur = con.cursor()


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Library Management")
        self.setGeometry(50, 50, 1050, 650)
        self.setFixedSize(self.size())
        self.UI()

        self.show()

    def UI(self):
        self.toolbar()
        self.design()
        self.getBooks()
        self.getMembers()
        self.getStatistics()

    def toolbar(self):
        self.tb = self.addToolBar("Tool Bar")
        self.add_book = QAction(QIcon('icons/add_book.png'), "Add Book", self)
        self.add_book.triggered.connect(self.addBook)
        self.tb.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.tb.addAction(self.add_book)
        self.tb.setStyleSheet("color: #666; font-weight: bold; font-family: Verdana; font-size: 16px")


        #######################################################################################################
        self.add_member = QAction(QIcon('icons/users.png'), "Add Member", self)
        self.add_member.triggered.connect(self.addMember)
        self.tb.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.tb.addAction(self.add_member)
        #######################################################################################################
        self.give_book = QAction(QIcon('icons/givebook.png'), "Lend Book", self)
        self.give_book.triggered.connect(self.giveBook)
        self.tb.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.tb.addAction(self.give_book)

    def design(self):
        #############################___main design widgets_____##############################################
        main_layout = QHBoxLayout()
        main_left_layout = QVBoxLayout()
        main_right_layout = QVBoxLayout()
        main_layout.addLayout(main_left_layout, 65)
        main_layout.addLayout(main_right_layout, 35)
        #######################################################################################################
        self.tabs = QTabWidget(self)
        self.tabs.blockSignals(True)
        self.setCentralWidget(self.tabs)
        self.tabs.currentChanged.connect(self.tabChanged)
        self.tab_1 = QWidget()
        self.tab_2 = QWidget()
        self.tab_3 = QWidget()
        self.tabs.addTab(self.tab_1, "Books")
        self.tabs.addTab(self.tab_2, "Member")
        self.tabs.addTab(self.tab_3, "Statistics")

        ##############################___Tab_1______##########################################################
        ##############################___main left layout__###################################################
        self.books_table = QTableWidget()
        self.books_table.setColumnCount(6)
        self.books_table.setColumnHidden(0, True)
        self.books_table.setHorizontalHeaderItem(0, QTableWidgetItem("Book ID"))
        self.books_table.setHorizontalHeaderItem(1, QTableWidgetItem("Book Name"))
        self.books_table.setHorizontalHeaderItem(2, QTableWidgetItem("Book Author"))
        self.books_table.setHorizontalHeaderItem(3, QTableWidgetItem("Book Page"))
        self.books_table.setHorizontalHeaderItem(4, QTableWidgetItem("Book Language"))
        self.books_table.setHorizontalHeaderItem(5, QTableWidgetItem("Book Status"))
        self.books_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.books_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.books_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.books_table.doubleClicked.connect(self.selectedBook)
        main_left_layout.addWidget(self.books_table)

        ##############################___main right layout__###################################################

            #################___Right Side top search box___##########################
        right_top_frame = QGroupBox(self)
        right_top_frame.setObjectName("Main")
        right_top_frame.setStyleSheet("#Main{font: Bold 15pt;}")
        right_top_frame_box = QHBoxLayout(right_top_frame)
        self.search_entry = QLineEdit(right_top_frame)
        self.search_entry.setStyleSheet("border: 1px solid #ccc; border-radius: 2px; height:30px; background: #F2F2F2; color: black;")
        search_button = QPushButton(right_top_frame)
        search_button.setIcon(QIcon('icons/loupe.png'))
        search_button.clicked.connect(self.searchBooks)
        right_top_frame_box.addWidget(self.search_entry)
        right_top_frame_box.addWidget(search_button)
        main_right_layout.addWidget(right_top_frame, 0)

        #################___Right Side List box___##########################
        right_middle_frame = QGroupBox(self)
        right_middle_frame.setObjectName("Main")
        right_middle_frame.setStyleSheet("#Main{font: Bold 15pt;"
                                          "color:black; border-radius: 5px;}")
        self.radio_btn1 = QRadioButton("All Books", right_middle_frame)
        self.radio_btn1.setStyleSheet("margin-bottom:10px;")
        self.radio_btn2 = QRadioButton("Available Books", right_middle_frame)
        self.radio_btn2.setStyleSheet("margin-bottom:10px;")
        self.radio_btn3 = QRadioButton("Borrowed Books", right_middle_frame)
        self.radio_btn3.setStyleSheet("margin-bottom:10px;")
        self.btn_list = QPushButton("List", right_middle_frame)
        self.btn_list.setStyleSheet("background-color: #8375C4; font: Bold 13pt; color: white;"
                                    " margin-left: 0px; height:30px; border-radius:2px; padding: 0 5px;")
        self.btn_list.clicked.connect(self.listBooks)
        right_middle_box = QVBoxLayout(right_middle_frame)
        right_middle_box.addWidget(self.radio_btn1)
        right_middle_box.addWidget(self.radio_btn2)
        right_middle_box.addWidget(self.radio_btn3)
        right_middle_box.addWidget(self.btn_list)
        main_right_layout.addWidget(right_middle_frame, 20)

        #################___Right Side bottom___##########################

        #################___tab-1 design___###############################

        right_bottom_layout = QVBoxLayout()
        img_library = QLabel("")
        img_library.setAlignment(Qt.AlignCenter)
        img = QPixmap('icons/library-1.png').scaled(250, 250)
        img_library.setPixmap(img)
        right_bottom_layout.addWidget(img_library)
        main_right_layout.addLayout(right_bottom_layout, 60)

        self.tab_1.setLayout(main_layout)

    #################___tab-1 design end___##########################

    #################___tab-2 design___##############################

        member_main_layout = QHBoxLayout()
        member_layout_left = QHBoxLayout()
        member_layout_right = QVBoxLayout()
        member_main_layout.addLayout(member_layout_left,65)
        member_main_layout.addLayout(member_layout_right,35)
        self.members_table = QTableWidget()
        self.members_table.setColumnCount(3)
        self.members_table.setHorizontalHeaderItem(0, QTableWidgetItem("Member ID"))
        self.members_table.setHorizontalHeaderItem(1, QTableWidgetItem("Member Fullname"))
        self.members_table.setHorizontalHeaderItem(2, QTableWidgetItem("Member Phone"))
        self.members_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.members_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.members_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.members_table.doubleClicked.connect(self.selectedMember)
        member_layout_left.addWidget(self.members_table)

        member_search_group = QGroupBox(self)
        member_search_group.setObjectName("Main")
        member_search_group.setStyleSheet("#Main{color: black;"
                                          "font: Bold 15pt; font-family: Times New Roman;}")
        member_layout_right_top = QHBoxLayout(member_search_group)
        self.entry_member_search = QLineEdit()
        self.entry_member_search.setStyleSheet("border: 1px solid #ccc; border-radius: 2px; height:30px; background: #F2F2F2; color: black;")
        button_memmber_search = QPushButton(right_top_frame)
        button_memmber_search.setIcon(QIcon('icons/loupe.png'))
        button_memmber_search.clicked.connect(self.searchMembers)
        member_layout_right_top.addWidget(self.entry_member_search)
        member_layout_right_top.addWidget(button_memmber_search)
        member_layout_right.addWidget(member_search_group)
        member_layout_right.addStretch()

        self.tab_2.setLayout(member_main_layout)

    #################___tab-2 design end___##########################

    #################___tab-3 design___##############################

        statistics_main_layout = QVBoxLayout()
        self.statistic_group = QGroupBox("Statistics")
        self.statistic_group.setAlignment(Qt.AlignCenter)
        self.statistic_form_layout = QFormLayout()
        self.statistic_group.setFont(QFont("Times New Roman", 20))
        self.total_books = QLabel("")
        self.total_members = QLabel("")
        self.taken_books = QLabel("")
        self.availabel_books = QLabel("")
        self.statistic_form_layout.addChildWidget(self.statistic_group)
        self.statistic_form_layout.addRow(QLabel("Total Books : "), self.total_books)
        self.statistic_form_layout.addRow(QLabel("Total Members : "), self.total_members)
        self.statistic_form_layout.addRow(QLabel("Taken Books : "), self.taken_books)
        self.statistic_form_layout.addRow(QLabel("Available Books : "), self.availabel_books)
        self.statistic_group.setLayout(self.statistic_form_layout)
        statistics_main_layout.addWidget(self.statistic_group)
        self.tab_3.setLayout(statistics_main_layout)
        self.tabs.blockSignals(False)


    def tabChanged(self, i):
        self.getMembers()
        self.getStatistics()
        self.getBooks()

    def giveBook(self):
        self.givebook = givebook.GiveBook()

    def addBook(self):
        self.addbook = addbook.AddBook()

    def addMember(self):
        self.addmember = addmember.AddMember()

    def searchMembers(self):
        value = self.entry_member_search.text()
        if value == "":
            QMessageBox.information(self, "Warning!!!", "Search query can't be empty!!!")
        else:
            self.entry_member_search.setText("")
            query = cur.execute("SELECT * FROM members WHERE member_name LIKE ?", ('%'+value+'%',)).fetchall()
            if query == []:
                QMessageBox.information(self, "Warning!!!", "There is no such a member!!!")
            else:
                for i in reversed(range(self.members_table.rowCount())):
                    self.members_table.removeRow(i)
                for row_data in query:
                    row_number = self.members_table.rowCount()
                    self.members_table.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.members_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))


    def getStatistics(self):
        count_books = cur.execute("SELECT count(book_id) FROM books").fetchall()
        count_members = cur.execute("SELECT count(member_id) FROM members").fetchall()
        taken_books = cur.execute("SELECT count(book_status) From books WHERE book_status = 'Not Available'").fetchall()
        available_books = cur.execute("SELECT count(book_status) From books WHERE book_status = 'Available'").fetchall()
        self.total_books.setText(str(count_books[0][0]))
        self.total_members.setText(str(count_members[0][0]))
        self.taken_books.setText(str(taken_books[0][0]))
        self.availabel_books.setText(str(available_books[0][0]))

    def getBooks(self):
        self.books_table.setFont(QFont("Times New Roman", 14))
        for i in reversed(range(self.books_table.rowCount())):
            self.books_table.removeRow(i)
        query = cur.execute("SELECT book_id,book_name,book_author,"
                            "book_page,book_language,book_status FROM books")
        for row_data in query:
            row_number = self.books_table.rowCount()
            self.books_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.books_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        self.books_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def getMembers(self):
        self.members_table.setFont(QFont("Times New Roman", 14))
        for i in reversed(range(self.members_table.rowCount())):
            self.members_table.removeRow(i)
        query = cur.execute("SELECT * FROM members")
        for row_data in query:
            row_number = self.members_table.rowCount()
            self.members_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.members_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        self.members_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.members_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def searchBooks(self):
        value = self.search_entry.text()
        if value=="":
            QMessageBox.information(self, "Warning!!!", "Search query can't be empty!!!")
        else:
            query = cur.execute("SELECT book_id,book_name,book_author,"
                            "book_page,book_language,book_status FROM books "
                                "WHERE book_name LIKE ? or book_author LIKE ?",
                                ('%'+value+'%', '%'+value+'%')).fetchall()

            if query == []:
                QMessageBox.information(self, "Warning!!!", "There is no such a book or author!!!")

            else:
                for i in reversed(range(self.books_table.rowCount())):
                    self.books_table.removeRow(i)
                for row_data in query:
                    row_number = self.books_table.rowCount()
                    self.books_table.insertRow(row_number)

                    for column_number, data in enumerate(row_data):
                        self.books_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def listBooks(self):
        if self.radio_btn1.isChecked() == True:
            query = cur.execute("SELECT book_id,book_name,book_author,"
                            "book_page,book_language,book_status FROM books")
            for i in reversed(range(self.books_table.rowCount())):
                self.books_table.removeRow(i)
            for row_data in query:
                row_number = self.books_table.rowCount()
                self.books_table.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.books_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        elif self.radio_btn2.isChecked() == True:
            query = cur.execute("SELECT book_id,book_name,book_author,"
                            "book_page,book_language,book_status FROM books WHERE book_status =?", ("Available",))
            for i in reversed(range(self.books_table.rowCount())):
                self.books_table.removeRow(i)
            for row_data in query:
                row_number = self.books_table.rowCount()
                self.books_table.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.books_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        elif self.radio_btn3.isChecked() == True:
            query = cur.execute("SELECT book_id,book_name,book_author,"
                                "book_page,book_language,book_status FROM books WHERE book_status =?", ("Not Available",))
            for i in reversed(range(self.books_table.rowCount())):
                self.books_table.removeRow(i)
            for row_data in query:
                row_number = self.books_table.rowCount()
                self.books_table.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.books_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def selectedBook(self):
        global book_id
        book_list = []
        for i in range(0,6):
            book_list.append(self.books_table.item(self.books_table.currentRow(),i).text())
        book_id = book_list[0]
        self.displaybook = DisplayBook()
        self.displaybook.show()

    def selectedMember(self):
        global member_id
        member_list = []
        for i in range(0,3):
            member_list.append(self.members_table.item(self.members_table.currentRow(),i).text())
        member_id = member_list[0]
        self.displaymember = DisplayMember()
        self.displaymember.show()

class DisplayMember(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Member Info")
        self.setGeometry(50, 50, 450, 550)
        self.setFixedSize(self.size())
        self.UI()

        self.show()

    def UI(self):
        #################___Get Member From Database___##########################
        global member_id
        member = cur.execute("SELECT * FROM members WHERE member_id=?",(member_id,)).fetchall()
        taken_books = cur.execute("SELECT books.book_name FROM borrows LEFT JOIN "
                                  "books ON books.book_id=borrows.bbook_id WHERE "
                                  "borrows.bmember_id=?",(member_id,)).fetchall()

        #################___Top Frame Design___##########################
        main_layout = QVBoxLayout()
        topFrame = QFrame(self)
        top_layout = QHBoxLayout(topFrame)
        bottomFrame = QFrame(self)
        bottom_layout = QFormLayout(bottomFrame)
        bottom_layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        bottomFrame.setStyleSheet("font: Bold 15pt; font-family: Times New Roman;")

        img_book = QLabel(topFrame)
        img = QPixmap('icons/person_info.png')
        img_book.setPixmap(img)
        lbl_title = QLabel("Member Details", topFrame)
        lbl_title.setStyleSheet("color: #8375C4; font: Bold 25pt; font-family: Times New Roman; ")
        top_layout.addStretch()
        top_layout.addWidget(img_book)
        top_layout.addWidget(lbl_title)
        top_layout.addStretch()
        main_layout.addWidget(topFrame)

        #################___Bottom Frame Design___##########################
        self.name_entry = QLineEdit(bottomFrame)
        self.name_entry.setText(member[0][1])
        self.name_entry.setStyleSheet("background-color: #F2F2F2; color: black")

        self.phone_entry = QLineEdit(bottomFrame)
        self.phone_entry.setText(member[0][2])
        self.phone_entry.setStyleSheet("background-color: #F2F2F2; color: black")

        self.taken_books_list = QListWidget(bottomFrame)
        self.taken_books_list.setStyleSheet("background-color: #F2F2F2; color: black")
        if taken_books!= []:
            for book in taken_books:
                self.taken_books_list.addItem(book[0])
        else:
            self.taken_books_list.addItem("No Taken Book")

        delete_button = QPushButton("Delete Member", bottomFrame)
        delete_button.setStyleSheet("background-color: #8375C4; color: white;")
        delete_button.clicked.connect(self.deleteMember)

        bottom_layout.addRow(QLabel("Fullname : "), self.name_entry)
        bottom_layout.addRow(QLabel("Phone : "), self.phone_entry)
        bottom_layout.addRow(QLabel("Taken Books : "), self.taken_books_list)
        bottom_layout.addRow(QLabel(""), delete_button)
        main_layout.addWidget(bottomFrame)

        self.setLayout(main_layout)

    def deleteMember(self):
        global member_id
        mbox = QMessageBox.information(self, "Warning!!!", "Are you sure to delete this member?",
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if mbox == QMessageBox.Yes:
            try:
                cur.execute("DELETE FROM members WHERE member_id=?", (member_id,))
                cur.execute("DELETE FROM borrows WHERE bmember_id=?",(member_id))
                con.commit()
                QMessageBox.information(self, "Info", "Member has been deleted!")

            except:
                QMessageBox.information(self, "Warning!!!", "Member has not been deleted!!!")



class DisplayBook(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Display Book")
        self.setGeometry(50, 50, 450, 550)
        self.setFixedSize(self.size())
        self.UI()

        self.show()

    def UI(self):
        #################___Getting Book Details From Database___##########################
        global book_id
        book = cur.execute("SELECT * FROM books WHERE book_id=?",(book_id,)).fetchall()

        #################___Top Frame Design___##########################

        main_layout = QVBoxLayout()
        topFrame = QFrame(self)
        top_layout = QHBoxLayout(topFrame)
        bottomFrame = QFrame(self)
        bottom_layout = QFormLayout(bottomFrame)
        bottom_layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        bottomFrame.setStyleSheet("font: Bold 15pt; font-family: Times New Roman;")

        img_book = QLabel(topFrame)
        img = QPixmap('icons/book_details.png')
        img_book.setPixmap(img)
        lbl_title = QLabel("Details of Book", topFrame)
        lbl_title.setStyleSheet("color: #8375C4; font: Bold 25pt; font-family: Times New Roman; ")
        top_layout.addStretch()
        top_layout.addWidget(img_book)
        top_layout.addWidget(lbl_title)
        top_layout.addStretch()
        main_layout.addWidget(topFrame)

        #################___Bottom Frame Design___##########################
        self.name_entry = QLineEdit(bottomFrame)
        self.name_entry.setText(book[0][1])
        self.name_entry.setStyleSheet("background-color: #F2F2F2; color: black")

        self.author_entry = QLineEdit(bottomFrame)
        self.author_entry.setText(book[0][2])
        self.author_entry.setStyleSheet("background-color: #F2F2F2; color: black")

        self.page_entry = QLineEdit(bottomFrame)
        self.page_entry.setText(book[0][3])
        self.page_entry.setStyleSheet("background-color: #F2F2F2; color: black")

        self.lan_entry = QLineEdit(bottomFrame)
        self.lan_entry.setText(book[0][5])
        self.lan_entry.setStyleSheet("background-color: #F2F2F2; color: black")

        self.description = QTextEdit(bottomFrame)
        self.description.setText(book[0][4])
        self.description.setStyleSheet("background-color: #F2F2F2; color: black")

        delete_button = QPushButton("Delete", bottomFrame)
        delete_button.setStyleSheet("background-color: #8375C4; color: white;")
        delete_button.clicked.connect(self.deleteBook)

        bottom_layout.addRow(QLabel("Name : "), self.name_entry)
        bottom_layout.addRow(QLabel("Author : "), self.author_entry)
        bottom_layout.addRow(QLabel("Page : "), self.page_entry)
        bottom_layout.addRow(QLabel("Language : "), self.lan_entry)
        bottom_layout.addRow(QLabel("Description : "), self.description)
        bottom_layout.addRow(QLabel(""), delete_button)
        main_layout.addWidget(bottomFrame)

        self.setLayout(main_layout)

    def deleteBook(self):
        global book_id
        mbox = QMessageBox.information(self, "Warning!!!", "Are you sure to delete this book?",
                                       QMessageBox.Yes|QMessageBox.No, QMessageBox.No)

        if mbox == QMessageBox.Yes:
            try:
                cur.execute("DELETE FROM books WHERE book_id=?",(book_id,))
                cur.execute("DELETE FROM borrows WHERE bbook_id=?",(book_id,))
                con.commit()
                QMessageBox.information(self, "Info", "Book has been deleted!")

            except:
                QMessageBox.information(self, "Warning!!!", "Book has not been deleted!!!")


def main():
    App = QApplication(sys.argv)
    window = Main()
    App.setWindowIcon(QIcon('icons/icon.png'))
    sys.exit(App.exec_())
if __name__ == '__main__':

    main()