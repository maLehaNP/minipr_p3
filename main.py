import sys
import json
from PyQt6.QtWidgets import QApplication, QWidget, QTableWidgetItem
from uiminip import Ui_Form


class MyWidget(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # загрузка списка и таблицы
        with open('items.json') as items:
            self.loc_items = json.load(items)
            for row in self.loc_items:
                self.rowmaker(row)

        # подключение кнопок
        self.yes_btn.clicked.connect(self.buttons)
        self.no_btn.clicked.connect(self.buttons)
        self.safe_btn.clicked.connect(self.buttons)
        self.reset_btn.clicked.connect(self.buttons)
        self.apply_btn.clicked.connect(self.buttons)
        self.ok_btn.clicked.connect(self.buttons)
        self.add_btn.clicked.connect(self.buttons)

    # функция кнопок
    def buttons(self):
        if self.sender() == self.yes_btn:
            self.yes_lbl.setText(f"{int(self.yes_lbl.text()) + 1}")
        if self.sender() == self.no_btn:
            self.no_lbl.setText(f"{int(self.no_lbl.text()) + 1}")
        if self.sender() == self.add_btn:
            new_item = [self.q_lbl.text(), self.yes_lbl.text(), self.no_lbl.text()]
            self.loc_items = self.loc_items + [new_item]
            self.rowmaker(new_item)
            print(self.loc_items)
        if self.sender() == self.safe_btn:
            self.safe()
        if self.sender() == self.reset_btn:
            self.yes_lbl.setText('0')
            self.no_lbl.setText('0')
        if self.sender() == self.ok_btn:
            self.q_lbl.setText(self.q_line.text())
        if self.sender() == self.apply_btn:
            self.yes_lbl.setText(self.yes_spin.text())
            self.no_lbl.setText(self.no_spin.text())

    # рисует строку
    def rowmaker(self, lst):
        rc = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rc)
        for i in range(3):
            self.tableWidget.setItem(rc, i, QTableWidgetItem(lst[i]))

    # сохранение значений
    def safe(self):
        with open('items.json', 'w') as items:
            json.dump(self.loc_items, items)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
