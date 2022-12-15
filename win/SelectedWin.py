from PySide2.QtUiTools import QUiLoader



class SelectedWin:
    def __init__(self, sself):
        super().__init__()
        self.ui = QUiLoader().load('./ui/selected.ui')
        self.ui.table.setColumnCount(8)
        self.ui.table.setHorizontalHeaderLabels(["课程号", "属性", "方式", "教师", "周数", "星期", "时间", "课程"])
        self.ui.delete_btn.clicked.connect(self.delete)
        self.course_grabbing = sself.course_grabbing
        self.course_grabbing.selectRes(self)

    def delete(self):
        self.course_grabbing.delete(self)

