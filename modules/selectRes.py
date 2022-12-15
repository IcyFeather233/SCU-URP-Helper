import json

import requests.exceptions
from PySide2.QtWidgets import QMessageBox, QTableWidgetItem

from modules.utils import *

def urp_selectRes(sself):
    try:
        res_data = http_main.get(http_urls_select_res)
    except requests.exceptions.ConnectionError or BaseException:
        print("网络错误")
        QMessageBox.about(sself.ui, '[错误]', '网络错误')
        return -2
    json_data = json.loads(res_data.text)
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
