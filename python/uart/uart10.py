import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QRect

class ImageWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置窗口的尺寸
        self.setWindowTitle('显示 PNG 图片')
        self.setGeometry(0, 0, 1848, 1053)

        # 创建一个 QWidget 作为中央小部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 创建一个 QLabel 控件
        self.image_label = QLabel(central_widget)
        
        # 加载并设置图片
        pixmap = QPixmap('png/01-初始化界面.png')
        self.image_label.setPixmap(pixmap)
        
        # 设置 QLabel 的位置和尺寸
        self.image_label.setGeometry(QRect(300, 500, 960, 240))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageWindow()
    window.show()
    sys.exit(app.exec_())
