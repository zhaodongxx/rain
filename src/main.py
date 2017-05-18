import requests  # pip install requests
import re
import os  # pip install NetEaseMusicApi
import itchat  # pip install itchat
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from NetEaseMusicApi import interact_select_song
import random
from ftplib import FTP
from iFtp import iFtp
from iEmail import iEmail
import linecache


def check_mantis():
    payload = {
        'return': 'index.php',
        'username': 'zhaodong',
        'password': '123456',
        "secure_session": "on"
    }
    r = requests.post(
        "http://mantis.mlrkon.com:8088/mantis/login.php", data=payload)
    pattern = "分派给我的(.*?)</table>"

    if re.search(pattern, r.text, re.S) != None:
        itchat.send("mantis have your bug ! ! !", itchat.search_friends("君海棠"))


def tuling(msg):
    payload = {
        'key': '7a592d30d73e42f9b5fb35bac4434e9c',
        'info': msg,
        'userid': random.randint(100000, 999999)  # 返回[a,b]之间的整数,
    }
    r = requests.post("http://www.tuling123.com/openapi/api", data=payload)
    return r.json()


def back(line):
    if (line.split("; ")[1] == "root.zip"):
        info = line.split("; ")[0].split("Modify=")[1]
        ret1 = info[0:4] + "-" + info[4:6] + "-" + info[6:8]
        ret2 = info[8:10] + ":" + info[10:12] + ":" + info[12:14]
        ret = ret1 + " " + ret2
        friends = itchat.search_friends("君海棠")
        itchat.send(ret, toUserName=friends[0]['UserName'])


def root():
    ftp = FTP()
    timeout = 30
    port = 21
    ftp.connect('171.217.156.124', port, timeout)
    ftp.login('zhaodong', 'Zhaodong')
    ftp.cwd('pub/minds/install')  # 更改目录
    ftp.retrlines('MLSD', back)


def getRootUpdateTime(msg):
    iftp = iFtp()
    ret = iftp.pollRoot()

    if ret['flag']:
        itchat.send(
            u'root已打包  >' + ret['time'], toUserName=msg['FromUserName'])
    else:
        itchat.send(
            u'root未打包  >' + ret['time'], toUserName=msg['FromUserName'])


#
def pollRootUpdateTime():
    iftp = iFtp()
    ret = iftp.pollRoot()
    if ret['flag']:
        friends = itchat.search_friends("君海棠")
        itchat.send(
            u'root已打包 ' + ret['time'], toUserName=friends[0]['UserName'])
        email = iEmail()
        email.sendEmail(u'root已打包  >' + ret['time'])
        # else:
        # itchat.send(u'root未打包 ' + ret['time'],
        # toUserName=msg['FromUserName'])


def getAddr(self, parameter_list):
    count = len(open("1024.txt", 'rU').readlines())
    linenum = random.randint(1, count)
    addr = linecache.getline("1024.txt", linenum)

    return addr


@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    # if msg['ToUserName'] != 'filehelper': return

    if msg['Text'] == u'bug':
        check_mantis()
        itchat.send(u'checked', toUserName=msg['FromUserName'])
    elif msg['Text'] == u'包':
        getRootUpdateTime(msg)
    elif msg['Text'] == u'邮件':
        email = iEmail()
        email.sendEmail('这是一份来自小雨的邮件。。。')
    elif msg['Text'] == u'东西':
        itchat.send(getAddr(), toUserName=msg['FromUserName'])
    else:
        itchat.send(
            tuling(msg['Text'])['text'], toUserName=msg['FromUserName'])


# 在注册时增加isGroupChat=True将判定为群聊回复
@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def groupchat_reply(msg):
    FromUserName = msg['FromUserName']
    if msg['Text'] == u'睡觉':
        itchat.send(u'sleeping...', toUserName=msg['FromUserName'])
        sleep(60 * 60)
    if msg['Text'] == u'包':
        root()
    if msg['Text'] == u'bug':
        check_mantis()
        itchat.send(u'checked', toUserName=msg['FromUserName'])
    if msg['Text'] == u'小雨闭嘴':
        itchat.send(u'┭┮﹏┭┮    ', toUserName=msg['FromUserName'])
        sleep(60 * 5)
    if msg['Text'] == u'你不要说话':
        itchat.send(u'(⊙o⊙)？', toUserName=msg['FromUserName'])
        sleep(60 * 1)
        # itchat.logout()
    if msg['Text'] == u'你好烦':
        itchat.send(u'(￢︿̫̿￢☆)   ', toUserName=msg['FromUserName'])
        sleep(60 * 10)
        # itchat.logout()
    else:
        itchat.send(tuling(msg['Text'])['text'], msg['FromUserName'])


itchat.auto_login(True)
itchat.send("success login", 'filehelper')

sched = BackgroundScheduler()
sched.add_job(
    check_mantis,
    'interval',
    minutes=30,
    start_date='2017-05-05 00:00:00',
    end_date='2018-01-01 00:00:00')
sched.add_job(
    pollRootUpdateTime,
    'interval',
    minutes=5,
    start_date='2017-05-05 00:00:00',
    end_date='2018-01-01 00:00:00')
sched.start()

itchat.run()
