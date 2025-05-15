import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QTextEdit

class GreenTravelApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口标题和大小
        self.setWindowTitle('绿色出行小助手')
        self.setGeometry(100, 100, 400, 300)

        # 创建布局
        layout = QVBoxLayout()

        # 出发地和目的地输入
        layout.addWidget(QLabel("出发地:"))
        self.start_location = QLineEdit()
        layout.addWidget(self.start_location)
        layout.addWidget(QLabel("目的地:"))
        self.end_location = QLineEdit()
        layout.addWidget(self.end_location)

        # 选择出行方式
        layout.addWidget(QLabel("选择出行方式:"))
        self.travel_mode = QComboBox()
        self.travel_mode.addItem("步行")
        self.travel_mode.addItem("骑行")
        self.travel_mode.addItem("公交")
        self.travel_mode.addItem("地铁")
        self.travel_mode.addItem("自家")
        layout.addWidget(self.travel_mode)

        # 计算按钮
        self.calc_button = QPushButton("计算出行规划和碳足迹")
        self.calc_button.clicked.connect(self.calculate_travel)
        layout.addWidget(self.calc_button)

        # 显示结果
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_text)

        # 设置布局
        self.setLayout(layout)

    def calculate_travel(self):
        start = self.start_location.text()
        end = self.end_location.text()
        mode = self.travel_mode.currentText()

        # 简化计算逻辑：假设距离为10公里，根据出行方式估算时间和碳足迹
        distance = 10  # 千米
        if mode == "步行":
            time = "1.5小时"
            carbon_footprint = "0公斤"
        elif mode == "骑行":
            time = "0.5小时"
            carbon_footprint = "0.1公斤"
        elif mode == "公交":
            time = "0.3小时"
            carbon_footprint = "0.4公斤"
        elif mode == "地铁":
            time = "0.2小时"
            carbon_footprint = "0.3公斤"
        else:
            time = "未知"
            carbon_footprint = "未知"

        # 显示结果
        self.result_text.setText(f"从{start}到{end}，选择{mode}出行方式：\n"
                                 f"预计时间：{time}\n"
                                 f"碳足迹：{carbon_footprint}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = GreenTravelApp()
    ex.show()
    sys.exit(app.exec_())