from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QGridLayout, QLabel, \
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, \
    QComboBox, QToolBar, QStatusBar, QMessageBox
from PyQt6.QtGui import QAction, QIcon
import sys
import sqlite3


class DataBaseConnection:
    # This class is created to create a connection object
    # For MySql Refer the pic uploaded to make the changes
    def __init__(self, database="database.db"):
        self.database = database

    def connection(self):
        connection = sqlite3.connect(self.database)
        return connection

# For Main window use QMainWindow
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(800, 600)

        # Adds a menu bar with buttons
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Search")

        #  Adds action to menu bar items
        add_action = QAction(QIcon("icons/add.png"), "Add Student", self)
        add_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        # about_action.setMenuRole(QAction.MenuRole.NoRole) For MAC users to show the action in menu bar
        about_action.triggered.connect(self.about)

        search_action = QAction(QIcon("icons/search.png"), "Search", self)
        search_action.triggered.connect(self.search)
        edit_menu_item.addAction(search_action)

        # Add the table to main display window
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        # Adds the toolbar under the menubar
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_action)
        toolbar.addAction(search_action)

        # Adds the status bar to the footer
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.table.cellClicked.connect(self.cell_clicked)

        # Makes the edit and delete to appear in status bar and adds functon to it
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

    # Calls the following classes to perform the specified action
    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()

    # Loads the data to table
    def load_data(self):
        connection = DataBaseConnection().connection()
        cursor = connection.cursor()
        # It is better to call the cursor object to perform actions on sqlite3 as mysql requires it as a mandatory.
        result = connection.execute("SELECT * FROM students")
        result = result.fetchall()
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

    def about(self):
        dialog = AboutDialog()
        dialog.exec()

# For Mini window use QDialog
class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Input text box
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Student Name")
        layout.addWidget(self.student_name)

        # Course selector - A drop down
        courses = ['Math', 'Chemistry', 'Alchemy', 'Physics']
        self.course_data = QComboBox()
        self.course_data.addItems(courses)
        layout.addWidget(self.course_data)

        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        # A submit button
        submit = QPushButton("Submit")
        submit.clicked.connect(self.add_student)
        layout.addWidget(submit)
        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.course_data.itemText(self.course_data.currentIndex())
        mobile = self.mobile.text()
        connection = DataBaseConnection().connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (Name, Course, Mobile) VALUES (?, ?, ?)", (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()
        self.close()


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
        connection = DataBaseConnection().connection()
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


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Edit Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        index = main_window.table.currentRow()
        student_name = main_window.table.item(index, 1).text()
        self.id = main_window.table.item(index, 0).text()

        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText("Student Name")
        layout.addWidget(self.student_name)

        current_course = main_window.table.item(index, 2).text()
        courses = ['Math', 'Chemistry', 'Alchemy', 'Physics']
        self.course_data = QComboBox()
        self.course_data.addItems(courses)
        self.course_data.setCurrentText(current_course)
        layout.addWidget(self.course_data)

        mobile = main_window.table.item(index, 3).text()
        self.mobile = QLineEdit(mobile)
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        submit = QPushButton("Update")
        submit.clicked.connect(self.update_record)
        layout.addWidget(submit)
        self.setLayout(layout)

    def update_record(self):
        connection = DataBaseConnection().connection()
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name=? , course=?,mobile=? WHERE id=?",
                       (self.student_name.text(),
                        self.course_data.itemText(self.course_data.currentIndex()),
                        self.mobile.text(), self.id))
        connection.commit()
        cursor.close()
        connection.close()

        # To Refresh the Table
        main_window.load_data()
        self.close()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Student Data")

        layout = QGridLayout()

        confirmation = QLabel("Are you sure you want to delete this record?")
        yes = QPushButton("Yes")
        no = QPushButton("No")

        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no, 1, 1)

        yes.clicked.connect(self.delete_record)
        no.clicked.connect(self.closer)

        self.setLayout(layout)

    def delete_record(self):
        index = main_window.table.currentRow()
        student_id = main_window.table.item(index, 0).text()
        connection = DataBaseConnection().connection()
        cursor = connection.cursor()
        cursor.execute("DELETE from students WHERE id = ? ", (student_id,))
        connection.commit()
        cursor.close()
        connection.close()
        # To Refresh the Table
        main_window.load_data()

        self.close()

        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("The Record was Deleted Successfully!")
        confirmation_widget.exec()
        confirmation_widget.close()

    def closer(self):
        self.close()

# For pop up messages use QMessageBox
class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About Us")
        content = """
This app was developed by me on my journey to python with the help of a udemy course.\n
This is one of the biggest apps I build. But this will not be the biggest forever...\n
If ur still coding and seeing this after 5 years You have come a long way 12.12.2023
"""
        self.setText(content)


# Default Code block for running PyQt Apps
app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())
