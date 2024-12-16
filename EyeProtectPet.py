from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import random
import time

# 宠物类
class Pet(object):
    def __init__(self, width=400, height=400):
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

# 应用程序类
class App(QWidget):
    def __init__(self):
        super(App, self).__init__()

        self.pet = Pet()
        self.pm_pet = QPixmap(self.pet.image)
        self.lb_pet = QLabel(self)

        self.init_ui()

        # 0.1秒更新图片实现gif效果
        self.gif_timer = QTimer(self)
        self.gif_timer.timeout.connect(self.gem)
        self.gif_timer.start(100)

        # 创建定时器，调用move_pet方法
        self.move_timer = QTimer(self)
        self.move_timer.timeout.connect(self.move_pet)
        self.move_timer.start((self.pet.image_num + 1) * 100)

        # 10秒后关闭窗口
        self.close_timer = QTimer(self)
        self.close_timer.timeout.connect(self.close_app)
        self.close_timer.setSingleShot(True)
        self.close_timer.start((self.pet.image_num + 1) * 100 * 2)

    def gem(self):
        self.pet.gif()
        self.pm_pet = QPixmap(self.pet.image)
        self.lb_pet.setPixmap(self.pm_pet)

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

        self.last_area = None

    def move_pet(self):
        screen = QDesktopWidget().screenGeometry()
        width = screen.width() // 2
        height = screen.height() // 2
        areas = [(0, 0, width, height), (width, 0, width, height), (0, height, width, height), (width, height, width, height)]
        available_areas = [area for area in areas if area != self.last_area]
        new_area = random.choice(available_areas)

        new_x = random.randint(new_area[0], new_area[0] + new_area[2] - self.pm_pet.width())
        new_y = random.randint(new_area[1], new_area[1] + new_area[3] - self.pm_pet.height())

        self.lb_pet.move(new_x, new_y)
        self.last_area = new_area

    def close_app(self):
        self.close()

def sleep_loop(total_time: int):
    time.sleep(total_time)

def main():
    app = QApplication(sys.argv)  # 创建 QApplication 实例
    while True:
        sleep_loop(1 * 5)  # 每 x 分钟休息一次
        pet = App()
        app.exec_()  # 执行事件循环

if __name__ == '__main__':
    main()
