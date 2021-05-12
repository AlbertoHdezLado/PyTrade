import sys

import requests
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt5.QtGui import QIcon, QImage, QPixmap

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import ExtractData


class GUI(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyTrade'
        #self.setStyleSheet('font-size: 15px', 'font-style:Inter Semi Bold')
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

        font_index = QFont("Inter Semi Bold", 12)
        font_name = QFont("Inter Semi Bold", 14)
        font_symbol = QFont("Inter Medium", 14)
        font_price = QFont("Inter Medium", 14)

        self.tableWidget.setRowCount(len(list))
        self.tableWidget.setColumnCount(5)
        for i in range(5):
            url = list[i]["image"]
            image = QImage()
            image.loadFromData(requests.get(url).content)

            label = QtWidgets.QLabel()
            label.setPixmap(QPixmap(image.smoothScaled(25, 25)))

            item = QTableWidgetItem(str(list[i]["market_cap_rank"]))
            item.setFont(font_index)
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget.setItem(i, 0, item)

            #self.tableWidget.setCellWidget(i, 1, label)

            item = QTableWidgetItem(str(list[i]["name"]))
            item.setFont(font_name)
            item.setTextAlignment(Qt.AlignCenter)
            #self.tableWidget.setItem(i, 2, item)



            item = QTableWidgetItem(str(list[i]["symbol"]).upper())
            item.setFont(font_symbol)
            item.setForeground(QBrush(QColor(160, 160, 160)))
            item.setTextAlignment(Qt.AlignCenter)
            #self.tableWidget.setItem(i, 3, item)



            item = QTableWidgetItem(str(list[i]["current_price"]))
            item.setFont(font_price)
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget.setItem(i, 4, item)

        self.tableWidget.move(0, 0)

        # Adjust to content
        self.tableWidget.verticalHeader().setDefaultSectionSize(50)
        self.tableWidget.setFixedWidth(600)
        self.tableWidget.resizeColumnsToContents()

        # Remove gridlines
        self.tableWidget.setShowGrid(False)
        self.tableWidget.horizontalHeader().hide()
        self.tableWidget.verticalHeader().hide()

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