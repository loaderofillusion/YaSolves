import sqlite3
import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI.ui", self)

        # название файла и таблица под твой проект
        self.con = sqlite3.connect("coffe_db.sqlite")

        self.pushButton.clicked.connect(self.update_result)
        self.tableWidget.itemChanged.connect(self.item_changed)
        self.pushButton_2.clicked.connect(self.save_results)

        self.modified = {}
        self.titles = None

    def update_result(self):
        try:
            cur = self.con.cursor()
            item_id = self.spinBox.value()  # ID из спинбокса (целое)
            result = cur.execute(
                "SELECT ID, sort, roast_level, is_ground, taste, volume, price "
                "FROM coffee WHERE ID = ?",
                (item_id,)
            ).fetchall()
        except Exception as e:
            print("DB error:", e)
            self.statusBar().showMessage(f"Ошибка БД: {e}")
            return

        self.tableWidget.blockSignals(True)

        self.tableWidget.setRowCount(len(result))
        if not result:
            self.statusBar().showMessage(f"Ничего не нашлось для ID = {item_id}")
            self.tableWidget.blockSignals(False)
            return
        else:
            self.statusBar().showMessage(f"Нашлась запись с ID = {item_id}")

        self.tableWidget.setColumnCount(7)
        self.titles = ["ID", "sort", "roast_level", "is_ground", "taste", "volume", "price"]

        # заголовки (если нужно)
        self.tableWidget.setHorizontalHeaderLabels(self.titles)

        for i, row in enumerate(result):
            for j, val in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

        self.tableWidget.blockSignals(False)
        self.modified = {}

    def item_changed(self, item):
        if not self.titles:
            return
        col = item.column()
        if 0 <= col < len(self.titles):
            col_name = self.titles[col]
            self.modified[col_name] = item.text()

    def save_results(self):
        if not self.modified:
            return

        cur = self.con.cursor()
        set_part = ", ".join([f"{key} = ?" for key in self.modified.keys()])
        que = f"UPDATE coffee SET {set_part} WHERE ID = ?"

        params = list(self.modified.values())
        params.append(self.spinBox.value())

        try:
            cur.execute(que, params)
            self.con.commit()
            self.statusBar().showMessage("Изменения сохранены")
            self.modified.clear()
        except Exception as e:
            print("DB save error:", e)
            self.statusBar().showMessage(f"Ошибка сохранения: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
