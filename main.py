from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QGridLayout, QLabel, \
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, \
    QComboBox, QToolBar, QStatusBar
from PyQt6.QtGui import QAction, QIcon
import sys
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(800, 600)

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        add_action = QAction(QIcon("icons/add.png"), "Add Student", self)
        add_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)

        search_action = QAction(QIcon("icons/search.png"), "Search", self)
        search_action.triggered.connect(self.search)
        edit_menu_item.addAction(search_action)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)


        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_action)
        toolbar.addAction(search_action)

        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        edit_button = QPushButton("Edit")
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete)

        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()

    def load_data(self):
        connection = sqlite3.connect('database.db')
        # cursor = connection.cursor
        # result = cursor.execute He did this like in web scrapper project
        result = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        dialog = SearchDialog()
        dialog.exec()


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Edit Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        layout = QVBoxLayout

        self.setLayout(layout)


class DeleteDialog(QDialog):
    pass


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Student Name")
        layout.addWidget(self.student_name)

        courses = ['Math', 'Chemistry', 'Alchemy', 'Science']
        self.course_data = QComboBox()
        self.course_data.addItems(courses)
        layout.addWidget(self.course_data)

        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        submit = QPushButton("Submit")
        submit.clicked.connect(self.add_student)
        layout.addWidget(submit)
        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.course_data.itemText(self.course_data.currentIndex())
        mobile = self.mobile.text()
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (Name, Course, Mobile) VALUES (?, ?, ?)", (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search For a Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Enter a name to search")
        layout.addWidget(self.student_name)

        search = QPushButton("Search")
        search.clicked.connect(self.search_data)
        layout.addWidget(search)

        self.setLayout(layout)

    def search_data(self):
        name = self.student_name.text()
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM students WHERE Name=?", (name,))
        row = cursor.fetchall()
        print(row)
        items = main_window.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            print(item.row())
            main_window.table.item(item.row(), 1).setSelected(True)
        cursor.close()
        connection.close()


# Default Code block for running PyQt Apps
app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())
