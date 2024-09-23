import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox
)
from database import Database
from PyQt6.QtGui import QIcon
from main import MainWindow
class LoginForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Đăng Nhập")
        self.setGeometry( 700, 300, 400, 300)

        self.database = Database()

        layout = QVBoxLayout()

        self.logo = QLabel("Đăng Nhập")
        self.logo.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(self.logo)

        self.username_label = QLabel("Tài khoản:")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nhập tài khoản của bạn")
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        self.password_label = QLabel("Mật khẩu:")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Nhập mật khẩu của bạn")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Đăng Nhập")
        self.login_button.setStyleSheet("background-color: #4285F4; color: white; font-weight: bold; padding: 10px; border-radius: 5px;")
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.register_button = QPushButton("Đăng Ký")
        self.register_button.setStyleSheet("background-color: #f1f1f1; color: #4285F4; padding: 10px; border-radius: 5px;")
        self.register_button.clicked.connect(self.open_register_form)
        layout.addWidget(self.register_button)

        self.forgot_password_button = QPushButton("Quên Mật Khẩu?")
        self.forgot_password_button.setStyleSheet("background-color: #f1f1f1; color: #4285F4; padding: 10px; border-radius: 5px;")
        self.forgot_password_button.clicked.connect(self.open_forgot_password_form)
        layout.addWidget(self.forgot_password_button)

        self.setLayout(layout)
        self.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                font-family: Arial, sans-serif;
            }
            QLabel {
                color: #333;
                margin: 10px 0;
            }
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 10px;
                margin-bottom: 10px;
            }
            QLineEdit:focus {
                border-color: #4285F4;
            }
        """)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Cảnh Báo", "Thiếu tham số bắt buộc!")
            return

        if self.database.validate_user(username, password):
            QMessageBox.information(self, "Thông Báo", "Đăng nhập thành công!")
            self.manage_users_form = MainWindow()  # Tạo đối tượng MainWindow
            self.manage_users_form.show()  # Hiện form quản lý người dùng
            self.close()  # Đóng form đăng nhập

        else:
            QMessageBox.warning(self, "Cảnh Báo", "Nhập sai mật khẩu!")

    def open_register_form(self):
        self.register_form = RegisterForm(self.database)
        self.register_form.show()

    def open_forgot_password_form(self):
        self.forgot_password_form = ForgotPasswordForm(self.database)
        self.forgot_password_form.show()

class RegisterForm(QWidget):
    def __init__(self, database):
        super().__init__()
        self.database = database
        self.setWindowTitle("Đăng Ký")
        self.setGeometry(300, 200, 400, 300)

        layout = QVBoxLayout()

        self.username_label = QLabel("Tài khoản:")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nhập tài khoản mới")
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        self.password_label = QLabel("Mật khẩu:")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Nhập mật khẩu mới")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        self.register_button = QPushButton("Đăng Ký")
        self.register_button.setStyleSheet("background-color: #4285F4; color: white; padding: 10px; border-radius: 5px;")
        self.register_button.clicked.connect(self.register_user)
        layout.addWidget(self.register_button)

        self.setLayout(layout)
        self.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                font-family: Arial, sans-serif;
            }
            QLabel {
                color: #333;
                margin: 10px 0;
            }
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 10px;
                margin-bottom: 10px;
            }
            QLineEdit:focus {
                border-color: #4285F4;
            }
        """)

    def register_user(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Cảnh Báo", "Thiếu tham số bắt buộc!")
            return

        if self.database.register_user(username, password):
            QMessageBox.information(self, "Thông Báo", "Đăng ký thành công!")
            self.close()  # Đóng form đăng ký
        else:
            QMessageBox.warning(self, "Cảnh Báo", "Tài khoản đã tồn tại!")


class ForgotPasswordForm(QWidget):
    def __init__(self, database):
        super().__init__()
        self.database = database
        self.setWindowTitle("Quên Mật Khẩu")
        self.setGeometry(300, 200, 400, 200)

        layout = QVBoxLayout()

        self.username_label = QLabel("Tài khoản:")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nhập tài khoản để đặt lại mật khẩu")
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        self.reset_button = QPushButton("Đặt lại mật khẩu")
        self.reset_button.setStyleSheet("background-color: #4285F4; color: white; padding: 10px; border-radius: 5px;")
        self.reset_button.clicked.connect(self.check_account)
        layout.addWidget(self.reset_button)

        self.new_password_label = None
        self.new_password_input = None
        self.confirm_password_label = None
        self.confirm_password_input = None

        self.setLayout(layout)
        self.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                font-family: Arial, sans-serif;
            }
            QLabel {
                color: #333;
                margin: 10px 0;
            }
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 10px;
                margin-bottom: 10px;
            }
            QLineEdit:focus {
                border-color: #4285F4;
            }
        """)

    def check_account(self):
        username = self.username_input.text()

        if not username:
            QMessageBox.warning(self, "Cảnh Báo", "Thiếu tài khoản!")
            return

        # Kiểm tra xem tài khoản có tồn tại không
        if not self.database.validate_register_check_user(username):  # Chỉ kiểm tra tên tài khoản
            QMessageBox.warning(self, "Cảnh Báo", "Tài khoản không tồn tại!")
            return

        # Tài khoản tồn tại, hiển thị các trường mật khẩu mới
        self.show_new_password_fields()

    def show_new_password_fields(self):
        if self.new_password_label is None:  # Only add if they don't already exist
            self.new_password_label = QLabel("Mật khẩu mới:")
            self.new_password_input = QLineEdit()
            self.new_password_input.setPlaceholderText("Nhập mật khẩu mới")
            self.new_password_input.setEchoMode(QLineEdit.EchoMode.Password)

            self.confirm_password_label = QLabel("Xác nhận mật khẩu:")
            self.confirm_password_input = QLineEdit()
            self.confirm_password_input.setPlaceholderText("Xác nhận mật khẩu mới")
            self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)

            self.layout().addWidget(self.new_password_label)
            self.layout().addWidget(self.new_password_input)
            self.layout().addWidget(self.confirm_password_label)
            self.layout().addWidget(self.confirm_password_input)

            self.reset_button.setText("Đặt lại mật khẩu")
            self.reset_button.clicked.disconnect()
            self.reset_button.clicked.connect(self.reset_password)

    def reset_password(self):
        new_password = self.new_password_input.text()
        confirm_password = self.confirm_password_input.text()

        if not new_password or not confirm_password:
            QMessageBox.warning(self, "Cảnh Báo", "Thiếu tham số bắt buộc!")
            return

        if new_password != confirm_password:
            QMessageBox.warning(self, "Cảnh Báo", "Mật khẩu không khớp!")
            return

        username = self.username_input.text()

        # Update the password
        self.database.update_password(username, new_password)
        QMessageBox.information(self, "Thông Báo", "Đặt lại mật khẩu thành công!")
        self.close()  # Close the form

if __name__ == "__main__":
    app = QApplication(sys.argv)
    #Thiêt lập biểu tượng cho ứng dụng
    app.setWindowIcon(QIcon('image/google.png'))
    window = LoginForm()
    window.show()
    sys.exit(app.exec())
