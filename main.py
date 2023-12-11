from PyQt6.QtWidgets import QApplication, QMainWindow, QGridLayout, QLabel, \
    QLineEdit, QPushButton
from PyQt6.QtGui import QAction
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        file_menu_item = self.menuBar().addMenu("File")
        help_men_item = self.menuBar().addMenu("Help")

        add_action = QAction("Add Student", self)
        file_menu_item.addAction(add_action)

        about_action = QAction("About", self)
        help_men_item.addAction(about_action)


# Default Code block for running PyQt Apps
app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())