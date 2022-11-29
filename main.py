import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class Edit(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)


class DBSample(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.edit_w = Edit()
        self.connection = sqlite3.connect("coffee.sqlite")
        self.cur = self.connection.cursor()
        self.select_data()
        self.pushButton.clicked.connect(self.open_edit)
        self.edit_w.add.clicked.connect(self.add_f)
        self.edit_w.change.clicked.connect(self.change_f)

    def select_data(self):
        self.tableWidget.clear()
        query = '''select * from coffee'''
        res = self.connection.cursor().execute(query).fetchall()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(
            ['ID', 'название сорта', 'степень обжарки', 'молотый/в зернах', 'описание вкуса', 'цена', 'объем упаковки'])
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()

    def closeEvent(self, event):
        self.connection.close()

    def open_edit(self):
        self.edit_w.show()
        self.edit_w.comboBox.addItems(
            [elem[0] for elem in self.cur.execute('SELECT DISTINCT title FROM coffee').fetchall()])

    def add_f(self):
        self.cur.execute('INSERT into coffee(title, roasting, form, taste, price, volume) VALUES(?, ?, ?, ?, ?, ?)',
                         (self.edit_w.title1.text(), self.edit_w.roast1.text(), self.edit_w.form1.text(),
                          self.edit_w.taste1.text(), self.edit_w.price1.value(),
                          self.edit_w.value1.value(),))
        self.connection.commit()
        self.edit_w.comboBox.addItems(
            [elem[0] for elem in self.cur.execute('SELECT DISTINCT title FROM coffee').fetchall()])
        self.select_data()

    def change_f(self):
        self.cur.execute('DELETE FROM coffee WHERE title = ?',
                         (self.edit_w.comboBox.currentText(),))
        self.cur.execute('INSERT into coffee(title, roasting, form, taste, price, volume) VALUES(?, ?, ?, ?, ?, ?)',
                         (self.edit_w.title1.text(), self.edit_w.roast1.text(), self.edit_w.form1.text(),
                          self.edit_w.taste1.text(), self.edit_w.price1.value(),
                          self.edit_w.value1.value(),))
        self.connection.commit()
        self.select_data()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DBSample()
    ex.show()
    sys.exit(app.exec())
