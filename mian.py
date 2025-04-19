import sys
from uiendof import CalendarWindow
from uiendof import QApplication

def main():
    

    
    # 启动GUI
    app = QApplication(sys.argv)
    window = CalendarWindow()
    window.show()
    sys.exit(app.exec_())  



if __name__ == "__main__":
    main()



