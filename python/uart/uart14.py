import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt

class ImageWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置窗口的标题
        self.setWindowTitle('显示 PNG 图片')

        # 加载图片
        self.pixmap = QPixmap('png/01-初始化界面.png')

        # 设置窗口的尺寸为全屏
        self.showFullScreen()

    def paintEvent(self, event):
        # 获取窗口的尺寸
        window_width = self.width()
        window_height = self.height()

        # 获取图片的原始尺寸
        pixmap_width = self.pixmap.width()
        pixmap_height = self.pixmap.height()
        print("window_width window_height pixmap_width pixmap_height", window_width, window_height, pixmap_width, pixmap_height)

        # 计算宽高比
        pixmap_ratio = pixmap_width / pixmap_height

        # 窗口宽高比大于图片宽高比，宽度充满，高度自适应
        new_width = window_width
        new_height = new_width / pixmap_ratio
        print("pixmap_ratio new_width new_height", pixmap_ratio, new_width, new_height)


        # 使用 QPainter 绘制缩放后的图片
        painter = QPainter(self)
        painter.drawPixmap(0, 0, new_width, new_height, self.pixmap)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()  # 按下 Escape 键关闭窗口

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageWindow()
    sys.exit(app.exec_())
