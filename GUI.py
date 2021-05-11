import sys

import requests
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt5.QtGui import QIcon, QImage, QPixmap
from PyQt5.QtCore import pyqtSlot

import ExtractData


class GUI(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyTrade'
        self.left = 0
        self.top = 0
        self.width = 300
        self.height = 200
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createTable()

        # Add box layout, add table to box layout and add box layout to widget
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)

        # Show widget
        self.show()

    def createTable(self):
        extractor = ExtractData.ExtractData()
        list = extractor.getCoinsMarket()
        print(list)

        # Create table
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(len(list))
        self.tableWidget.setColumnCount(4)
        for i in range(len(list)):

            url = list[i]["image"]
            image = QImage()
            image.loadFromData(requests.get(url).content)

            label = QtWidgets.QLabel()
            label.setPixmap(QPixmap(image.smoothScaled(20, 20)))

            self.tableWidget.setCellWidget(i, 0, label)
            self.tableWidget.setItem(i, 1, QTableWidgetItem(list[i]["name"]))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(list[i]["symbol"]))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(str((list[i]["current_price"]))))

        self.tableWidget.move(0, 0)

        self.tableWidget.resizeRowsToContents()
        self.tableWidget.resizeColumnsToContents()

        # table selection change
        self.tableWidget.doubleClicked.connect(self.on_click)

    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GUI()
    sys.exit(app.exec_())