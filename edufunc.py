# -*- coding=utf-8 -*-
import requests
import json
import os
from configparser import ConfigParser

# 经过判断，Headers加与不加貌似都没有影响呢

# 初始化文件内容
def IniFile():
    '''
    将ini文件初始化为某种格式
    '''
    print('文件不存在或设置有误，已重新初始化文件')
    print('请在目录下set.ini填写账号密码')
    config = ConfigParser()
    config.add_section('HanxvenBasicSet')
    config.set('HanxvenBasicSet', 'account', '填入账号')
    config.set('HanxvenBasicSet', 'password', '填入密码')
    config.add_section('AutoFillSet')
    config.set('AutoFillSet', 'rand', 'randomcode=1588733273&client_key=13d443fc3a3b45ad429312bbad2b2a6d')
    config.set('AutoFillSet', 'header', '{"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36"  " (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36", "Host": "www.educoder.net",  "Origin": "https://www.educoder.net", "Connection": "keep-alive", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Accept": "application/json, text/plain, */*"}')
    config.write(open('set.ini', 'w'), space_around_delimiters=False)

# 检测文件内容,若无问题，返回0，反之返回1
def CheckSetFile():
    '''
    检测文件内容是否正确，若是，返回0，反之为非零值
    '''
    config = ConfigParser()
    if not os.path.exists("set.ini"):
        IniFile()
        return 1
    else:
        config.read('set.ini', encoding='utf-8')
        if not config.has_section('HanxvenBasicSet'):
            IniFile()
            return 1
        elif not config.has_section('AutoFillSet'):
            IniFile()
            return 1
        elif not config.has_option('HanxvenBasicSet','password'):
            IniFile()
            return 1
        elif not config.has_option('HanxvenBasicSet','account'):
            IniFile()
            return 1
        elif not config.has_option('AutoFillSet','header'):
            IniFile()
            return 1
        elif not config.has_option('AutoFillSet','rand'):
            IniFile()
            return 1
    return 0


# 该函数尝试登录educoder，并返回一个个人信息字典，若失败，返回空字典
def TryLogin():
    '''
    函数尝试按照ini文件提供的账号密码进行登录，成功则返回个人信息字典，否则返回空字典
    '''
    config = ConfigParser()
    config.read('set.ini', encoding='utf-8')
    LoginJson = { "login":config['HanxvenBasicSet']['account'], "password":config['HanxvenBasicSet']['password'], "autologin":1}
    LoginURL = "https://www.educoder.net/api/accounts/login.json?" + config['AutoFillSet']['Rand']
    header = json.loads(config['AutoFillSet']['header'])
    Res = requests.post(LoginURL, json=LoginJson, headers = header)
    Cookie = requests.utils.dict_from_cookiejar(Res.cookies)
    LoginResDict = json.loads(Res.text)
    InfoDict = {}
    InfoDict['cookie'] = Cookie
    if Cookie:
        InfoDict['id'] = LoginResDict["user_id"]
        InfoDict['login'] = LoginResDict["login"]
        InfoDict['name'] = LoginResDict["name"]
        InfoDict['grade'] = LoginResDict["grade"]
        InfoDict['identity'] = LoginResDict["identity"]
        InfoDict['school'] = LoginResDict["school"]
    return InfoDict


def Attendance(cookie, login):
    '''
    该函数尝试签到，接收一个cookie字典以及登录名
    '''
    config = ConfigParser()
    config.read('set.ini', encoding='utf-8')
    AttendanceUrl = "https://www.educoder.net/api/users/attendance.json?" + config['AutoFillSet']['rand']
    homePage = "https://www.educoder.net/api/users/" + login + "/homepage_info.json?" + config['AutoFillSet']['rand']
    header = json.loads(config['AutoFillSet']['header'])
    ResAttend = requests.post(AttendanceUrl, headers = header, cookies = cookie)
    ResHome = requests.get(homePage, cookies = cookie)
    AttendanceResDict = json.loads(ResAttend.text) # 签到后获得的响应，打包成字典
    HomePageInfoDict = json.loads(ResHome.text) # 获取主页面的相应

    if AttendanceResDict["status"] == 0:
        print(f"签到成功,当前{AttendanceResDict['grade']},下一级{AttendanceResDict['next_gold']}")
    else: 
        print(f"已经签到过,当前经验{HomePageInfoDict['experience']},金币{HomePageInfoDict['grade']}")

# 主函数入口
if __name__ == '__main__':

    CheckSetFile()
    Dict = TryLogin()

    if Dict:
        print(Dict)
    else:
        print('账号或者密码不正确，未能获得正确的cookie')
    
    Attendance(Dict['cookie'], Dict['login'])