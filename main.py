# main.py

import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTabWidget,
                             QWidget, QVBoxLayout, QPushButton, QLabel)
from PyQt6.QtGui import QIcon
from manage_users import ManageUsers
from manage_warehouse import ManageWarehouse

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quản Lý Hệ Thống")
        self.setGeometry(700, 300, 500, 400)

        # Create a tab widget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)


        # Add user management tab
        self.user_management_tab = ManageUsers()
        self.tabs.addTab(self.user_management_tab, "Quản Lý Người Dùng")

        # Add warehouse management tab
        self.warehouse_management_tab = ManageWarehouse()
        self.tabs.addTab(self.warehouse_management_tab, "Quản Lý Kho")

        self.apply_styles()

    def apply_styles(self):
            style = """
            QWidget {
                background-color: #ffffff;  /* Change to white */
            }

            QTableWidget {
                background-color: #ffffff;  /* Table background */
                border: 1px solid #cccccc;
            }
            """
            self.setStyleSheet(style)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('image/google.png'))
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
