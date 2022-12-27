from PySide2.QtUiTools import QUiLoader

from modules.AutoCourseGrabbing import AutoCourseGrabbing
from win.AddWin import AddWin
from win.SelectedWin import SelectedWin
from win.StartWin import StartWin


class MenuWin:
    def __init__(self):
        super().__init__()
        self.ui = QUiLoader().load('./ui/menu.ui')
        self.ui.add_btn.clicked.connect(self.go_add)
        self.ui.query_btn.clicked.connect(self.go_selected)
        self.ui.start_btn.clicked.connect(self.go_start)
        self.course_grabbing = AutoCourseGrabbing()


    def go_selected(self):
        """
        已选课程
        :return:
        """
        global se_win
        se_win = SelectedWin(self)
        se_win.ui.show()


    def go_add(self):
        """
        添加课程
        :return:
        """
        global add_win
        add_win = AddWin(self)
        add_win.ui.show()

    def go_start(self):
        """
        开始抢课
        :return:
        """
        global start_win
        start_win = StartWin(self)
        start_win.ui.show()
