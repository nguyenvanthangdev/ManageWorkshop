import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem,
    QHBoxLayout, QCheckBox, QInputDialog
)
from PyQt6.QtGui import QIcon
from database import Database

class ManageUsers(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quản Lý Người Dùng")
        self.setGeometry(300, 200, 500, 400)

        self.database = Database()  # Initialize the Database instance
        self.layout = QVBoxLayout()

        self.title_label = QLabel("Danh Sách Người Dùng")
        self.layout.addWidget(self.title_label)

        self.user_table = QTableWidget()
        self.user_table.setColumnCount(3)
        self.user_table.setHorizontalHeaderLabels(["Chọn", "Tài khoản", "Mật khẩu"])
        self.layout.addWidget(self.user_table)

        self.button_layout = QHBoxLayout()
        self.add_button = QPushButton("Thêm Người Dùng")
        self.add_button.clicked.connect(self.add_user)
        self.button_layout.addWidget(self.add_button)

        self.edit_button = QPushButton("Sửa Người Dùng")
        self.edit_button.clicked.connect(self.edit_user)
        self.button_layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("Xóa Người Dùng")
        self.delete_button.clicked.connect(self.delete_user)
        self.button_layout.addWidget(self.delete_button)

        self.layout.addLayout(self.button_layout)
        self.setLayout(self.layout)
        self.load_users()
        self.apply_styles()  # Apply styles

    def apply_styles(self):
        style = """
        QWidget {
            background-color: #FFFFFF;  /* Change to white */
        }

        QTableWidget {
            background-color: #ffffff;  /* Table background */
            border: 1px solid #cccccc;
        }

        QPushButton {
            background-color: #007bff;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 5px;
        }

        QPushButton:hover {
            background-color: #0056b3;
        }

        QLabel {
            font-weight: bold;
            font-size: 16px;
        }

        QLineEdit {
            padding: 5px;
            border: 1px solid #cccccc;
            border-radius: 3px;
        }
        """
        self.setStyleSheet(style)

    def load_users(self):
        users = self.database.get_users()
        self.user_table.setRowCount(len(users))

        for row, (username, password) in enumerate(users):
            checkbox = QCheckBox()
            self.user_table.setCellWidget(row, 0, checkbox)
            self.user_table.setItem(row, 1, QTableWidgetItem(username))
            self.user_table.setItem(row, 2, QTableWidgetItem(password))

    def add_user(self):
        username, ok1 = QInputDialog.getText(self, "Thêm Người Dùng", "Tài khoản:")
        password, ok2 = QInputDialog.getText(self, "Thêm Người Dùng", "Mật khẩu:", QLineEdit.EchoMode.Password)

        if ok1 and ok2 and username and password:
            if self.database.register_user(username, password):
                QMessageBox.information(self, "Thông Báo", "Người dùng đã được thêm!")
                self.load_users()
            else:
                QMessageBox.warning(self, "Cảnh Báo", "Tài khoản đã tồn tại!")

    def edit_user(self):
        for row in range(self.user_table.rowCount()):
            checkbox = self.user_table.cellWidget(row, 0)
            if checkbox.isChecked():
                current_username = self.user_table.item(row, 1).text()
                new_username, ok_username = QInputDialog.getText(self, "Sửa Người Dùng", "Tài khoản mới:", text=current_username)
                new_password, ok_password = QInputDialog.getText(self, "Sửa Người Dùng", "Mật khẩu mới:", QLineEdit.EchoMode.Password)

                if ok_username and ok_password:
                    if new_username and new_password:
                        if current_username != new_username:
                            # Check if the new username already exists
                            if self.database.validate_register_check_user(new_username):
                                QMessageBox.warning(self, "Cảnh Báo", "Tài khoản mới đã tồn tại!")
                                return
                            else:
                                self.database.delete_user(current_username)  # Remove old username
                                self.database.register_user(new_username, new_password)  # Add new username
                                QMessageBox.information(self, "Thông Báo", "Người dùng đã được cập nhật!")
                        else:
                            # Only update password if the username hasn't changed
                            self.database.update_password(current_username, new_password)
                            QMessageBox.information(self, "Thông Báo", "Mật khẩu đã được cập nhật!")

                        self.load_users()  # Reload the user list
                    else:
                        QMessageBox.warning(self, "Cảnh Báo", "Vui lòng nhập tài khoản và mật khẩu mới!")
                return

        QMessageBox.warning(self, "Cảnh Báo", "Vui lòng chọn người dùng để sửa!")

    def delete_user(self):
        for row in range(self.user_table.rowCount()):
            checkbox = self.user_table.cellWidget(row, 0)
            if checkbox.isChecked():
                username = self.user_table.item(row, 1).text()
                self.database.delete_user(username)
                QMessageBox.information(self, "Thông Báo", "Người dùng đã được xóa!")
                self.load_users()
                return

        QMessageBox.warning(self, "Cảnh Báo", "Vui lòng chọn người dùng để xóa!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('image/google.png'))
    window = ManageUsers()
    window.show()
    sys.exit(app.exec())
