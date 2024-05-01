import sys
import json
from PyQt6.QtWidgets import QApplication, QWidget, QTableWidgetItem
from ui_main import Ui_Form


class MyWidget(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # загрузка списка и таблицы
        with open('items.json') as items:
            self.loc_items = json.load(items)
            loc_items_l = len(self.loc_items)
            self.tableWidget.setRowCount(loc_items_l)
            self.tableWidget.setColumnCount(3)
            self.updtable()
            self.lcd.display(loc_items_l)

        self.cboxcng()

        # подключение кнопок
        self.yes_btn.clicked.connect(self.buttons)
        self.no_btn.clicked.connect(self.buttons)
        self.reset_btn.clicked.connect(self.buttons)
        self.apply_btn.clicked.connect(self.buttons)
        self.ok_btn.clicked.connect(self.buttons)
        self.safe_btn.clicked.connect(self.buttons)
        self.up_btn.clicked.connect(self.buttons)
        self.down_btn.clicked.connect(self.buttons)
        self.comboBox.currentTextChanged.connect(self.cboxcng)

    # функции кнопок
    def buttons(self):
        if self.sender() == self.yes_btn:
            self.yes_lbl.setText(f"{int(self.yes_lbl.text()) + 1}")
        if self.sender() == self.no_btn:
            self.no_lbl.setText(f"{int(self.no_lbl.text()) + 1}")
        if self.sender() == self.safe_btn:
            q_text = self.q_lbl.text()
            if q_text not in self.loc_items.keys():
                self.lcd.display(f"{self.lcd.intValue() + 1}")
                self.comboBox.addItem(q_text)
                self.tableWidget.insertRow(self.tableWidget.rowCount())
                self.loc_items[q_text] = [self.tableWidget.rowCount() - 1, self.yes_lbl.text(), self.no_lbl.text()]
            else:
                self.loc_items[q_text][1] = self.yes_lbl.text()
                self.loc_items[q_text][2] = self.no_lbl.text()
            self.updtable()
        if self.sender() == self.reset_btn:
            self.yes_lbl.setText('0')
            self.no_lbl.setText('0')
        if self.sender() == self.ok_btn:
            self.q_lbl.setText(self.q_line.text())
        if self.sender() == self.apply_btn:
            self.yes_lbl.setText(self.yes_spin.text())
            self.no_lbl.setText(self.no_spin.text())
        if self.sender() == self.up_btn:
            crkey = self.tableWidget.item(self.tableWidget.currentRow(), 0).text()
            uppkey = self.tableWidget.item(self.tableWidget.currentRow() - 1, 0).text()
            self.loc_items[crkey][0] = self.loc_items[crkey][0] - 1
            self.loc_items[uppkey][0] = self.loc_items[uppkey][0] + 1
            self.updtable()
        if self.sender() == self.down_btn:
            crkey = self.tableWidget.item(self.tableWidget.currentRow(), 0).text()
            lowkey = self.tableWidget.item(self.tableWidget.currentRow() + 1, 0).text()
            self.loc_items[crkey][0] = self.loc_items[crkey][0] + 1
            self.loc_items[lowkey][0] = self.loc_items[lowkey][0] - 1
            self.updtable()

    # рисует строку по ключу
    def drawrow(self, key):
        self.tableWidget.setItem(self.loc_items[key][0], 0, QTableWidgetItem(key))
        self.tableWidget.setItem(self.loc_items[key][0], 1, QTableWidgetItem(self.loc_items[key][1]))
        self.tableWidget.setItem(self.loc_items[key][0], 2, QTableWidgetItem(self.loc_items[key][2]))

    # обновляет таблицу
    def updtable(self):
        for key in self.loc_items.keys():
            self.drawrow(key)
        self.comboBox.clear()
        self.comboBox.addItems(sorted(self.loc_items.keys(), key=lambda key: self.loc_items[key][0]))

    # меняет все по комбо-боксу
    def cboxcng(self):
        curtext = self.comboBox.currentText()
        if curtext in self.loc_items.keys():
            self.q_lbl.setText(curtext)
            self.yes_lbl.setText(self.loc_items[curtext][1])
            self.no_lbl.setText(self.loc_items[curtext][2])

    # действие при закрытии
    def closeEvent(self, event):
        with open('items.json', 'w') as items:
            json.dump(self.loc_items, items)
        event.accept()

    # декствие при нажатии клавишы
    def keyPressEvent(self, event):
        if self.q_line.hasFocus() and event.key() == 16777220:
            self.ok_btn.click()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
