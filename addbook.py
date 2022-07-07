import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sqlite3
import main


con = sqlite3.connect('library.db')
cur = con.cursor()


class AddBook(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Book")
        self.setGeometry(50, 50, 450, 550)
        self.setFixedSize(self.size())
        self.UI()

        self.show()

    def UI(self):

        #################___Top Frame Design___##########################
        main_layout = QVBoxLayout()
        topFrame = QFrame(self)
        top_layout = QHBoxLayout(topFrame)
        bottomFrame = QFrame(self)
        bottom_layout = QFormLayout(bottomFrame)
        bottom_layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        bottomFrame.setStyleSheet("font: Bold 15pt; font-family: Times New Roman;")

        img_book = QLabel(topFrame)
        img = QPixmap('icons/addbook.png')
        img_book.setPixmap(img)
        lbl_title = QLabel("Add Book", topFrame)
        lbl_title.setStyleSheet("color: #8375C4; font: Bold 25pt; font-family: Times New Roman;")
        top_layout.addStretch()
        top_layout.addWidget(img_book)
        top_layout.addWidget(lbl_title)
        top_layout.addStretch()
        main_layout.addWidget(topFrame)

        #################___Bottom Frame Design___##########################
        self.name_entry = QLineEdit(bottomFrame)
        self.name_entry.setPlaceholderText("Name of Book")
        self.name_entry.setPalette(QPalette(QColor("#FFF")))
        self.name_entry.setStyleSheet("background-color: #F2F2F2")

        self.author_entry = QLineEdit(bottomFrame)
        self.author_entry.setPlaceholderText("Name of Author")
        self.author_entry.setPalette(QPalette(QColor("#FFF")))
        self.author_entry.setStyleSheet("background-color: #F2F2F2")

        self.page_entry = QLineEdit(bottomFrame)
        self.page_entry.setPlaceholderText("Page Size")
        self.page_entry.setPalette(QPalette(QColor("#FFF")))
        self.page_entry.setStyleSheet("background-color: #F2F2F2")

        self.lan_entry = QLineEdit(bottomFrame)
        self.lan_entry.setPlaceholderText("Language")
        self.lan_entry.setPalette(QPalette(QColor("#FFF")))
        self.lan_entry.setStyleSheet("background-color: #F2F2F2")

        self.description = QTextEdit(bottomFrame)
        self.description.setStyleSheet("background-color: #F2F2F2; margin-bottom:10px; color:black;")

        add_button = QPushButton("Add", bottomFrame)
        add_button.setStyleSheet("background-color: #8375C4; color: white;")
        add_button.clicked.connect(self.addBook)

        bottom_layout.addRow(QLabel("Name : "), self.name_entry)
        bottom_layout.addRow(QLabel("Author : "), self.author_entry)
        bottom_layout.addRow(QLabel("Page : "), self.page_entry)
        bottom_layout.addRow(QLabel("Language : "), self.lan_entry)
        bottom_layout.addRow(QLabel("Description : "), self.description)
        bottom_layout.addRow(QLabel(""), add_button)
        main_layout.addWidget(bottomFrame)

        self.setLayout(main_layout)

    def addBook(self):
        name = self.name_entry.text()
        author = self.author_entry.text()
        page = self.page_entry.text()
        language = self.lan_entry.text()
        description = self.description.toPlainText()

        if(name and author and page and language and description !=""):
            try:
                query = "INSERT INTO 'books' (book_name,book_author,book_page," \
                        "book_language,book_details) VALUES(?,?,?,?,?)"
                cur.execute(query,(name,author,page,language,description))
                con.commit()
                self.name_entry.setText("")
                self.author_entry.setText("")
                self.page_entry.setText("")
                self.lan_entry.setText("")
                self.description.setText("")
                QMessageBox.information(self, "Information!!!", "Book has been added.")


            except:
                QMessageBox.information(self, "Warning!!!", "Book can't be added.")


        else:
            QMessageBox.information(self, "Warning!!!", "Fields can't be empty.")
