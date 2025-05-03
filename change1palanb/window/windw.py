from PyQt5.QtWidgets import (
    QMainWindow, QCalendarWidget, QListWidget, 
    QTextEdit, QLineEdit, QPushButton, 
    QSplitter, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QListWidgetItem
)
from PyQt5.QtCore import Qt, QTime, QDateTime
from PyQt5.QtGui import QIcon
from typing import Dict

from ..aimodels.ai import AIClient
from ..aimodels.date import Calendar as date
from ..logged import og

class CalendarWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ai = AIClient()
        self.db = date()
        self._init_ui()
        self._setup_connections()
        
    def _init_ui(self) -> None:
        """初始化UI界面"""
        self.setWindowTitle("Deepseek日历")
        self.setWindowIcon(QIcon("assets/calendar.png"))
        self.resize(1200, 800)

        # 主部件
        self.calendar = QCalendarWidget()
        self.event_list = QListWidget()
        self.chat_area = QTextEdit()
        self.input_field = QLineEdit()
        self.send_btn = QPushButton("发送")
        
        # 设置UI属性
        self.chat_area.setReadOnly(True)
        self.event_list.setSpacing(5)
        
        # 布局
        main_splitter = QSplitter(Qt.Vertical)
        
        # 顶部布局
        top_splitter = QSplitter(Qt.Horizontal)
        top_splitter.addWidget(self.calendar)
        top_splitter.addWidget(self.event_list)
        
        # 底部布局
        bottom_widget = QWidget()
        chat_layout = QVBoxLayout()
        input_layout = QHBoxLayout()
        
        chat_layout.addWidget(self.chat_area)
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_btn)
        chat_layout.addLayout(input_layout)
        bottom_widget.setLayout(chat_layout)
        
        main_splitter.addWidget(top_splitter)
        main_splitter.addWidget(bottom_widget)
        
        self.setCentralWidget(main_splitter)
        
    def _setup_connections(self) -> None:
        """设置信号槽连接"""
        self.send_btn.clicked.connect(self._handle_ai_input)
        self.input_field.returnPressed.connect(self._handle_ai_input)
        self.calendar.selectionChanged.connect(self._update_events)
        
    def _handle_ai_input(self) -> None:
        """处理用户输入"""
        user_input = self.input_field.text().strip()
        if not user_input:
            return
            
        self._append_message("用户", user_input)
        self.input_field.clear()
        
        response = self.ai.generate_plan(user_input, self.calendar.selectedDate())
        
        if response:
            self.db.add_event(response)
            self._append_message("系统", f"已添加：{response['title']}")
            event_date = QDateTime.fromString(response["start"], "yyyy-MM-dd HH:mm:ss").date()
            self.calendar.setSelectedDate(event_date)
            self._update_events()
        else:
            self._append_message("系统", "添加失败，请尝试不同的表达方式（例：'明天下午三点开会'）")
        
    def _update_events(self) -> None:
        """更新事件列表"""
        selected_date = self.calendar.selectedDate()
        events = self.db.get_events(selected_date)
        self.event_list.clear()
        
        for event in events:
            item = QListWidgetItem()
            widget = self._create_event_widget(event)
            item.setSizeHint(widget.sizeHint())
            self.event_list.addItem(item)
            self.event_list.setItemWidget(item, widget)
            
    def _create_event_widget(self, event: Dict) -> QWidget:
        """创建事件显示部件"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        start = QDateTime.fromString(event["start"], "yyyy-MM-dd HH:mm:ss")
        end = QDateTime.fromString(event["end"], "yyyy-MM-dd HH:mm:ss")
        
        time_str = (
            "⏳ 全天" 
            if start.time() == QTime(0, 0) and end.time() == QTime(23, 59)
            else f"🕒 {start.toString('HH:mm')} - {end.toString('HH:mm')}"
        )
        
        title = QLabel(f"💡 {event['title']}")
        time = QLabel(time_str)
        
        title.setStyleSheet("font-weight: bold; color: #2c3e50;")
        time.setStyleSheet("color: #7f8c8d;")
        
        layout.addWidget(title)
        layout.addWidget(time)
        widget.setLayout(layout)
        
        return widget
        
    def _append_message(self, sender: str, message: str) -> None:
        """添加消息到聊天区域"""
        self.chat_area.append(f"<b>{sender}:</b> {message}")
        self.chat_area.verticalScrollBar().setValue(
            self.chat_area.verticalScrollBar().maximum()
        )