import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap, QPainter, QFont, QFontMetrics
from PyQt5.QtCore import Qt

class ImageWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置窗口的标题
        self.setWindowTitle('显示 PNG 图片')

        # 加载图片和图标
        self.pixmap = QPixmap('png/03-核对正常.png')
        self.icon = QPixmap('png/normal-标签.png')  # 确保路径正确

        # 图标和文字的显示状态
        self.icon_visible = True
        self.text_visible = True

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

        if self.icon_visible:
            # 计算图标的缩放比例
            icon_width = self.icon.width()
            icon_height = self.icon.height()

            # 计算图标的新尺寸
            icon_new_width = new_width * (icon_width / pixmap_width)
            icon_new_height = new_height * (icon_height / pixmap_height)

            # 计算图标的位置，使其居中
            icon_x = (new_width - icon_new_width) / 2
            icon_y = (new_height - icon_new_height) / 2

            # 绘制缩放后的图标
            painter.drawPixmap(icon_x - 500, icon_y + 100, icon_new_width, icon_new_height, self.icon)

            # 设置字体和字体大小
            font_size = icon_new_height / 10  # 根据图标高度设置字体大小
            font = QFont('Arial', font_size)
            painter.setFont(font)

            # 计算文字尺寸
            text = '识别成功一个标签'
            metrics = QFontMetrics(font)
            text_width = metrics.width(text)
            text_height = metrics.height()

            # 计算文字位置，使其在图标上方居中
            text_x = (new_width - text_width) / 2
            text_y = icon_y - text_height - 10  # 图标上方留出一点距离

            # 绘制文字
            painter.drawText(text_x, text_y+50, text)


            # 计算第二行文字的尺寸和位置
            text2 = 'E1B2C4667123'
            text2_width = metrics.width(text2)
            text2_height = metrics.height()

            # 计算文字位置，使其在图标下方居中
            text2_x = (new_width - text2_width) / 2
            text2_y = icon_y + icon_new_height + text2_height + 10  # 图标下方留出一点距离

            # 绘制第二行文字
            painter.drawText(text2_x-500, text2_y+80, text2)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()  # 按下 Escape 键关闭窗口
        elif event.key() == Qt.Key_W:
            self.icon_visible = not self.icon_visible  # 切换图标的显示状态
            self.text_visible = not self.text_visible  # 切换文字的显示状态
            self.update()  # 更新窗口以重新绘制内容

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageWindow()
    sys.exit(app.exec_())
