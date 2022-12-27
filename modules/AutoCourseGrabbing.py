import json
import time

import requests.exceptions
from PySide2.QtCore import QThread
from PySide2.QtWidgets import QMessageBox, QTableWidgetItem

from modules.utils import *

class Thread_start(QThread):
    def __init__(self, sself):
        super().__init__()
        self.sself = sself
        self.course_grabbing = sself.course_grabbing

    def run(self) -> None:
        self.course_grabbing.start(self.sself)



class AutoCourseGrabbing:
    def __init__(self):
        self.data = {}
        self.fxid = 0
        self.numc = {}
        # self.tokenVal = ""
        self.data_list = []

    def show_course_in_table(self, data_list, sself):
        """
        显示课程信息
        :param data_list:
        :param sself:
        :return:
        """
        if not isinstance(data_list,list):
            data_list = [data_list]
        print(data_list)
        sself.ui.table.setRowCount(len(data_list))
        idx = 0
        for classData in data_list:
            # 课程序号 ---------------------------------
            try:
                classUUID = str(classData['kch'])
            except (ValueError, TypeError, Exception):
                classUUID = "?????????"
            # 课程名称 ---------------------------------
            try:
                className = str(classData['kcm'])[0:15]
            except (ValueError, TypeError, Exception):
                className = "未知课程名称, 数据错误!!!"
            # 上课校区 ---------------------------------
            try:
                classArea = str(classData['kkxqm'])
            except (ValueError, TypeError, Exception):
                classArea = "未知"
            # 课程余量 ---------------------------------
            try:
                classFree = str(classData['bkskyl'])
            except (ValueError, TypeError, Exception):
                classFree = "??"
            # 课程楼层 ---------------------------------
            try:
                roomBuild = str(classData['jxlm'])[0:4]
            except (ValueError, TypeError, Exception):
                roomBuild = "????"
            # 课程教室 ---------------------------------
            try:
                classRoom = str(classData['jasm'])[0:4]
            except (ValueError, TypeError, Exception):
                classRoom = "未知地点"
            # 课程周数 ---------------------------------
            try:
                classWeek = str(classData['zcsm'])
            except (ValueError, TypeError, Exception):
                classWeek = "????"
            # 课程天数 ---------------------------------
            try:
                classDays = classData['skxq']  # 天数
            except (ValueError, TypeError, Exception):
                classDays = 8
            # 课程开始 ---------------------------------
            try:
                classTime = str(classData['skjc'])
            except (ValueError, TypeError, Exception):
                classTime = "??"
            # 课程结束 ---------------------------------
            try:
                tmpTime = int(str(classData['cxjc']))
                classEnds = str(int(classTime) + tmpTime - 1)
            except (ValueError, TypeError, Exception):
                classEnds = "0"
            # 课程教师 ---------------------------------
            try:
                classTech = str(classData['skjs'][0:9])
            except (ValueError, TypeError, Exception):
                classTech = "未知教师"

            sself.ui.table.setItem(idx, 0, QTableWidgetItem(classUUID))
            sself.ui.table.setItem(idx, 1, QTableWidgetItem(className))
            sself.ui.table.setItem(idx, 2, QTableWidgetItem(classArea))
            sself.ui.table.setItem(idx, 3, QTableWidgetItem(classFree))
            sself.ui.table.setItem(idx, 4, QTableWidgetItem(roomBuild))
            sself.ui.table.setItem(idx, 5, QTableWidgetItem(classRoom))
            sself.ui.table.setItem(idx, 6, QTableWidgetItem(classWeek))
            sself.ui.table.setItem(idx, 7, QTableWidgetItem(classDays))
            sself.ui.table.setItem(idx, 8, QTableWidgetItem(classTime + "-" + classEnds))
            sself.ui.table.setItem(idx, 9, QTableWidgetItem(classTech))
            idx += 1

    def selectRes(self, sself):
        """
        选课结果
        :param sself:
        :return:
        """
        try:
            res_data = http_main.get(http_urls_select_res)
        except requests.exceptions.ConnectionError or BaseException:
            print("网络错误")
            QMessageBox.about(sself.ui, '[错误]', '网络错误')
            return -2
        json_data = json.loads(res_data.text)
        self.fxid = json_data['dateList'][0]['programPlanCode']
        # token_temp = res_data.text.find('id="tokenValue"')
        # self.tokenVal = res_data.text[token_temp + 23: token_temp + 55]
        sself.ui.table.setRowCount(len(json_data['xkxx'][0]))
        idx = 0
        for e_course in json_data['xkxx'][0]:
            e_exam_type = json_data['xkxx'][0][e_course]['examTypeName']
            e_teacher_name = str(json_data['xkxx'][0][e_course]['attendClassTeacher']).split(" ")
            if len(e_teacher_name) <= 1:
                e_teacher_name = "未知"
            else:
                e_teacher_name = e_teacher_name[0]
            e_course_type = json_data['xkxx'][0][e_course]['coursePropertiesName']
            if len(json_data['xkxx'][0][e_course]['timeAndPlaceList']) > 0:
                e_week_desc = json_data['xkxx'][0][e_course]['timeAndPlaceList'][0]['weekDescription']
                e_day = json_data['xkxx'][0][e_course]['timeAndPlaceList'][0]['classDay']
                e_start_time = json_data['xkxx'][0][e_course]['timeAndPlaceList'][0]['classSessions']
                e_during_time = json_data['xkxx'][0][e_course]['timeAndPlaceList'][0]['continuingSession']
                try:
                    e_end_time = str(int(e_start_time) + int(e_during_time) - 1)
                except ValueError:
                    e_end_time = "0"
            e_course_name = json_data['xkxx'][0][e_course]['courseName']
            sself.ui.table.setItem(idx, 0, QTableWidgetItem(e_course))
            sself.ui.table.setItem(idx, 1, QTableWidgetItem(e_course_type))
            sself.ui.table.setItem(idx, 2, QTableWidgetItem(e_exam_type))
            sself.ui.table.setItem(idx, 3, QTableWidgetItem(e_teacher_name))
            sself.ui.table.setItem(idx, 4, QTableWidgetItem(e_week_desc))
            sself.ui.table.setItem(idx, 5, QTableWidgetItem(str(e_day)))
            sself.ui.table.setItem(idx, 6, QTableWidgetItem(str(e_start_time) + "-" + str(e_end_time)))
            sself.ui.table.setItem(idx, 7, QTableWidgetItem(e_course_name))
            idx += 1

    def query_course(self, sself):
        """
        查询课程
        :param sself:
        :return:
        """
        query_content = sself.ui.query_info.text()
        query_data = {
            "kkxsh": "",
            "kch": "",
            "kcm": query_content,
            "skjs": "",
            "xq": "0",
            "jc": "0",
            "kclbdm": ""
        }
        try:
            query_res = http_main.get(http_urls_course_select)
            if query_res.text.find("自由选课") != -1:
                query_res = http_main.post(http_urls_course_list, query_data)
            else:
                print("当前非选课阶段，或者教务处网站挂了，或者你的网络不行")
                QMessageBox.about(sself.ui, '[错误]', '当前非选课阶段，或者教务处网站挂了，或者你的网络不行')
                return -3
        except requests.exceptions.ConnectionError:
            print("网络错误")
            QMessageBox.about(sself.ui, '[错误]', '网络错误')
            return -2
        raw_data = json.loads(query_res.text)
        if type(raw_data['rwRxkZlList']) is str:
            data_list = json.loads(raw_data['rwRxkZlList'])
        elif type(raw_data['rwRxkZlList']) is list:
            data_list = raw_data['rwRxkZlList']
        else:
            print("网络错误")
            QMessageBox.about(sself.ui, '[错误]', '网络错误')
            return -2
        self.data_list = data_list
        self.fxid = json.loads(raw_data['yxkclist'])[0]['programPlanNumber']
        self.show_course_in_table(data_list, sself)

    def add_course(self, sself):
        """
        添加课程
        :param sself:
        :return:
        """
        selected_row = sself.ui.table.selectedItems()
        print("选中的行数")
        selected_row = [e.row() for e in selected_row]
        selected_row = list(set(selected_row))
        print(selected_row)
        addles_tpdt = {
            'dat1': [],
            'dat2': [],
            'dat3': [],
            'dat4': [],
        }
        idx = 0
        for each_data in self.data_list:
            for each_selected in selected_row:
                if idx == each_selected:
                    addles_tpdt['dat1'].append(each_data['kcm'])
                    addles_tpdt['dat2'].append(each_data['jasm'])
                    addles_tpdt['dat3'].append(each_data['skjs'])
                    addles_tpdt['dat4'].append(each_data['kxh'])
            idx += 1
        self.data[sself.ui.query_info.text()] = addles_tpdt
        self.numc[sself.ui.query_info.text()] = len(selected_row)
        print("成功添加")
        # print(addles_tpdt)
        QMessageBox.about(sself.ui, '[成功]', '成功将' + str(self.numc[sself.ui.query_info.text()]) + '门课程添加进列表')

    def start(self, sself):
        """
        开始抢课
        :param sself:
        :return:
        """
        sself.ui.start_btn.setEnabled(False)
        # 查看当前添加的课程列表
        print(self.data)
        loop_time = sself.ui.time.text()
        if len(self.data) == 0:
            print("[尚未添加课程]:请先添加课程，然后再重新开始抢课")
            # QMessageBox.about(sself.ui, '[提示]', '[尚未添加课程]:请先添加课程，然后再重新开始抢课')
            sself.communicate.message.emit('[尚未添加课程]:请先添加课程，然后再重新开始抢课')
            return -1
        flag = 0
        count = 0
        begin_time = time.time()
        last_time = time.time()
        while flag == 0:
            count += 1
            all_time = str((time.time() - begin_time) // 3600) + "时" + str(
                ((time.time() - begin_time) % 3600) // 60) + "分" + str(((time.time() - begin_time) % 60) // 1) + "秒"
            lunxun = str(int((time.time() - last_time) * 1000))
            last_time = time.time()
            print(" 当前次数：" + str(count),
                  " 总共耗时：" + all_time,
                  " 轮询速度：" + str(lunxun) + "ms/次",
                  " 设定速度：" + str(loop_time) + "s/次")
            sself.communicate.top_bar.emit(" 当前次数：" + str(count) +
                  " 总共耗时：" + all_time +
                  " 轮询速度：" + str(lunxun) + "ms/次")

            time.sleep(int(loop_time) - 1)
            try:
                addles_datr = http_main.get(http_urls_course_select)
            except requests.exceptions.ConnectionError:
                print("网络错误")
                continue
            try:
                data_change = False
                for addles_name in list(self.data):
                    if data_change:
                        break
                    addles_post = {
                        "searchtj": addles_name,
                        "xq": 0,
                        "jc": 0,
                        "kclbdm": ""
                    }
                    addles_data = http_main.post(http_urls_course_list, addles_post)
                    addles_tabs = json.loads(addles_data.text)
                    if type(addles_tabs['rwRxkZlList']) is str:
                        addles_list = json.loads(addles_tabs['rwRxkZlList'])
                    elif type(addles_tabs['rwRxkZlList']) is list:
                        addles_list = addles_tabs['rwRxkZlList']
                    else:
                        print("网络错误")
                        sself.communicate.message.emit('网络错误')
                        return -2
                    addles_nums = 0
                    for addles_loop in addles_list:
                        if data_change:
                            break
                        addles_nums += 1
                        for addles_tttp in range(0, self.numc[addles_name]):
                            if data_change:
                                break
                            if self.data[addles_name]['dat1'][addles_tttp] == addles_loop['kcm'] \
                                    and self.data[addles_name]['dat2'][addles_tttp] == addles_loop['jasm'] \
                                    and self.data[addles_name]['dat3'][addles_tttp] == addles_loop['skjs'] \
                                    and self.data[addles_name]['dat4'][addles_tttp] == addles_loop['kxh']:
                                # print(addles_loop)
                                self.show_course_in_table(addles_loop, sself)
                                if int(addles_loop['bkskyl']) > 0:
                                    zxyk_name = ""
                                    for i in range(0, len(addles_loop['kcm'])):
                                        zxyk_name += str(int((hex(ord(addles_loop['kcm'][i])).zfill(4)), 16)) + ","
                                    zxyk_temp = addles_datr.text.find('id="tokenValue"')
                                    zxyk_toke = addles_datr.text[zxyk_temp + 23:zxyk_temp + 55]
                                    zxyk_post = {
                                        "dealType": 5,
                                        "kcIds": addles_loop['kch']
                                                 + "@"
                                                 + addles_loop['kxh']
                                                 + "@"
                                                 + addles_loop['zxjxjhh'],
                                        "kcms": zxyk_name,
                                        "fajhh": self.fxid,
                                        "sj": "0_0",
                                        "searchtj": addles_name,
                                        "kclbdm": "",
                                        "inputCode": "",
                                        "tokenValue": zxyk_toke
                                    }
                                    try:
                                        addles_data = http_main.post(http_urls_post, zxyk_post)
                                    except requests.exceptions.ConnectionError:
                                        print("网络错误")
                                        continue
                                    if addles_data.text.find("ok") != -1:
                                        print(addles_loop['kcm'] + "抢课成功")
                                        # QMessageBox.about(sself.ui, '[成功]', addles_loop['kcm'] + '抢课成功')
                                        sself.communicate.message.emit(addles_loop['kcm'] + '抢课成功')
                                        self.data.pop(addles_name)
                                        data_change = True
                                    else:
                                        print("抢课失败")
                                        # QMessageBox.about(sself.ui, '[失败]', addles_loop['kcm'] + '抢课失败')
                                        sself.communicate.message.emit(addles_loop['kcm'] + '抢课失败')
                                        time.sleep(5)
                                        flag = 0
                                        break
                                    if len(self.data) <= 0:
                                        flag = 1
                                        break
                                    print("系统返回内容：" + addles_data.text)
                        if len(self.data) <= 0:
                            flag = 1
                            break
                    if len(self.data) <= 0:
                        flag = 1
                        break
                if len(self.data) <= 0:
                    flag = 1
                    break
            except KeyboardInterrupt:
                return -1
            except requests.exceptions.ConnectionError:
                print("网络错误")
                # QMessageBox.about(sself.ui, '[错误]', '网络错误')
                sself.communicate.message.emit('网络错误')
                continue
        print("抢课全部结束")
        # QMessageBox.about(sself.ui, '[成功]', '抢课全部结束')
        sself.communicate.message.emit('抢课全部结束')

    def delete(self, sself):
        """
        退课
        :param sself:
        :return:
        """
        selected_row = sself.ui.table.selectedItems()
        print("选中的行数")
        selected_row = [e.row() for e in selected_row]
        selected_row = list(set(selected_row))
        print(selected_row)
        for e_row in selected_row:
            try:
                addles_datr = http_main.get(http_urls_course_quit)
            except requests.exceptions.ConnectionError:
                print("网络错误")
            token_temp = addles_datr.text.find('id="tokenValue"')
            tokenval = addles_datr.text[token_temp + 23: token_temp + 55]
            course = sself.ui.table.item(e_row, 0).text()
            name = sself.ui.table.item(e_row, 7).text()
            course = course.split('_')
            data = {
                "fajhh": self.fxid,
                "kch": course[0],
                "kxh": course[1],
                "tokenValue": tokenval
            }
            post_res = http_main.post(http_urls_delete, data)
            print(post_res.text)
            if post_res.text.find("删除课程成功") != -1:
                print(name + "删除成功")
                QMessageBox.about(sself.ui, '[成功]', name + '删除成功')
        self.selectRes(sself)
