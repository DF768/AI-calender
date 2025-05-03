import sys
from PyQt5.QtWidgets import QApplication
from view.main_winodws import MainWindow
from controller.controller import MainController

def main():
    app = QApplication(sys.argv)
    
    # 创建控制器和视图
    controller = MainController(None)  # 先创建控制器
    window = MainWindow(controller)    # 创建视图并注入控制器
    controller.view = window           # 将视图注入控制器
    
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()