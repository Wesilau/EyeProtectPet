'''
@-*- coding: utf-8 -*-
@Project ：EyeProtectPet
@File    ：EyeProtectPet.py
@Author  ：Weaud
@Date    ：2024/12/10
@explain : 期望实现桌面随机位置出现宠物，眼睛跟随，起到护眼作用
'''

from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
import sys

class Pet(object):
    def __init__(self, width=800, height=400):
        self.image = 'images/xiaogou/xiaogou_0.png'  # 使用静态图像
        self.rect_x = width
        self.rect_y = height

class App(QWidget):
    def __init__(self):
        super(App, self).__init__()

        self.pet = Pet()
        self.pm_pet = QPixmap(self.pet.image)
        self.lb_pet = QLabel(self)  # 创建标签来显示宠物图像

        self.init_ui()

    def init_ui(self):
        # 设置窗口为全屏
        screen = QDesktopWidget().screenGeometry()
        self.setGeometry(0, 0, screen.width(), screen.height())

        # 设置宠物标签的图像和位置
        self.lb_pet.setPixmap(self.pm_pet)
        self.lb_pet.move(self.pet.rect_x, self.pet.rect_y)

        # 设置窗口无边框并且总是显示在最上层
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.showMaximized()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    pet = App()
    sys.exit(app.exec_())

