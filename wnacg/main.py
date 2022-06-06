#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import sys
import re
import os
import time

target_site="http://www.wnacg.org"
work_dir=os.getcwd()
response=None
path=None
url=None
rate=0

def enquire():
    global response,url
    try:
        url=sys.argv[1]
    except IndexError:
        print("not have url")
        os._exit(1)
    if(re.search("index",url)):
        url=re.sub("index","slide",url)
        #print(url)
    response=requests.get(url)

def get_pic_url():
    pic_info=re.search("/photo.*\.html",str(response.text)).group()
    pic_info=target_site+pic_info
    doc=requests.get(pic_info)
    pic_url=re.findall("(?<=//).*?\.jpg(?=\\\\\")",str(doc.text))
    return pic_url

def down_pic(pic_url):
    num=1
    for i in pic_url:
        print("picture:"+str(num))
        pic=requests.get("http://"+i).content
        with open(path+"/"+str(num)+".jpg","wb") as f:
            f.write(pic)
        num+=1
        time.sleep(rate)

def mkdir():
    global path
#   title=re.search("(?<=<title>).*(?=</title>)",str(response.text)).group()
#   OSError: [Errno 36] File name too long:
    title=str(int(time.time()))
    path=work_dir+"/"+title
    os.mkdir(path)

def start():
    enquire()
    mkdir()
    down_pic(get_pic_url())

if __name__=='__main__':
    start()
