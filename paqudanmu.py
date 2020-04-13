# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 11:41:41 2020

@author: 86137
"""
import time
import requests
import json
import pymysql
Roomid=input()#764155房间号
url ='https://api.live.bilibili.com/xlive/web-room/v1/dM/gethistory'

#请求头
headers={
    'Content-Type':'application/x-www-form-urlencoded',
    'Origin': 'https://live.bilibili.com',
    'Referer':'https://live.bilibili.com/5225369?spm_id_from=333.334.b_62696c695f6c697665.5',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
}
#请求体
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

########
def create():
    
    #打开数据库连接
    db = pymysql.connect(host='localhost',port=3306,user='root',passwd='721017988',database='BiliBiliDanMu',charset='utf8',connect_timeout=10)
    
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    
    # 如果数据表已经存在使用 execute() 方法删除表。
    cursor.execute("DROP TABLE IF EXISTS ROOMID")

    # 创建数据表SQL语句
    sql = """CREATE TABLE ROOMID (
            RID INT(8),
            UID INT,
            NICKNAME CHAR(16),
            TEXT CHAR(32),
            TIMELINE DATETIME,
            VIP TINYINT UNSIGNED,
            SVIP TINYINT UNSIGNED,
            ISADMIN TINYINT UNSIGNED,
            GUARDLEVEL INT(2),
            MEDALLEVEL INT(2),
            MEDAL CHAR(8)
             )"""
    try:
         
        # 执行SQL语句
        cursor.execute(sql)
        print("创建数据库成功")
    except Exception as e:
        print("创建数据库失败：case%s"%e)
    finally:
        
        #关闭游标连接
        cursor.close()

        # 关闭数据库连接
        db.close()
 
def insert(value):

    # 打开数据库连接
    db = pymysql.connect(host='localhost',port=3306,user='root',passwd='721017988',database='BiliBiliDanMu',charset='utf8')

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 插入语句
    sql = "INSERT INTO ROOMID(RID,UID,NICKNAME,TEXT,TIMELINE,VIP,SVIP,ISADMIN,GUARDLEVEL,MEDALLEVEL,MEDAL)VALUES(%s, %s,' %s',' %s',' %s', %s, %s, %s, %s, %s,' %s')"%(value[0],value[1],value[2],value[3],value[4],value[5],value[6],value[7],value[8],value[9],value[10])
    try:
        cursor.execute(sql)
        db.commit()
        print('插入数据成功')
    except:
        db.rollback()
        print("插入数据失败")
    db.close()


#实时请求数据
create()
while True:
    time.sleep(2)
    response=requests.post(url=url,headers=headers,data=dat)
    dic_data=response.json()
    # print(type(dic_data))
    content=[item for item in dic_data['data']['room']]
    for item in content:
        if len(item['medal']):#判断是否有牌子
            value=[Roomid,item['uid'],item['nickname'],item['text'],item['timeline'],item['vip'],item['svip'],item['isadmin'],item['guard_level'],item['medal'][0],item['medal'][1]]
        else:
            value=[Roomid,item['uid'],item['nickname'],item['text'],item['timeline'],item['vip'],item['svip'],item['isadmin'],item['guard_level'],0,'medal']
        insert(value)
