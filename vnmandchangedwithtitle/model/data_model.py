import webbrowser

class DataModel:
    def process_text(self, text):
        """业务逻辑：处理文本"""
        if not text:
            raise ValueError("输入不能为空")
        
        # 这里可以添加各种业务规则
        if len(text) > 100:
            raise ValueError("输入过长")
            
        return text.upper()  # 示例处理
    
    def open_web_link(self, url):
        """业务逻辑：打开网页"""
        webbrowser.open(url)