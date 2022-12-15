from PySide2.QtUiTools import QUiLoader


class StartWin:
    def __init__(self, sself):
        super().__init__()
        self.ui = QUiLoader().load('./ui/start.ui')
        self.ui.table.setColumnCount(10)
        self.ui.table.setHorizontalHeaderLabels(
            ["课程编号", "课程名", "校区", "课余量", "位置", "教室", "周数", "星期", "时间", "教师"])
        self.ui.start_btn.clicked.connect(self.start)
        self.course_grabbing = sself.course_grabbing

    def start(self):
        self.course_grabbing.start(self)