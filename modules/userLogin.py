import hashlib
import json
import hashlib

from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QMessageBox

from modules.utils import *

http_url_login = "http://zhjw.scu.edu.cn/j_spring_security_check"
http_url_captcha = "http://zhjw.scu.edu.cn/img/captcha.jpg"

def urp_setup(sself):
    """
    刚刚访问，还没登录
    """
    try:
        http_page = http_main.get(http_url_init)
        token_value = http_page.text.find("tokenValue")
        if token_value > 0:
            token_value = http_page.text[token_value + 37: token_value + 69]
            print("[随机码获取]：", token_value)
        else:
            print("随机token获取错误")
            QMessageBox.about(sself.ui, '[错误]', '随机token获取错误')
        print("获取验证码")
        http_captcha = http_main.get(http_url_captcha)
    except requests.exceptions.ConnectionError:
        print("网络错误")
        QMessageBox.about(sself.ui, '[错误]', '网络错误')
    with open('captcha.jpg', 'wb') as http_capfile:
        http_capfile.write(http_captcha.content)
        http_capfile.close()
    pixmap = QPixmap('captcha.jpg')
    sself.ui.captcha_pic.setPixmap(pixmap)
    print("验证码显示成功")
    return token_value

def urp_login(sself):
    username = sself.ui.username.currentText()
    password = sself.ui.password.text()
    captcha = sself.ui.captcha.text()

    http_hash = hashlib.md5(password.encode()).hexdigest()
    post_data = {
        "tokenValue": sself.tokenval,
        "j_username": username,
        "j_password": http_hash,
        "j_captcha": captcha}
    try:
        http_post = http_main.post(http_url_login, post_data, http_head)
    except:
        print("网络错误")
        QMessageBox.about(sself.ui, '[错误]', '网络错误')
    # QMessageBox.about(sself.ui, '提示', '我是内容')
    if http_post.text.find('验证码错误') != -1:
        print("[登录未成功]：验证码不正确")
        QMessageBox.about(sself.ui, '[登录未成功]', '验证码不正确')
        return -1
    elif http_post.text.find('token校验失败') != -1:
        print("[登录未成功]：token校验失败")
        QMessageBox.about(sself.ui, '[登录未成功]', 'token校验失败')
        return -1
    elif http_post.text.find('的培养方案') == -1:
        print("[登录未成功]：账号密码错误")
        QMessageBox.about(sself.ui, '[登录未成功]', '账号密码错误')
        return 1
    if http_post.text.find('的培养方案') != -1:
        print("[已成功登录]：成功登录系统")
        # QMessageBox.about(sself.ui, '[已成功登录]', '成功登录系统')
        if sself.ui.is_remember.isChecked():
            user_json = {}
            try:
                with open('userinfo.json', 'r') as user_file:
                    user_json = json.load(user_file)
                    if 'userList' not in user_json:
                        user_json['userList'] = [{"username": username, "password": password}]
                    else:
                        exist_flag = False
                        for i in range(len(user_json['userList'])):
                            if user_json['userList'][i]['username'] == username:
                                user_json['userList'][i]['password'] = password
                                exist_flag = True
                        if not exist_flag:
                            user_json['userList'].append({"username": username, "password": password})
                    user_file.close()
            except FileNotFoundError:
                user_json['userList'] = [{"username": username, "password": password}]
            with open('userinfo.json', 'w') as user_file:
                user_file.write(json.dumps(user_json))
                print("已经保存用户信息")
                user_file.close()

        return 0

