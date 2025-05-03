import sys
from PyQt5.QtWidgets import QApplication

from calendar_app.views.main_window import CalendarWindow

def main():
    # 创建应用实例
    app = QApplication(sys.argv)
    
    # 设置应用样式
    app.setStyle("Fusion")
    
    # 创建主窗口
    window = CalendarWindow()
    window.show()
    
    # 执行应用
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()