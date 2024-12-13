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
    def __init__(self, width=400, height=400):
        # self.image = 'images/xiaogou/xiaogou_0.png'  # 导入图像
        self.image_url = 'images/xiaogou/xiaogou_'
        self.image_key = 1
        self.image = self.image_url + str(self.image_key) + '.png'

        self.rect_x = width
        self.rect_y = height
        self.image_num = 23  # 图片数量

    def gif(self):
        if self.image_key < self.image_num - 1:
            self.image_key += 1
        else:
            self.image_key = 1
        self.image = self.image_url + str(self.image_key) + '.png'


class App(QWidget):
    def __init__(self):
        super(App, self).__init__()

        self.pet = Pet()
        self.pm_pet = QPixmap(self.pet.image)
        self.lb_pet = QLabel(self)  # 创建标签来显示宠物图像

        self.init_ui()

        # 创建定时器，调用 move_pet 方法
        self.move_timer = QTimer(self)
        self.move_timer.timeout.connect(self.move_pet)
        self.move_timer.start((self.pet.image_num + 1) * 100)

        # 创建一个定时器，10 秒后关闭窗口
        self.close_timer = QTimer(self)
        self.close_timer.timeout.connect(self.close_app)
        self.close_timer.setSingleShot(True)  # 只触发一次
        self.close_timer.start((self.pet.image_num + 1) * 100 * 8)  # 10 秒后触发

        # 创建一个定时器，0.1 秒更新图片实现gif效果
        self.gif_timer = QTimer(self)
        self.gif_timer.timeout.connect(self.gem)
        self.gif_timer.start(100)

    def gem(self):
        # 宠物实现gif效果
        self.pet.gif()
        self.pm_pet = QPixmap(self.pet.image)
        self.lb_pet.setPixmap(self.pm_pet)
        pass

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

        # 记录上次宠物所在的区域
        self.last_area = None


    def move_pet(self):
        # 随机生成新的位置
        screen = QDesktopWidget().screenGeometry()

        # 将屏幕分成四个区域
        width = screen.width() // 2
        height = screen.height() // 2

        areas = [(0, 0, width, height),  # 上左
                 (width, 0, width, height),  # 上右
                 (0, height, width, height),  # 下左
                 (width, height, width, height)]  # 下右

        # 随机选择一个区域，但不能是上次的区域
        available_areas = [area for area in areas if area != self.last_area]
        new_area = random.choice(available_areas)

        # 获取新的随机位置
        new_x = random.randint(new_area[0], new_area[0] + new_area[2] - self.pm_pet.width())
        new_y = random.randint(new_area[1], new_area[1] + new_area[3] - self.pm_pet.height())

        # new_x = random.randint(0, screen.width() - self.pm_pet.width())
        # new_y = random.randint(0, screen.height() - self.pm_pet.height())

        # 移动宠物标签到新位置
        self.lb_pet.move(new_x, new_y)

        # 记录当前区域
        self.last_area = new_area

    '''
    def move_pet(self):
        screen = QDesktopWidget().screenGeometry()

        # 将屏幕分成四个区域
        width = screen.width() // 2
        height = screen.height() // 2

        areas = [(0, 0, width, height),  # 上左
                 (width, 0, width, height),  # 上右
                 (0, height, width, height),  # 下左
                 (width, height, width, height)]  # 下右

        # 随机选择一个区域，但不能是上次的区域
        available_areas = [area for area in areas if area != self.last_area]
        new_area = random.choice(available_areas)

        # 获取新的随机位置
        new_x = random.randint(new_area[0], new_area[0] + new_area[2] - self.pm_pet.width())
        new_y = random.randint(new_area[1], new_area[1] + new_area[3] - self.pm_pet.height())

        # 使用动画平滑移动宠物
        self.animation = QPropertyAnimation(self.lb_pet, b"pos")
        self.animation.setDuration(1000)  # 动画持续时间为 1 秒
        self.animation.setStartValue(self.lb_pet.pos())  # 设置动画起始位置
        self.animation.setEndValue(QPoint(new_x, new_y))  # 设置动画结束位置
        self.animation.start()  # 启动动画

        # 更新宠物当前坐标
        self.pet.rect_x = new_x
        self.pet.rect_y = new_y

        # 记录当前区域
        self.last_area = new_area
    '''

    def close_app(self):
        # 关闭窗口
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    pet = App()
    sys.exit(app.exec_())

