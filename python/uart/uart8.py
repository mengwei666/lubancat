import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PIL import Image

class FullScreenWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('互创联合-ANT200')
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

    def add_icon_to_image(target_image_path, icon_image_path, output_image_path, x_offset=100):
    # 打开目标图片和图标图片
    target_image = Image.open(target_image_path)
    icon_image = Image.open(icon_image_path)

    # 计算图标的位置
    target_width, target_height = target_image.size
    icon_width, icon_height = icon_image.size
    x_position = (target_width - icon_width) // 2 - x_offset  # 中间位置向左偏移x_offset像素
    y_position = (target_height - icon_height) // 2

    # 将图标粘贴到目标图片上
    target_image.paste(icon_image, (x_position, y_position), icon_image)

    # 保存合并后的图片
    target_image.save(output_image_path)

if __name__ == '__main__':

    # 添加图标到目标图片上
    add_icon_to_image('png/03-核对正常.png', '/mnt/data/normal-标签.png', 'png/03-核对正常_with_icon.png')

    app = QApplication(sys.argv)
    window = FullScreenWindow()
    window.show()
    sys.exit(app.exec_())
