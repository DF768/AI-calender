import sqlite3
from datetime import datetime

class CalendarDB:
    
    def __init__(self, db_path="calendar.db"):
        self.conn = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS events
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              title TEXT NOT NULL,
              start DATETIME NOT NULL,
              end DATETIME NOT NULL,
              description TEXT,
              location TEXT,
              tags TEXT)''')

    def add_event(self, event_data):
        query = '''INSERT INTO events 
                   (title, start, end, description, location, tags)
                   VALUES (?, ?, ?, ?, ?, ?)'''
        self.conn.execute(query, (
            event_data['title'],
            event_data['start'],
            event_data['end'],
            event_data.get('description', ''),
            event_data.get('location', ''),
            ','.join(event_data.get('tags', []))
        ))
        self.conn.commit()

        def get_events(self, date=None):

            try:
                if date:
                    # 如果传入的是QDate对象，转换为字符串
                    if hasattr(date, "toString"):
                        date_str = date.toString("yyyy-MM-dd")
                    else:
                        date_str = date
                    
                    query = '''SELECT * FROM events 
                            WHERE DATE(start) = ? 
                            ORDER BY start'''
                    cursor = self.conn.execute(query, (date_str,))
                else:
                    query = '''SELECT * FROM events 
                            ORDER BY start'''
                    cursor = self.conn.execute(query)
                
                # 将查询结果转换为字典列表
                events = []
                for row in cursor.fetchall():
                    event = dict(row)
                    event['tags'] = event['tags'].split(',') if event['tags'] else []
                    events.append(event)
                
                return events
            except Exception as e:
                print(f"查询事件失败: {str(e)}")
                return []