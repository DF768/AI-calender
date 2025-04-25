from typing import List, Dict
from PyQt5.QtCore import QDate, QDateTime  # 导入 QDateTime

class Calendar:
    def __init__(self):
        self.events: List[Dict] = []
        
    def add_event(self, event: Dict) -> None:
        """添加新事件"""
        self.events.append(event)
        
    def get_events(self, date: QDate) -> List[Dict]:
        """获取指定日期的事件"""
        return [
            e for e in self.events 
            if QDateTime.fromString(e["start"], "yyyy-MM-dd HH:mm:ss").date() == date
        ]
        
    def remove_event(self, event_id: str) -> bool:
        """删除事件"""
        # 待实现
        pass