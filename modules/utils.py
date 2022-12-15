import requests

http_main = requests.session()

http_url_init = "http://zhjw.scu.edu.cn/login"
http_urls_select_res = "http://zhjw.scu.edu.cn/student/courseSelect/thisSemesterCurriculum/callback"
http_urls_course_select = "http://zhjw.scu.edu.cn/student/courseSelect/courseSelect/index"
http_urls_course_list = "http://zhjw.scu.edu.cn/student/courseSelect/freeCourse/courseList"
http_urls_post = "http://zhjw.scu.edu.cn/student/courseSelect/selectCourse/checkInputCodeAndSubmit"
http_urls_delete = "http://zhjw.scu.edu.cn/student/courseSelect/delCourse/deleteOne"
http_urls_course_quit = "http://zhjw.scu.edu.cn/student/courseSelect/quitCourse/index"

http_head = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.33"}

proxies = {
  'http': 'http://127.0.0.1:8888',
  'https': 'http://127.0.0.1:8888',
}
