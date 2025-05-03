from PyQt5.QtWidgets import QMainWindow
from view.main_winodws import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller  # 注入控制器
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # 连接信号槽
        self._connect_signals()
    
    def _connect_signals(self):
        """连接所有UI信号到控制器方法"""
        self.ui.pushButton.clicked.connect(self._on_send_button_click)
        self.ui.commandLinkButton.clicked.connect(self._on_link_button_click)
        # 连接其他信号...
    
    def _on_send_button_click(self):
        """处理发送按钮点击事件"""
        text = self.ui.lineEdit.text()
        self.controller.handle_send_action(text)
    
    def _on_link_button_click(self):
        """处理链接按钮点击事件"""
        self.controller.handle_link_action()
    
    # 其他UI更新方法
    def update_status(self, message):
        """更新状态栏"""
        self.ui.statusbar.showMessage(message)
    
    def clear_input(self):
        """清空输入框"""
        self.ui.lineEdit.clear()