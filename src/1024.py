#!/usr/bin/env python

from io import *
import string
import requests


def urliter():
    for i in range(100000):
        for j in string.ascii_lowercase:
            for k in string.ascii_lowercase:
                yield "http://www.%02d%c%c%c%c.com" % (i, j, k, j, k)


for u in urliter():
    try:
        #print(u)
        wp = requests.get(u)
        print("find  " + u)
        logfile = open('1024.txt', 'a')
        logfile.write(u + "\n")

    except:
        pass

logfile.close()
