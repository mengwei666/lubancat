import sys
import time
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget

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
        
        self.label = QLabel("Starting...", self)
        self.label.setStyleSheet("QLabel { font-size: 48px; }")  # 设置字体大小
        self.layout.addWidget(self.label)
        
        self.update_thread = threading.Thread(target=self.update_label, daemon=True)
        self.update_thread.start()
        
        # 按 Esc 键退出全屏模式
        self.central_widget.setFocus()
        self.central_widget.keyPressEvent = self.keyPressEvent

    def keyPressEvent(self, event):
        if event.key() == 16777216:  # Qt.Key_Escape
            self.showNormal()  # 退出全屏

    def update_label(self):
        counter = 0
        while True:
            time.sleep(1)  # 每秒更新一次
            counter += 1
            self.label.setText(f"Update {counter}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FullScreenWindow()
    window.show()
    sys.exit(app.exec_())
