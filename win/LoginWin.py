import json

from PySide2.QtUiTools import QUiLoader

from modules.userLogin import urp_setup, urp_login
from win.MenuWin import MenuWin


class LoginWin:

    def __init__(self):
        super().__init__()
        self.ui = QUiLoader().load('./ui/login.ui')
        self.ui.btn_login.clicked.connect(self.login)
        self.readUser()
        self.ui.username.currentIndexChanged.connect(self.update_passwd)
        self.tokenval = urp_setup(self)
        self.username = ""
        self.password = ""
        self.captcha = ""

    def readUser(self):
        try:
            with open('userinfo.json', 'r') as user_file:
                user_data = json.load(user_file)
                for e_user in user_data['userList']:
                    print(e_user['username'])
                    self.ui.username.addItem(e_user["username"])
                self.ui.password.setText(user_data['userList'][0]['password'])
                user_file.close()
        except FileNotFoundError:
            print("找不到用户信息文件")

    def update_passwd(self):
        idx = self.ui.username.currenIndex()
        try:
            with open('userinfo.json', 'r') as user_file:
                user_data = json.load(user_file)
                self.ui.password.setText(user_data['userList'][idx]["password"])
                user_file.close()
        except FileNotFoundError:
            print("找不到用户信息文件")

    def login(self):
        global menu_win
        print("tokenval: " + self.tokenval)
        login_res = urp_login(self)
        if login_res != 0:
            self.tokenval = urp_setup(self)
        else:
            menu_win = MenuWin()
            menu_win.ui.show()
            self.ui.close()