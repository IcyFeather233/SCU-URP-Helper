from PySide2 import QtWidgets

import sys

from win.LoginWin import LoginWin


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    login_win = LoginWin()
    login_win.ui.show()
    sys.exit(app.exec_())