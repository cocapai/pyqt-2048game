#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import (QWidget, QToolTip,
    QPushButton, QApplication, QMessageBox, QDesktopWidget)

from PyQt5.QtCore import QCoreApplication

from PyQt5.QtGui import QIcon, QFont

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI() # 使用initUI()方法创建一个GUI


    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10)) # 设置了提示框的字体
        self.setToolTip('This is a <b>QWidget</b> widget') # 为应用创建了一个提示框
        # 创建一个按钮，并且为按钮添加了一个提示框
        btn = QPushButton('Quit', self) # 第一个参数是按钮的文本，第二个参数是按钮的父级组件
        btn.clicked.connect(QCoreApplication.instance().quit)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.resize(btn.sizeHint()) # 调整按钮大小
        btn.move(50, 50)

        # self.setGeometry(300, 300, 300, 220) # 把窗口放到屏幕上并且设置窗口大小。参数分别代表屏幕坐标的x、y和窗口大小的宽、高
        self.center()
        self.setWindowTitle('Icon')
        self.setWindowIcon(QIcon('smile.png'))

        self.show()

    def closeEvent(self, event): # 内置方法，重写
        reply = QMessageBox.question(self, 'Message',
                                     'Are you sure to quit?',
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def center(self):
        widget_windows_size = self.frameGeometry() # 得到了主窗口的大小
        user_windows_center = QDesktopWidget().availableGeometry().center() # 获取显示器分辨率的中间点的位置
        widget_windows_size.moveCenter(user_windows_center) # 将窗口的中心店移动到显示器的中心点
        self.move(widget_windows_size.topLeft())


if __name__ == '__main__':

    app = QApplication(sys.argv) # 创建一个应用对象

    ex = Example()

    sys.exit(app.exec_()) # 进入了应用的主循环中，事件处理器这个时候开始工作