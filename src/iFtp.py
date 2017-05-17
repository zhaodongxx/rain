#! /usr/bin/env python
# -*- coding: utf-8 -*-

# *************************************************************
#     Filename @  ftp.py
#       Author @  zhaodong
#  Create date @  2017-05-16 20:40:50
#  Description @
# *************************************************************
from ftplib import FTP


class iFtp:

    prevRootTime = "1999-01-01 00:00:00"
    nowRootTime = "1999-01-01 00:00:00"

    def back(line):
        if (line.split("; ")[1] == "root.zip"):
            info = line.split("; ")[0].split("Modify=")[1]
            ret1 = info[0:4] + "-" + info[4:6] + "-" + info[6:8]
            ret2 = info[8:10] + ":" + info[10:12] + ":" + info[12:14]
            iFtp.nowRootTime = ret1 + " " + ret2

    def loginFtp():
        ftp = FTP()
        timeout = 30
        port = 21
        ftp.connect('171.217.156.124', port, timeout)
        ftp.login('zhaodong', 'Zhaodong')
        ftp.cwd('pub/minds/install')  # 更改目录
        return ftp

    def init():
        #ftp.itchat = itchat;
        ftp = iFtp.loginFtp()
        ftp.retrlines('MLSD', iFtp.back)
        iFtp.prevRootTime = iFtp.nowRootTime
        print("init... time:" + iFtp.prevRootTime)

    #@staticmethod
    def pollRoot(params):
        #ftp.itchat = itchat
        ftp = iFtp.loginFtp()
        ftp.retrlines('MLSD', iFtp.back)
        if iFtp.prevRootTime < iFtp.nowRootTime:
            iFtp.prevRootTime = iFtp.nowRootTime
            return {'flag': True, 'time': iFtp.prevRootTime}
        else:
            return {'flag': False, 'time': iFtp.nowRootTime}


try:
    iFtp.init()
except TimeoutError:
    print("ftp服务器连接失败")
