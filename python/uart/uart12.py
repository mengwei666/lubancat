import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QRect, Qt

class ImageWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置窗口的尺寸
        self.setWindowTitle('显示 PNG 图片')

        # 创建一个 QWidget 作为中央小部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 创建一个容器 QWidget
        self.container = QWidget(self.central_widget)

        # 设置容器的背景颜色为红色
        self.container.setStyleSheet("background-color: red;")

        # 创建一个 QVBoxLayout 布局管理器
        self.layout = QVBoxLayout()
        self.container.setLayout(self.layout)

        # 创建一个 QLabel 控件
        self.image_label = QLabel(self.container)
        self.image_label.setStyleSheet("background-color: green;")
        
        # 加载并设置图片
        self.pixmap = QPixmap('png/01-初始化界面.png')
        self.image_label.setPixmap(self.pixmap)
        
        # 将 QLabel 添加到容器中
        self.layout.addWidget(self.image_label)

    def keyPressEvent(self, event):
        # 检测 Ctrl + C 组合键
        if event.key() == Qt.Key_C and event.modifiers() & Qt.ControlModifier:
            QApplication.quit()  # 退出程序

    def resizeEvent(self, event):
        # 获取当前窗口尺寸
        size = self.size()  
        # 设置容器的尺寸为当前窗口尺寸
        self.container.setGeometry(QRect(0, 0, size.width(), size.height()))
        print(f"container: 宽={size.width()} 高={size.height()}")
        




        # 设置 QLabel 的位置和大小
        self.image_label.setGeometry(QRect(0, 0, size.width(), 240))




        # 确保图片填充 QLabel 的大小
        scaled_pixmap = self.pixmap.scaled(size.width(), 240, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        # self.image_label.setPixmap(scaled_pixmap)


        super().resizeEvent(event)  # 保持父类行为

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageWindow()
    window.showFullScreen()  # 全屏显示
    sys.exit(app.exec_())
