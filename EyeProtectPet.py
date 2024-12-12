'''
@-*- coding: utf-8 -*-
@Project ：EyeProtectPet
@File    ：EyeProtectPet.py
@Author  ：Weaud
@Date    ：2024/12/10
@explain : 期望实现桌面随机位置出现宠物，眼睛跟随，起到护眼作用
'''

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import os
import random
import math

class Pet(object):
    def __init__(self, width=800, height=400):
        self.image = 'images/xiaogou/xiaogou_0.png'  # 导入图像
        self.rect_x = width
        self.rect_y = height

class App(QWidget):
    def __init__(self):
        super(App, self).__init__()

        self.pet = Pet()
        self.pm_pet = QPixmap(self.pet.image)
        self.lb_pet = QLabel(self)  # 创建标签来显示宠物图像

        self.init_ui()

        # 创建定时器，每 1 秒调用一次 move_pet 方法
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.move_pet)
        self.timer.start(1000)

        # 创建一个定时器，10 秒后关闭窗口
        self.close_timer = QTimer(self)
        self.close_timer.timeout.connect(self.close_app)
        self.close_timer.setSingleShot(True)  # 只触发一次
        self.close_timer.start(10000)  # 10 秒后触发

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


    def move_pet(self):
        # 随机生成新的位置
        screen = QDesktopWidget().screenGeometry()
        new_x = random.randint(0, screen.width() - self.pm_pet.width())
        new_y = random.randint(0, screen.height() - self.pm_pet.height())

        # 移动宠物标签到新位置
        self.lb_pet.move(new_x, new_y)

    '''
    def move_pet(self):
        # 随机生成新的目标位置
        screen = QDesktopWidget().screenGeometry()
        new_x = random.randint(0, screen.width() - self.pm_pet.width())
        new_y = random.randint(0, screen.height() - self.pm_pet.height())

        # 使用动画将标签平滑移动到新位置
        self.animation = QPropertyAnimation(self.lb_pet, b"pos")
        self.animation.setDuration(2000)  # 动画持续时间为 2 秒
        self.animation.setStartValue(self.lb_pet.pos())
        self.animation.setEndValue(QPoint(new_x, new_y))
        self.animation.start()
    '''

    def close_app(self):
        # 关闭窗口
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    pet = App()
    sys.exit(app.exec_())

