#!/usr/bin/evn python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:       test4
   Description:     
   Author:          litong
   date:            2018/10/23
-------------------------------------------------
   Change Activity: 2018/10/23:
-------------------------------------------------
"""
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QLCDNumber, QSlider,
                             QVBoxLayout, QApplication, QGridLayout, QLabel, QPushButton)


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        grid.setSpacing(10)

        x = 0
        y = 0

        self.text = "x: {0},  y: {1}".format(x, y)

        self.label = QLabel(self.text, self)
        grid.addWidget(self.label, 0, 0, Qt.AlignTop)

        self.setMouseTracking(True)


        lcd = QLCDNumber(self)
        sld = QSlider(Qt.Horizontal, self)  # 水平

        grid.addWidget(lcd, 1, 0)
        grid.addWidget(sld, 2, 0)

        btn1 = QPushButton('button 1', self)
        btn2 = QPushButton('button 2', self)

        grid.addWidget(btn1, 4, 0)
        grid.addWidget(btn2, 4, 1)

        self.setLayout(grid)

        sld.valueChanged.connect(lcd.display)  # 把滑块的变化和数字的变化绑定在一起
        btn1.clicked.connect(self.buttonClicked)
        btn2.clicked.connect(self.buttonClicked)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Signal and slot')
        self.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    def mouseMoveEvent(self, e):
        x = e.x()
        y = e.y()

        text = "x: {0},  y: {1}".format(x, y)
        self.label.setText(text)

    def buttonClicked(self):
        sender = self.sender()
        self.label.setText(sender.text() + ' was pressed')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
