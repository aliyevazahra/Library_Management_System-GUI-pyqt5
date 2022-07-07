import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sqlite3
import main


con = sqlite3.connect('library.db')
cur = con.cursor()


class AddMember(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Member")
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
        img = QPixmap('icons/addperson.png')
        img_book.setPixmap(img)
        lbl_title = QLabel("Add Member", topFrame)
        lbl_title.setStyleSheet("color: #8375C4; font: Bold 25pt; font-family: Times New Roman;")
        top_layout.addStretch()
        top_layout.addWidget(img_book)
        top_layout.addWidget(lbl_title)
        top_layout.addStretch()
        main_layout.addWidget(topFrame)

        #################___Bottom Frame Design___##########################
        self.name_entry = QLineEdit(bottomFrame)
        self.name_entry.setPlaceholderText("Fullname of Member")
        self.name_entry.setPalette(QPalette(QColor("#FFF")))
        self.name_entry.setStyleSheet("background-color: #F2F2F2")

        self.phone_entry = QLineEdit(bottomFrame)
        self.phone_entry.setPlaceholderText("Member's phone number")
        self.phone_entry.setPalette(QPalette(QColor("#FFF")))
        self.phone_entry.setStyleSheet("background-color: #F2F2F2; margin-bottom:10px;")


        add_button = QPushButton("Add", bottomFrame)
        add_button.setStyleSheet("background-color: #8375C4; color: white;")
        add_button.clicked.connect(self.addMember)

        bottom_layout.addRow(QLabel("Fullname : "), self.name_entry)
        bottom_layout.addRow(QLabel("Phone : "), self.phone_entry)
        bottom_layout.addRow(QLabel(""), add_button)
        main_layout.addWidget(bottomFrame)

        self.setLayout(main_layout)

    def addMember(self):
        name = self.name_entry.text()
        phone = self.phone_entry.text()

        if(name and phone !=""):

            try:
                query = "INSERT INTO 'members' (member_name, member_phone) VALUES(?,?)"
                cur.execute(query,(name,phone))
                con.commit()
                self.name_entry.setText("")
                self.phone_entry.setText("")
                QMessageBox.information(self, "Information!!!", "Member has been added.")

            except:
                QMessageBox.information(self, "Warning!!!", "Member can't be added.")


        else:
            QMessageBox.information(self, "Warning!!!", "Fields can't be empty.")
