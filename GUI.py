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
        self.left = 0
        self.top = 0
        self.width = 300
        self.height = 200
        self.initUI()
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
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
        self.tableWidget.setColumnCount(3)

        font_index = QFont("Inter Semi Bold", 12)
        font_name = QFont("Inter Semi Bold", 14)
        font_symbol = QFont("Inter Medium", 14)
        font_price = QFont("Inter Medium", 14)

        for i in range(10):
            url = list[i]["image"]
            image = QImage()
            image.loadFromData(requests.get(url).content)

            item = QTableWidgetItem(str(list[i]["market_cap_rank"]))
            item.setFont(font_index)
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget.setItem(i, 0, item)

            tablename = QTableWidget()
            tablename.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
            tablename.setColumnCount(3)
            tablename.setRowCount(1)
            tablename.setShowGrid(False)
            tablename.horizontalHeader().hide()
            tablename.verticalHeader().hide()

            label = QtWidgets.QLabel()
            label.setPixmap(QPixmap(image.smoothScaled(25, 25)))
            tablename.setCellWidget(0, 0, label)

            item = QTableWidgetItem(str(list[i]["name"]))
            item.setFont(font_name)
            item.setTextAlignment(Qt.AlignCenter)
            tablename.setItem(0, 1, item)

            item = QTableWidgetItem(str(list[i]["symbol"]).upper())
            item.setFont(font_symbol)
            item.setForeground(QBrush(QColor(160, 160, 160)))
            item.setTextAlignment(Qt.AlignCenter)
            tablename.setItem(0, 2, item)

            tablename.resizeColumnsToContents()
            tablename.setFixedHeight(30)
            tablename.adjustSize()
            tablename.setFrameStyle(0)
            layout = QVBoxLayout()
            layout.addWidget(tablename)
            layout.setAlignment(Qt.AlignCenter)
            widget = QWidget()
            widget.setLayout(layout)

            self.tableWidget.setCellWidget(i, 1, widget)

            item = QTableWidgetItem(str(list[i]["current_price"]))
            item.setFont(font_price)
            item.setTextAlignment(Qt.AlignVCenter)
            self.tableWidget.setItem(i, 2, item)

        self.tableWidget.move(0, 0)

        # Adjust to content
        self.tableWidget.verticalHeader().setDefaultSectionSize(50)
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