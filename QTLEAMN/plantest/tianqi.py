import sys
import requests
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QLabel, QPushButton, QTableWidget, QTableWidgetItem, 
                             QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

# 初始化SQLite数据库
def init_db():
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("school_schedule.db")
    if not db.open():
        QMessageBox.critical(None, "数据库错误", "无法连接数据库！")
        return False
    
    query = QSqlQuery()
    query.exec_("""
        CREATE TABLE IF NOT EXISTS schedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day TEXT,
            time TEXT,
            subject TEXT,
            classroom TEXT
        )
    """)
    
    # 插入示例数据（仅第一次运行时生效）
    query.exec_("SELECT COUNT(*) FROM schedule")
    query.next()
    if query.value(0) == 0:
        query.exec_("INSERT INTO schedule (day, time, subject, classroom) VALUES ('周一', '08:00', '数学', 'A203')")
        query.exec_("INSERT INTO schedule (day, time, subject, classroom) VALUES ('周一', '10:00', '物理', 'B101')")
    
    return True

# 获取天气数据（模拟API）
def get_weather():
    try:
        # 实际项目中替换为真实API（如和风天气）
        response = requests.get("https://api.example.com/weather?city=北京", timeout=3)
        data = response.json()
        return data.get("weather", "晴"), data.get("temp", "25")
    except:
        return "晴", "25"  # 模拟数据

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("智能课表提醒系统")
        self.resize(400, 300)
        
        # 主布局
        layout = QVBoxLayout()
        
        # 标题
        self.label_title = QLabel("今日课表")
        self.label_title.setAlignment(Qt.AlignCenter)
        self.label_title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(self.label_title)
        
        # 课表表格
        self.table_schedule = QTableWidget()
        self.table_schedule.setColumnCount(3)
        self.table_schedule.setHorizontalHeaderLabels(["时间", "科目", "教室"])
        layout.addWidget(self.table_schedule)
        
        # 天气提醒按钮
        self.btn_weather = QPushButton("获取天气提醒")
        self.btn_weather.clicked.connect(self.show_weather_alert)
        layout.addWidget(self.btn_weather)
        
        # 加载数据
        self.load_schedule()
        
        # 设置中心部件
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
    
    def load_schedule(self):
        query = QSqlQuery("SELECT time, subject, classroom FROM schedule WHERE day='周一'")
        self.table_schedule.setRowCount(0)
        
        row = 0
        while query.next():
            self.table_schedule.insertRow(row)
            for col in range(3):
                self.table_schedule.setItem(row, col, QTableWidgetItem(query.value(col)))
            row += 1
    
    def show_weather_alert(self):
        weather, temp = get_weather()
        advice = ""
        if "雨" in weather:
            advice = "建议带伞！"
        elif int(temp) > 30:
            advice = "注意防晒！"
        
        QMessageBox.information(
            self, 
            "天气提醒", 
            f"当前天气：{weather}，温度：{temp}℃\n{advice}"
        )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    if not init_db():
        sys.exit(1)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())