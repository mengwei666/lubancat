import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class FullScreenWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Full Screen PyQt5 Window')
        self.showFullScreen()  # 全屏显示

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout(self.central_widget)
        
        self.label = QLabel(self)
        self.label.setStyleSheet("QLabel { font-size: 48px; }")  # 设置字体大小
        self.layout.addWidget(self.label)
        
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_label)
        
        self.current_image = 'png/01-初始化界面.png'  # 初始图片路径
        self.load_image(self.current_image)  # 加载并显示初始图片
        
        # 按 Esc 键退出全屏模式
        self.central_widget.setFocus()
        self.central_widget.keyPressEvent = self.keyPressEvent

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.showNormal()  # 退出全屏
        elif event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_C:
            QApplication.quit()  # 退出程序
        else:
            super().keyPressEvent(event)

    def load_image(self, path):
        self.pixmap = QPixmap(path)
        self.update_image_display()

    def update_image_display(self):
        # 获取屏幕的可用几何区域
        screen_geom = QApplication.primaryScreen().availableGeometry()
        screen_size = screen_geom.size()

        # 缩放图片以适应屏幕
        self.scaled_pixmap = self.pixmap.scaled(screen_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        # 直接将缩放后的图片设置为 QLabel 的 pixmap
        self.image_label.setPixmap(self.scaled_pixmap)
        self.image_label.setGeometry(0, 0, screen_size.width(), screen_size.height())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            screen_size = QApplication.primaryScreen().size()
            if event.pos().x() > screen_size.width() / 2:
                # 点击了屏幕右半部分
                self.current_image = 'png/03-核对正常.png'
            else:
                # 点击了屏幕左半部分
                self.current_image = 'png/01-初始化界面.png'
            
            self.load_image(self.current_image)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FullScreenWindow()
    window.show()
    sys.exit(app.exec_())
