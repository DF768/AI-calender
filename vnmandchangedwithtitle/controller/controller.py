from model.data_model import DataModel

class MainController:
    def __init__(self, view):
        self.view = view  # 视图引用
        self.model = DataModel()  # 模型实例
        
    def handle_send_action(self, text):
        """处理发送按钮的业务逻辑"""
        try:
            # 调用模型处理数据
            processed_data = self.model.process_text(text)
            
            # 更新视图
            self.view.update_status(f"已发送: {processed_data}")
            self.view.clear_input()
        except Exception as e:
            self.view.update_status(f"错误: {str(e)}")
    
    def handle_link_action(self):
        """处理链接按钮的业务逻辑"""
        self.view.update_status("正在打开链接...")
        self.model.open_web_link("https://www.baidu.com")