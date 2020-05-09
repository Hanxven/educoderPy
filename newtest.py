# -*- coding=utf-8 -*-

import os
import json
import requests
from configparser import ConfigParser
import re

# 本部分用于测试调节的时间





# randomcode=1588676483&client_key=f396618f2275852b72507f55bd9fba51
randomcode = 'randomcode=1588954716&client_key=ff532ff39bc3c3be9adb3f1f2e0f91b6'
# randomcode = 'randomcode=1588936916&client_key=77f047237b93a38ab9d78f52f9c7cc0d'
# randomcode = 'randomcode=1588676483&client_key=f396618f2275852b72507f55bd9fba51'
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                  'AppleWebKit/537.36 (KHTML, '
                  'like Gecko) Chrome/67.0.3396.99 '
                  'Safari/537.36',
    'Host': "www.educoder.net",
#    'Referer':'None',
    'Origin':'https://www.educoder.net',
    'Connection': 'keep-alive',
    'Sec-Fetch-Site':'same-origin',
    'Sec-Fetch-Mode':'cors',
    'Sec-Fetch-Dest':'empty',
    'Accept':'application/json, text/plain, */*',
}

inputcor = 0
while inputcor != 1:
    ACC = input("输入账号:")
    PWD = input("输入密码:")
    LoginJson = { "login":ACC, "password":PWD, "autologin":1}
    Res = requests.post('https://www.educoder.net/api/accounts/login.json?' + randomcode, json=LoginJson, headers = header)
    curjs = json.loads(Res.text)
#    print(curjs)
    if 'user_id' in curjs.keys():
        print('登录成功')
        login = curjs['login']
        inputcor = 1
    else:
        print('请检查账号或密码的正确性')

cookie = requests.utils.dict_from_cookiejar(Res.cookies)

URL = 'https://www.educoder.net/api/users/'+ login +'/courses.json?' + randomcode + '&page=1&sort_by=updated_at&sort_direction=desc&per_page=64'
res = requests.get(URL, headers = header, cookies=cookie)
result = json.loads(res.text)
#print(result)

# 因为缺少相应的样本账号，当老师有多个时暂时不受用
# 遍历每个老师的ID，本处only一个
teacherid = []
for item in result['courses']:
    teacherid.append(item['id'])

# 实验性功能
# classroom = 'https://www.educoder.net/api/courses/' + str(teacherid[0]) + '/left_banner.json?' + randomcode
container = 'https://www.educoder.net/api/courses/' + str(teacherid[0]) + '/homework_commons.json?type=4&' + randomcode
clg = 'https://www.educoder.net/api/shixuns/'+ login +'/challenges.json?randomcode=1588900692&client_key=426f282e4b59872ec8db1d237a63c43b'

print(f"当前课程ID:{teacherid[0]}")
print('因为程序是半成品，目前只能对[第一个][加入的课程]进行修改')

resp = requests.get(container, headers = header, cookies=cookie)
resultShixun = json.loads(resp.text)
# print(resultShixun)

ShixunIDList = []

for item in resultShixun['homeworks']:
    ShixunIDList.append(item['shixun_identifier'])


Allcontainer = []
for ids in ShixunIDList:
    try:
        shixunIDURL = 'https://www.educoder.net/api/shixuns/' + ids + '/challenges.json?' + randomcode
        shixun = requests.get(shixunIDURL, headers = header, cookies=cookie)
        cur = json.loads(shixun.text)
        for item in cur['challenge_list']:
            Allcontainer.append([item['open_game'].split('/')[2],item['name'], item['status']])
    except:
        pass
    # 无权限访问的将不会去访问


# status 2为完成，其他未完成

# 获取了全部的实训container

number = 0
for it in Allcontainer:
    print(f"序号{number:3}: 容器ID:{it[0]}, 名称:{it[1]}, 状态:{'已完成' if it[2] == 2 else '未完成'}")
    number += 1



# 获得要修改的实

while True:
    inputcor = 0
    while inputcor != 1:
        select = input('输入要更改的序号，以及要更改的时间(单位秒)[中间用空格或逗号进行分割](中文逗号也可)，退出则Q/q:')
        if select == 'q' or select == 'Q':
            break
        lst = re.split(r'[\s,，]', select)
        if len(lst) != 2:
            print('输入有误，请重新')
            continue
        if not lst[0].isdigit() or not lst[1].isdigit():
            print('必须输入正整数，请重新')
            continue
        if int(lst[0]) > len(Allcontainer) - 1 or int(lst[0]) < 0:
            print('越界，请重新')
            continue
        if Allcontainer[int(lst[0])][2] != 2:
            print('不能选择未完成的，请重新')
            continue
        inputcor = 1
    if select == 'q' or select == 'Q':
        break
    time = f'&time={int(lst[1])}'
    DistoryingURL = 'https://www.educoder.net/api/tasks/' + Allcontainer[int(lst[0])][0] + '/cost_time.json?' + randomcode + '&time=-99999999'
    TimeURL = 'https://www.educoder.net/api/tasks/' + Allcontainer[int(lst[0])][0] + '/cost_time.json?' + randomcode + time
    res = requests.get(DistoryingURL, headers =header, cookies = cookie)
    res = requests.get(TimeURL, headers =header, cookies = cookie)
    resjs = json.loads(res.text)
    print("执行结果:")
    for item in resjs:
        print(f'{item}:{resjs[item]}')

i = os.system('pause')