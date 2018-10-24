#!/usr/bin/evn python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:       mian
   Description:     
   Author:          litong
   date:            2018/10/23
-------------------------------------------------
   Change Activity: 2018/10/23:
-------------------------------------------------
"""
import sys
import random

from PyQt5.QtGui import QIcon, QPalette, QColor, QFont
from PyQt5.QtWidgets import (QWidget, QGridLayout,
                             QPushButton, QApplication, QLabel, QLineEdit, QTextEdit, QMessageBox, QLCDNumber)
from PyQt5.QtCore import Qt, QTimer, QDateTime, QDate, QTime

ROW = 4
COL = 4

NUM_MAP_COLOR = {
    '0': {
        'background': QColor(0xcdc1b4),
        'font': QColor(0xcdc1b4)
    },
    '2': {
        'background': QColor(0xeee4da),
        'font': QColor(0x776e65)
    },
    '4': {
        'background': QColor(0xede0c8),
        'font': QColor(0x776e65)
    },
    '8': {
        'background': QColor(0xf2b179),
        'font': QColor(0xffffff)
    },
    '16': {
        'background': QColor(0xf59563),
        'font': QColor(0xffffff)
    },
    '32': {
        'background': QColor(0xf67c5f),
        'font': QColor(0xffffff)
    },
    '64': {
        'background': QColor(0xf65e3b),
        'font': QColor(0xffffff)
    },
    '128': {
        'background': QColor(0xedcf72),
        'font': QColor(0xffffff)
    },
    '256': {
        'background': QColor(0xedcc61),
        'font': QColor(0xffffff)
    },
    '512': {
        'background': QColor(0xedc850),
        'font': QColor(0xffffff)
    },
    '1024': {
        'background': QColor(0xedc53f),
        'font': QColor(0xffffff)
    },
    '2048': {
        'background': QColor(0xedc22e),
        'font': QColor(0xffffff)
    }
}


class Game(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        grid = QGridLayout()
        grid.setSpacing(10)  # 创建标签之间的空间。
        self.labels = []
        self.palettes = []
        for i in range(ROW ** 2):
            # create label
            label = QLabel('0', self)
            label.setAlignment(Qt.AlignCenter)  # 居中显示
            label.setFixedWidth(80)
            label.setFixedHeight(80)
            label.setFont(QFont("Arial", 20, QFont.Bold))  # 粗体
            grid.addWidget(label, i // ROW, i % ROW)
            self.labels.append(label)
            # create palette
            pe = QPalette()
            pe.setColor(QPalette.WindowText, NUM_MAP_COLOR['0']['font'])
            label.setAutoFillBackground(True)  # 设置背景充满，为设置背景颜色的必要条件
            pe.setColor(QPalette.Window, NUM_MAP_COLOR['0']['background'])  # 设置背景颜色
            label.setPalette(pe)
            self.palettes.append(pe)
        self.randomSetLabels(2)

        self.succeed = False
        self.isMove = False
        self.isLose = False

        # lcd
        self.lcd = QLCDNumber(self)
        lb = QLabel("game running time : ", self)
        self.lcd.setDigitCount(8)
        self.lcd.setMode(QLCDNumber.Dec)
        self.lcd.setStyleSheet("border: 2px solid black; color: red; background: silver;")
        grid.addWidget(lb, 4, 0, 1, 2)
        grid.addWidget(self.lcd, 4, 2, 1, 2)
        # debug label
        self.__debug_label = QLabel('debug text', self)
        grid.addWidget(self.__debug_label, 5, 0, 4, 4)
        self.setLayout(grid)

        # timer
        self.second_count = 0
        time = QTimer(self)
        time.setInterval(1000)
        time.timeout.connect(self.refresh)
        time.start()

        self.setGeometry(300, 300, 400, 600)
        self.setWindowTitle('2048 game')
        self.setWindowIcon(QIcon('2048.png'))
        self.show()

    def refresh(self):
        self.second_count += 1
        sec = self.second_count % 60
        min = int(self.second_count / 60) % 60
        hour = int(self.second_count / 60 / 60) % 60
        sec_str = str(sec) if sec > 9 else '0' + str(sec)
        min_str = str(sec) if min > 9 else '0' + str(min)
        hour_str = str(sec) if hour > 9 else '0' + str(hour)
        show_num = '{}:{}:{}'.format(hour_str, min_str, sec_str)
        self.lcd.display(show_num)

    def resetLabel(self):
        for i in range(ROW * COL):
            self.setTextAndColor(i, '0', setIsMove=False)
        self.randomSetLabels(2)
        self.second_count = 0

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Up:
            self.__debug_label.setText('↑')
            self.gridMove('up')
        elif e.key() == Qt.Key_Down:
            self.__debug_label.setText('↓')
            self.gridMove('down')
        elif e.key() == Qt.Key_Left:
            self.__debug_label.setText('←')
            self.gridMove('left')
        elif e.key() == Qt.Key_Right:
            self.__debug_label.setText('→')
            self.gridMove('right')
        elif e.key() == Qt.Key_R:
            self.resetLabel()

    def gridMove(self, dir):
        self.removeEmptyLabel(dir)
        self.mergeSameLabel(dir)
        if self.isLose:
            self.gameOver()
        if self.succeed:
            self.gameSuccess()
        if self.isMove:
            self.isMove = False
            self.randomSetLabels(1)

    def removeEmptyLabel(self, dir):
        self.isLose = True
        if dir == 'right':
            for i in range(ROW):  # 每一行
                row_point = []  # 记录所有有效值
                for j in range(COL - 1, -1, -1):
                    if self.labels[i * ROW + j].text() != '0':
                        row_point.append(self.labels[i * ROW + j].text())
                    else:
                        self.isLose = False
                j = COL - 1
                # 依次填充有效值
                for text in row_point:
                    self.setTextAndColor(i * ROW + j, text)
                    j -= 1
                # 剩余label补零
                while j != -1:
                    self.setTextAndColor(i * ROW + j, '0')
                    j -= 1
        elif dir == 'left':
            for i in range(ROW):  # 每一行
                row_point = []
                for j in range(COL):
                    if self.labels[i * ROW + j].text() != '0':
                        row_point.append(self.labels[i * ROW + j].text())
                    else:
                        self.isLose = False
                j = 0
                for text in row_point:
                    self.setTextAndColor(i * ROW + j, text)
                    j += 1
                while j != COL:
                    self.setTextAndColor(i * ROW + j, '0')
                    j += 1
        elif dir == 'up':
            for j in range(COL):  # 每一行
                row_point = []
                for i in range(ROW):
                    if self.labels[i * ROW + j].text() != '0':
                        row_point.append(self.labels[i * ROW + j].text())
                    else:
                        self.isLose = False
                i = 0
                for text in row_point:
                    self.setTextAndColor(i * ROW + j, text)
                    i += 1
                while i != ROW:
                    self.setTextAndColor(i * ROW + j, '0')
                    i += 1
        elif dir == 'down':
            for j in range(COL):  # 每一行
                col_point = []
                for i in range(ROW - 1, -1, -1):
                    if self.labels[i * ROW + j].text() != '0':
                        col_point.append(self.labels[i * ROW + j].text())
                    else:
                        self.isLose = False
                i = ROW - 1
                for text in col_point:
                    self.setTextAndColor(i * ROW + j, text)
                    i -= 1
                while i != -1:
                    self.setTextAndColor(i * ROW + j, '0')
                    i -= 1

    def mergeSameLabel(self, dir):
        if dir == 'right':
            for j in range(ROW):  # 每一行
                for i in range(COL - 1, 0, -1):  # 每一列
                    right_label = self.labels[j * ROW + i]  # 每一行中相邻两个靠右的label
                    left_label = self.labels[j * ROW + i - 1]  # 靠左的label
                    if right_label.text() == left_label.text():  # 两个格相等
                        num = int(right_label.text())
                        self.finishedMerge(j * ROW + i, num * 2)
                        self.setTextAndColor(j * ROW + i, str(num * 2))
                        for k in range(i - 1, 0, -1):  # 依次右移一格
                            self.setTextAndColor(j * ROW + k, self.labels[j * ROW + k - 1].text())
                        self.setTextAndColor(j * ROW + 0, '0')
                        break
        elif dir == 'left':
            for j in range(ROW):  # 每一行
                for i in range(COL - 1):  # 每一列
                    right_label = self.labels[j * ROW + i + 1]
                    left_label = self.labels[j * ROW + i]
                    if right_label.text() == left_label.text():  # 两个格相等
                        num = int(left_label.text())
                        self.finishedMerge(j * ROW + i, num * 2)
                        self.setTextAndColor(j * ROW + i, str(num * 2))
                        for k in range(i + 1, COL - 1):
                            self.setTextAndColor(j * ROW + k, self.labels[j * ROW + k + 1].text())
                        self.setTextAndColor(j * ROW + COL - 1, '0')
                        break
        elif dir == 'down':
            for i in range(COL):
                for j in range(ROW - 1, 0, -1):
                    up_label = self.labels[(j - 1) * ROW + i]
                    down_label = self.labels[j * ROW + i]
                    if up_label.text() == down_label.text():  # 两个格相等
                        num = int(down_label.text())
                        self.finishedMerge(j * ROW + i, num * 2)
                        self.setTextAndColor(j * ROW + i, str(num * 2))
                        for k in range(j - 1, 0, -1):
                            self.setTextAndColor(k * ROW + i, self.labels[(k - 1) * ROW + i].text())
                        self.setTextAndColor(0 * ROW + i, '0')
                        break
        elif dir == 'up':
            for i in range(COL):
                for j in range(ROW - 1):
                    up_label = self.labels[j * ROW + i]
                    down_label = self.labels[(j + 1) * ROW + i]
                    if up_label.text() == down_label.text():  # 两个格相等
                        num = int(up_label.text())
                        self.finishedMerge(j * ROW + i, num * 2)
                        self.setTextAndColor(j * ROW + i, str(num * 2))
                        for k in range(j + 1, ROW - 1):
                            self.labels[k * ROW + i].setText(self.labels[(k + 1) * ROW + i].text())
                            self.setTextAndColor(k * ROW + i, self.labels[(k + 1) * ROW + i].text())
                        self.setTextAndColor((COL - 1) * ROW + i, '0')
                        break

    def randomSetLabels(self, nums):
        empty_grids = self.getEmptyGrid()
        num_strs = '22244'
        for _ in range(nums):
            num = random.choice(num_strs)  # todo 添加权重
            label_index = random.choice(empty_grids)
            self.setTextAndColor(label_index, num, setIsMove=False)

    def getEmptyGrid(self):
        results = [index for index, labels in enumerate(self.labels) if labels.text() == '0']
        return results

    def gameSuccess(self):
        button = QMessageBox.question(self, "Congratulations",
                                      "You are very NB! Do you want to restart?",
                                      QMessageBox.Ok | QMessageBox.Cancel,
                                      QMessageBox.Ok)
        if button == QMessageBox.Ok:
            self.resetLabel()
            self.__debug_label.setText("Question button/Ok")
        elif button == QMessageBox.Cancel:
            self.__debug_label.setText("Question button/Cancel")

    def setTextAndColor(self, index, num, setIsMove=True):
        if setIsMove:
            pre_text = self.labels[index].text()
            if pre_text != num:
                self.isMove = True

        self.labels[index].setText(num)
        self.palettes[index].setColor(QPalette.WindowText, NUM_MAP_COLOR[num]['font'])
        self.palettes[index].setColor(QPalette.Window, NUM_MAP_COLOR[num]['background'])
        self.labels[index].setPalette(self.palettes[index])

    def finishedMerge(self, index, num):
        if num == 2048:
            self.succeed = True
        self.isLose = False

    def gameOver(self):
        button = QMessageBox.question(self, "Sorry",
                                      "Game over! Do you want to restart?",
                                      QMessageBox.Ok | QMessageBox.Cancel,
                                      QMessageBox.Ok)
        if button == QMessageBox.Ok:
            self.resetLabel()
            self.__debug_label.setText("Question button/Ok")
        elif button == QMessageBox.Cancel:
            self.__debug_label.setText("Question button/Cancel")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Game()
    sys.exit(app.exec_())
