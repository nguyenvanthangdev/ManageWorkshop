import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem,
    QHBoxLayout, QCheckBox, QInputDialog
)
from PyQt6.QtGui import QIcon
from database import Database  # Assuming this manages your SQLite database

class ManageWarehouse(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quản Lý Kho")
        self.setGeometry(300, 200, 600, 400)

        self.database = Database()  # Initialize the Database instance
        self.layout = QVBoxLayout()

        self.title_label = QLabel("Danh Sách Sản Phẩm")
        self.layout.addWidget(self.title_label)

        self.product_table = QTableWidget()
        self.product_table.setColumnCount(4)
        self.product_table.setHorizontalHeaderLabels(["Chọn", "Tên Sản Phẩm", "Số Lượng", "Giá"])
        self.layout.addWidget(self.product_table)

        self.button_layout = QHBoxLayout()
        self.add_button = QPushButton("Thêm Sản Phẩm")
        self.add_button.clicked.connect(self.add_product)
        self.button_layout.addWidget(self.add_button)

        self.edit_button = QPushButton("Sửa Sản Phẩm")
        self.edit_button.clicked.connect(self.edit_product)
        self.button_layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("Xóa Sản Phẩm")
        self.delete_button.clicked.connect(self.delete_product)
        self.button_layout.addWidget(self.delete_button)

        self.layout.addLayout(self.button_layout)
        self.setLayout(self.layout)
        self.load_products()
        self.apply_styles()  # Apply styles

    def apply_styles(self):
        style = """
        QWidget {
            background-color: #ffffff;
        }

        QTableWidget {
            background-color: #ffffff;
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

    def load_products(self):
        products = self.database.get_products()  # Fetch products from the database
        self.product_table.setRowCount(len(products))

        for row, (name, quantity, price) in enumerate(products):
            checkbox = QCheckBox()
            self.product_table.setCellWidget(row, 0, checkbox)
            self.product_table.setItem(row, 1, QTableWidgetItem(name))
            self.product_table.setItem(row, 2, QTableWidgetItem(str(quantity)))
            self.product_table.setItem(row, 3, QTableWidgetItem(f"{price:.2f}"))

    def add_product(self):
        name, ok1 = QInputDialog.getText(self, "Thêm Sản Phẩm", "Tên sản phẩm:")
        quantity, ok2 = QInputDialog.getInt(self, "Thêm Sản Phẩm", "Số lượng:")
        price, ok3 = QInputDialog.getDouble(self, "Thêm Sản Phẩm", "Giá:")

        if ok1 and ok2 and ok3 and name:
            self.database.add_product(name, quantity, price)
            QMessageBox.information(self, "Thông Báo", "Sản phẩm đã được thêm!")
            self.load_products()

    def edit_product(self):
        for row in range(self.product_table.rowCount()):
            checkbox = self.product_table.cellWidget(row, 0)
            if checkbox.isChecked():
                current_name = self.product_table.item(row, 1).text()
                new_name, ok_name = QInputDialog.getText(self, "Sửa Sản Phẩm", "Tên sản phẩm mới:", text=current_name)
                new_quantity, ok_quantity = QInputDialog.getInt(self, "Sửa Sản Phẩm", "Số lượng mới:", value=int(self.product_table.item(row, 2).text()))
                new_price, ok_price = QInputDialog.getDouble(self, "Sửa Sản Phẩm", "Giá mới:", value=float(self.product_table.item(row, 3).text()))

                if ok_name and ok_quantity and ok_price and new_name:
                    self.database.update_product(current_name, new_name, new_quantity, new_price)
                    QMessageBox.information(self, "Thông Báo", "Sản phẩm đã được cập nhật!")
                    self.load_products()
                return

        QMessageBox.warning(self, "Cảnh Báo", "Vui lòng chọn sản phẩm để sửa!")

    def delete_product(self):
        for row in range(self.product_table.rowCount()):
            checkbox = self.product_table.cellWidget(row, 0)
            if checkbox.isChecked():
                product_name = self.product_table.item(row, 1).text()
                self.database.delete_product(product_name)
                QMessageBox.information(self, "Thông Báo", "Sản phẩm đã được xóa!")
                self.load_products()
                return

        QMessageBox.warning(self, "Cảnh Báo", "Vui lòng chọn sản phẩm để xóa!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('image/google.png'))  # Set your own icon
    window = ManageWarehouse()
    window.show()
    sys.exit(app.exec())
