import sys
from builtins import print

import requests
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt5.QtGui import QImage, QPixmap

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import ExtractData


class VentanaPrincipal(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyTrade'
        self.left = 0
        self.top = 0
        self.width = 1280
        self.height = 720
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        self.createTable()
        self.setStyleSheet("background-color:white")

        # Add box layout, add table to box layout and add box layout to widget
        self.horizontalGroupBox = QGroupBox()
        self.horizontalGroupBox.setStyleSheet("QGroupBox { border: 0px;}")

        layout = QGridLayout()

        layout.addWidget(QPushButton('Calcular '), 0, 0)
        layout.addWidget(QPushButton('2'), 0, 1)
        layout.addWidget(QPushButton('3'), 0, 2)

        self.horizontalGroupBox.setLayout(layout)

        self.windowLayout = QVBoxLayout()
        self.windowLayout.addWidget(self.horizontalGroupBox)
        self.windowLayout.addWidget(self.tableWidget)

        self.setLayout(self.windowLayout)

        # self.tableLayout.addWidget(, 1)
        # self.tableLayout.insertSpacing(0, 300)
        # self.tableLayout.insertSpacing(2, 300)

        # self.setLayout(self.horizontalGroupBox)

        # Show widget
        self.show()

    def createTable(self):
        extractor = ExtractData.ExtractData()
        self.coinList = extractor.getCoinsMarket()
        print(self.coinList)

        # Set fonts
        self.font_header = QFont()
        self.font_header.setPointSize(10)
        self.font_header.setWeight(QFont.Medium)
        self.font_index = QFont()
        self.font_index.setPointSize(12)
        self.font_index.setWeight(QFont.Medium)
        self.font_name = QFont()
        self.font_name.setPointSize(14)
        self.font_name.setWeight(QFont.Medium)
        self.font_symbol = QFont()
        self.font_symbol.setPointSize(14)
        self.font_symbol.setWeight(QFont.Medium)
        self.font_price = QFont()
        self.font_price.setPointSize(12)
        self.font_price.setWeight(QFont.Medium)

        # Create table
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(len(self.coinList))
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(['#', 'Name', 'Price', '24h %', 'Market cap', 'Available supply'])
        self.tableWidget.move(0, 0)
        self.tableWidget.horizontalHeader().setFont(self.font_header)
        self.tableWidget.horizontalHeader().setStyleSheet("QHeaderView::section { background-color:#eeeeee} ")
        self.tableWidget.horizontalHeader().setSelectionMode(QAbstractItemView.NoSelection)

        # Remove gridlines
        self.tableWidget.setShowGrid(False)
        self.tableWidget.verticalHeader().hide()
        self.tableWidget.setFrameStyle(0)

        # Load rows
        for i in range(len(self.coinList)):
            VentanaPrincipal.addCoin(self, i)

        # self.carga.hide()

        self.show()

    def addCoin(self, i):
        # 1: Market_cap_rank
        url = self.coinList[i]["image"]
        image = QImage()
        image.loadFromData(requests.get(url).content)

        item = QTableWidgetItem(str(self.coinList[i]["market_cap_rank"]))
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        item.setFlags(QtCore.Qt.ItemIsSelectable)
        item.setFont(self.font_index)
        item.setTextAlignment(Qt.AlignCenter)
        item.setForeground(QBrush(QColor(0, 0, 0)))
        self.tableWidget.setItem(i, 0, item)

        # 2: Name
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

        item = QTableWidgetItem(str(self.coinList[i]["name"]))
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        item.setFont(self.font_name)
        item.setForeground(QBrush(QColor(0, 0, 0)))
        item.setTextAlignment(Qt.AlignCenter)
        tablename.setItem(0, 1, item)

        item = QTableWidgetItem(str(self.coinList[i]["symbol"]).upper())
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        item.setFlags(QtCore.Qt.ItemIsSelectable)
        item.setFont(self.font_symbol)
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

        # 3: Price
        item = QTableWidgetItem("$" + str("{:,}".format(self.coinList[i]["current_price"])))
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        item.setFlags(QtCore.Qt.ItemIsSelectable)
        item.setFont(self.font_price)
        item.setForeground(QBrush(QColor(0, 0, 0)))
        item.setTextAlignment(Qt.AlignVCenter)
        self.tableWidget.setItem(i, 2, item)

        # 4: 24h %
        positivo = not str(self.coinList[i]["price_change_percentage_24h"]).startswith("-")
        if positivo:
            item = QTableWidgetItem("▴" + str(self.coinList[i]["price_change_percentage_24h"]) + "%")
        else:
            item = QTableWidgetItem("▾" + str(self.coinList[i]["price_change_percentage_24h"])[1:] + "%")
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        item.setFlags(QtCore.Qt.ItemIsSelectable)
        item.setFont(self.font_price)
        if positivo:
            item.setForeground(QBrush(QColor(0, 255, 0)))
        else:
            item.setForeground(QBrush(QColor(255, 0, 0)))
        item.setTextAlignment(Qt.AlignVCenter)
        self.tableWidget.setItem(i, 3, item)

        # 5:Market cap
        item = QTableWidgetItem("$" + str("{:,}".format(self.coinList[i]["market_cap"])))
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        item.setFlags(QtCore.Qt.ItemIsSelectable)
        item.setFont(self.font_price)
        item.setForeground(QBrush(QColor(0, 0, 0)))
        item.setTextAlignment(Qt.AlignVCenter)
        self.tableWidget.setItem(i, 4, item)

        # 6:Available supply
        widget = QWidget()
        layout = QVBoxLayout()
        pgbar = QProgressBar()
        pgbar.setFixedHeight(10)
        pgbar.setStyleSheet("QProgressBar { border: 1px; border-radius:5px; color:black; background-color:#eeeeee; "
                            "text-align: center; text:; } QProgressBar::chunk {background-color:#f5d033; "
                            "border-radius:5px; } ")
        pgbar.setTextVisible(False)
        if self.coinList[i]["total_supply"] is None:
            total = str(self.coinList[i]["circulating_supply"])
        else:
            total = str(self.coinList[i]["total_supply"])
        parcial = str(self.coinList[i]["circulating_supply"])
        try:
            pgbar.setRange(0, int(float(total)))
        except OverflowError:
            pgbar.setRange(0, int(float(total) / 1000000))
        try:
            pgbar.setValue(int(float(parcial)))
        except OverflowError:
            pgbar.setValue(int(float(parcial) / 1000000))

        layout.addWidget(pgbar)
        label = QLabel(str("{:,}".format(self.coinList[i]["circulating_supply"])) + " "
                       + str(self.coinList[i]["symbol"].upper()))
        label.setFont(self.font_price)
        label.setAlignment(Qt.AlignRight)
        layout.addWidget(label)
        layout.setAlignment(Qt.AlignVCenter)

        widget.setLayout(layout)
        self.tableWidget.setCellWidget(i, 5, widget)

        # Adjusting sizes
        self.tableWidget.verticalHeader().setDefaultSectionSize(70)
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.viewport().repaint()


class VentanaCarga(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'PyTrade'
        self.left = 0
        self.top = 0
        self.width = 512
        self.height = 288
        self.initUI()

    def initUI(self):
        # self.setWindowFlag(Qt.FramelessWindowHint)
        self.setGeometry(self.left, self.top, self.width, self.height)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        oImage = QImage("Image\\logo.jpg")
        sImage = oImage.scaled(QSize(300, 200))  # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # carga = VentanaCarga()
    ex = VentanaPrincipal()
    app.exec_()
    # carga.hide()
