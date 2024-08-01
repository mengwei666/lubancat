import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt, QRect

class ImageWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置窗口的标题
        self.setWindowTitle('显示 PNG 图片')

        # 加载图片和图标
        self.pixmap = QPixmap('png/01-初始化界面.png')
        self.icon = QPixmap('png/normal-标签.png')  # 确保路径正确

        # 图标的显示状态
        self.icon_visible = True

        # 设置窗口的尺寸为全屏
        self.showFullScreen()

    def paintEvent(self, event):
        # 获取窗口的尺寸
        window_width = self.width()
        window_height = self.height()

        # 获取图片的原始尺寸
        pixmap_width = self.pixmap.width()
        pixmap_height = self.pixmap.height()

        # 计算宽高比
        pixmap_ratio = pixmap_width / pixmap_height

        # 窗口宽高比大于图片宽高比，宽度充满，高度自适应
        new_width = window_width
        new_height = new_width / pixmap_ratio

        # 使用 QPainter 绘制缩放后的图片
        painter = QPainter(self)
        painter.drawPixmap(0, 0, new_width, new_height, self.pixmap)

        # 计算图标位置并绘制图标
        if self.icon_visible:
            icon_width = self.icon.width()
            icon_height = self.icon.height()
            icon_x = (new_width - icon_width) / 2
            icon_y = (new_height - icon_height) / 2
            painter.drawPixmap(icon_x, icon_y, self.icon)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()  # 按下 Escape 键关闭窗口
        elif event.key() == Qt.Key_W:
            self.icon_visible = not self.icon_visible  # 切换图标的显示状态
            self.update()  # 更新窗口以重新绘制内容

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageWindow()
    sys.exit(app.exec_())
