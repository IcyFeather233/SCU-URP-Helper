import threading

from PySide2.QtCore import Signal, Slot, QObject
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QLabel, QMessageBox

from modules.AutoCourseGrabbing import Thread_start


class Communicate(QObject):
    top_bar = Signal(str)
    message = Signal(str)

class StartWin:
    def __init__(self, sself):
        super().__init__()
        self.th_start = None
        self.ui = QUiLoader().load('./ui/start.ui')
        self.ui.table.setColumnCount(10)
        self.ui.table.setHorizontalHeaderLabels(
            ["课程编号", "课程名", "校区", "课余量", "位置", "教室", "周数", "星期", "时间", "教师"])
        self.ui.start_btn.setEnabled(True)
        self.ui.start_btn.clicked.connect(self.start)
        self.course_grabbing = sself.course_grabbing
        self.communicate = Communicate()
        self.communicate.top_bar.connect(self.show_running_info)
        self.communicate.message.connect(self.show_messagebox)

    @Slot(str)
    def show_messagebox(self, content):
        print(content)
        QMessageBox.about(self.ui, '[提示]', content)

    @Slot(str)
    def show_running_info(self,  content):
        print(content)
        self.ui.running_info.setText(content)

    def start(self):
        self.th_start = Thread_start(self)
        self.th_start.start()
        # self.course_grabbing.start(self)