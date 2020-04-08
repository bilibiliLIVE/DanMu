# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 11:41:41 2020

@author: 86137
"""
import time
import requests
Roomid=input()#764155房间号
url ='https://api.live.bilibili.com/xlive/web-room/v1/dM/gethistory'
dat={'roomid'	:Roomid,
'csrf_token':'6889415833245876182d74a0f361b641',
'csrf'	:'6889415833245876182d74a0f361b641',
'visit_id':''}
def Text():#弹幕内容
 while True:  
  html=requests.post(url,data=dat)
  text=list(map(lambda ii: html.json()['data']['room'][ii]['text'],range(10)))
  time.sleep(5)
  #print("{}:{}:{}".format(nickname,text,timeline))
  return text

def Time_Line():#时间
    while True:  
      html=requests.post(url,data=dat)
      timeline=list(map(lambda ii: html.json()['data']['room'][ii]['timeline'],range(10)))
      time.sleep(5)
      return timeline
  
def Nick_Name():#用户名
    while True:  
      html=requests.post(url,data=dat)
      nickname=list(map(lambda ii: html.json()['data']['room'][ii]['naickname'],range(10)))
      time.sleep(5)
      return nickname

def User_Id():#用户ID
    while True:  
      html=requests.post(url,data=dat)
      uid=list(map(lambda ii: html.json()['data']['room'][ii]['uid'],range(10)))
      time.sleep(5)
      return uid

def User_Level():#用户等级
    while True:  
      html=requests.post(url,data=dat)
      user_level=list(map(lambda ii: html.json()['data']['room'][ii]['user_level'],range(10)))
      time.sleep(5)
      return user_level
     
def Vip():#用户是否为VIP
    while True:  
      html=requests.post(url,data=dat)
      vip=list(map(lambda ii: html.json()['data']['room'][ii]['vip'],range(10)))
      time.sleep(5)
      return vip

def Svip():#用户是否为SVIP
    while True:  
      html=requests.post(url,data=dat)
      svip=list(map(lambda ii: html.json()['data']['room'][ii]['svip'],range(10)))
      time.sleep(5)
      return svip
  
def Guard_Level():#牌子
    while True:  
      html=requests.post(url,data=dat)
      guard_level=list(map(lambda ii: html.json()['data']['room'][ii]['guard_level'],range(10)))
      time.sleep(5)
      return guard_level
         
def Bubble():#气泡
    while True:  
      html=requests.post(url,data=dat)
      bubble=list(map(lambda ii: html.json()['data']['room'][ii]['bubble'],range(10)))
      time.sleep(5)
      return bubble
  
def User_Name_Color():#牌子
    while True:  
      html=requests.post(url,data=dat)
      uname_color=list(map(lambda ii: html.json()['data']['room'][ii]['uname_color'],range(10)))
      time.sleep(5)
      return uname_color
   
  