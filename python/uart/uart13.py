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
        # 使用 QPainter 绘制图片
        painter = QPainter(self)
        painter.drawPixmap(300, 400, self.pixmap)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()  # 按下 Escape 键关闭窗口

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageWindow()
    sys.exit(app.exec_())
