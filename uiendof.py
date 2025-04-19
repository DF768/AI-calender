#此文件为最终的第一个版本

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from openai import OpenAI


class AIClient:
    def __init__(self):
        self.client = OpenAI(
            base_url="https://api.deepseek.com/v1",# 本地部署请使用 http://127.0.0.1:11434/v1 在线部署请使用"https://api.deepseek.com/v1"
            #base_url="http://127.0.0.1:11434/v1",
            api_key="sk-0b69e753d8da4628989dd0d75a23c57e"  # DeepSeek API Key  sk-0b69e753d8da4628989dd0d75a23c57e ，如果为本地部署则为"a"
            #api_key="a"
        )
        self.model = "deepseek-chat" #如果使用在线api请使用"deepseek-chat"模型。本地部署请使用"deepseek-r1:模型规模，建议模型规模大于8b，才支持超长文本解析"

    def generate_plan(self, user_input, selected_date):
        try:
            time_data = selected_date.toString("yyyy-MM-dd")
            system_input = f"""当前日期是{time_data}，用户将输入包含时间和事件的描述，你需要：
1. 识别所有时间相关表达（绝对时间、相对时间和周期时间）
2. 自动转换时间为具体日期和时间（格式：YYYY-MM-DD HH:mm）
3. 按以下JSON格式返回结果：
{{
    "title": "事件标题",
    "date": "计算后的日期（YYYY-MM-DD）",
    "time": "具体时间（HH:mm或全天）",
    "duration": 默认1小时（单位：分钟）
}}

示例：
用户输入：明天下午三点和团队开会
响应：{{"title": "团队会议", "date": "2024-03-21", "time": "15:00", "duration": 60}}

用户输入：每周五下午团队建设
响应：{{"title": "团队建设", "date": "2024-03-22", "time": "14:00", "duration": 60}}"""

            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_input},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.3,
                max_tokens=512,
                top_p=0.9,
                response_format={"type": "json_object"}
            )

            response_text = completion.choices[0].message.content
            return self.parse_response(response_text, selected_date)
        except Exception as e:
            print(f"API Error: {e}")
            return None

    def parse_response(self, response_text, base_date):
        try:
            import json
            data = json.loads(response_text)
            
            # 解析日期
            event_date = QDate.fromString(data["date"], "yyyy-MM-dd")
            if not event_date.isValid():
                return None

            # 处理时间
            if data["time"] == "全天":
                start_time = QTime(0, 0)
                end_time = QTime(23, 59)
            else:
                start_time = QTime.fromString(data["time"], "HH:mm")
                if not start_time.isValid():
                    return None
                duration = data.get("duration", 60)
                end_time = start_time.addSecs(duration * 60)

            return {
                "title": data["title"],
                "start": QDateTime(event_date, start_time).toString("yyyy-MM-dd HH:mm:ss"),
                "end": QDateTime(event_date, end_time).toString("yyyy-MM-dd HH:mm:ss")
            }
        except Exception as e:
            print(f"解析失败: {e}")
            return None

class Calendar:
    def __init__(self):
        self.events = []
        
    def add_event(self, event):
        self.events.append(event)
        
    def get_events(self, date):
        return [e for e in self.events if QDateTime.fromString(
            e["start"], "yyyy-MM-dd HH:mm:ss").date() == date]

class CalendarWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ai = AIClient()
        self.db = Calendar()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Deepseek日历")
        self.resize(1200, 800)

        # 日历部件
        self.calendar = QCalendarWidget()
        self.event_list = QListWidget()
    
        # AI聊天部件
        self.chatarea = QTextEdit()
        self.chatarea.setReadOnly(True)
        self.input_field = QLineEdit()
        self.send_btn = QPushButton("发送")
    
        # 布局
        splitter = QSplitter(Qt.Vertical)
        top1split = QSplitter(Qt.Horizontal)
        top1split.addWidget(self.calendar)  # 将日历部件添加ui

        top1split.addWidget(self.event_list)  # 将事件列表部件添加到右边
    
        bottom_split = QWidget()
        chat_layout = QVBoxLayout()
        chat_layout.addWidget(self.chatarea)  # 将聊天区域添加到下面
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_field)  # 将输入框添加到输入
        input_layout.addWidget(self.send_btn)  # 将发送按钮添加到输入右侧
        chat_layout.addLayout(input_layout)  # 将输入布局添加到聊天框
        bottom_split.setLayout(chat_layout)  # 设置底部分割线
    
        splitter.addWidget(top1split)  # 将顶部分割器添加到ui
        splitter.addWidget(bottom_split)  # 将底部分割器添加到ui
    
        self.setCentralWidget(splitter)  # 设置ui页面的分割
    
        # 连接api
        self.send_btn.clicked.connect(self.handle_ai_input)  # 发送按钮的点击到处理AI输入
        self.calendar.selectionChanged.connect(self.update_events)  # 连接日历日期变化的响应到更新
        
    def handle_ai_input(self):
        user_input = self.input_field.text()
        if not user_input:
            return
            
        self.chatarea.append(f"用户: {user_input}")
        self.input_field.clear()
        
        response = self.ai.generate_plan(user_input, self.calendar.selectedDate())
        
        if response:
            self.db.add_event(response)
            self.chatarea.append(f"Deepseek: 已添加：{response['title']}")
            event_date = QDateTime.fromString(response["start"], "yyyy-MM-dd HH:mm:ss").date()
            self.calendar.setSelectedDate(event_date)
            self.update_events()
        else:
            self.chatarea.append("Deepseek: 添加失败，请尝试不同的表达方式（例：'明天下午三点开会'）")
        
    def update_events(self):
        selected_date = self.calendar.selectedDate()
        events = self.db.get_events(selected_date)
        self.event_list.clear()
        
        for event in events:
            start = QDateTime.fromString(event["start"], "yyyy-MM-dd HH:mm:ss")
            end = QDateTime.fromString(event["end"], "yyyy-MM-dd HH:mm:ss")
            
            item = QListWidgetItem()
            widget = QWidget()
            layout = QVBoxLayout()
            
            time_str = ""
            if start.time() == QTime(0,0) and end.time() == QTime(23,59):
                time_str = "⏳ 全天"
            else:
                time_str = f"🕒 {start.toString('HH:mm')} - {end.toString('HH:mm')}"
                
            title = QLabel(f"💡 {event['title']}")
            time = QLabel(time_str)
            
            title.setStyleSheet("font-weight: bold; color: #2c3e50;")
            time.setStyleSheet("color: #7f8c8d;")
            
            layout.addWidget(title)
            layout.addWidget(time)
            widget.setLayout(layout)
            
            item.setSizeHint(widget.sizeHint())
            self.event_list.addItem(item)
            self.event_list.setItemWidget(item, widget)
'''

#测试生成
if __name__ == "__main__":
    app = QApplication([])
    window = CalendarWindow()
    window.show()
    app.exec_()
    
'''
#启动ui
def main():
    app = QApplication(sys.argv)
    window = CalendarWindow()
    window.show()
    sys.exit(app.exec_())  

if __name__ == "__main__":
    main()


