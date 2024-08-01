import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class FullScreenWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('互创联合-ANT200')
        self.showFullScreen()  # 全屏显示

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        
        # 创建标签用于显示文本
        self.label = QLabel(self)
        self.label.setStyleSheet("QLabel { font-size: 48px; }")  # 设置字体大小
        self.label.setText("这是一个示例标签")
        self.label.setGeometry(50, 50, 400, 100)  # 使用绝对位置设置大小和位置
        
        # 创建标签用于显示图片
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        # 初始化图片路径
        self.current_image = 'png/01-初始化界面.png'
        
        # 加载图标
        self.icon_label = QLabel(self)
        self.icon_pixmap = QPixmap('png/normal-标签.png')
        self.icon_label.setPixmap(self.icon_pixmap)
        self.icon_label.setVisible(False)  # 初始状态为隐藏
        
        # 加载图片并显示
        self.load_image(self.current_image)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.showNormal()  # 退出全屏
        elif event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_C:
            QApplication.quit()  # 退出程序
        elif event.key() == Qt.Key_W:
            self.toggle_icon_visibility()  # 切换图标可见性
        else:
            super().keyPressEvent(event)

    def load_image(self, path):
        self.pixmap = QPixmap(path)
        if self.pixmap.isNull():
            print(f"Failed to load image from path: {path}")
        else:
            self.update_image_display()

    def update_image_display(self):
        # 获取屏幕的可用几何区域
        screen_geom = QApplication.primaryScreen().availableGeometry()
        screen_size = screen_geom.size()
        print("screen_size", screen_size)

        # 缩放图片以适应屏幕
        self.scaled_pixmap = self.pixmap.scaled(screen_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        # 计算图片的实际尺寸
        pixmap_size = self.scaled_pixmap.size()
        
        # 设置图片显示的位置，确保图片底部对齐屏幕底部
        x_position = (screen_size.width() - pixmap_size.width()) // 2
        y_position = screen_size.height() - pixmap_size.height()
        
        # 设置 QLabel 的几何区域
        self.image_label.setGeometry(x_position, y_position, pixmap_size.width(), pixmap_size.height())
        self.image_label.setPixmap(self.scaled_pixmap)

        print(f"Image position: x={x_position}, y={y_position}, width={pixmap_size.width()}, height={pixmap_size.height()}")

        # 更新图标位置
        icon_width = self.icon_pixmap.width()
        icon_height = self.icon_pixmap.height()
        x_position_icon = (screen_size.width() - icon_width) // 2
        y_position_icon = (screen_size.height() - icon_height) // 2
        self.icon_label.setGeometry(x_position_icon, y_position_icon, icon_width, icon_height)

        print(f"Icon position: x={x_position_icon}, y={y_position_icon}, width={icon_width}, height={icon_height}")

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
            
    def toggle_icon_visibility(self):
        self.icon_label.setVisible(not self.icon_label.isVisible())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FullScreenWindow()
    window.show()
    sys.exit(app.exec_())
