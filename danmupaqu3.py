#填入本地MySQL数据库访问密码
#项目目录下放图片"大象",实际上更换任何背景图片可生成相应形状的词云
#本地安装相应模块包

import time
import requests
import pymysql
import datetime
import threading
import tkinter as tk


Roomid = 904823
user='root'
passwd='qzw3066906793'
database='BiliBiliDanMu'
button = False
start_sign = False

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

def create_temp(Roomid):#爬取过程中建立临时表
    
    #打开数据库连接
    db = pymysql.connect(host='localhost',port=3306,user=user,passwd=passwd,database=database,charset='utf8',connect_timeout=10)
    
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    
    # 如果数据表已经存在使用 execute() 方法删除表。
    sql = "DROP TABLE IF EXISTS `%s`"%(Roomid)
    cursor.execute(sql)

    # 创建数据表SQL语句
    sql = "CREATE TABLE `%s`(UID INT,NICKNAME CHAR(16),TEXT CHAR(32),TIMELINE DATETIME,VIP TINYINT UNSIGNED,SVIP TINYINT UNSIGNED,ISADMIN TINYINT UNSIGNED, GUARDLEVEL INT(2),MEDALLEVEL INT(2),MEDAL CHAR(8))"%(Roomid)
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

def create(Roomid):#爬取结束建立去重后的表
    
    #打开数据库连接
    db = pymysql.connect(host='localhost',port=3306,user=user,passwd=passwd,database=database,charset='utf8',connect_timeout=10)
    
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    
    # 如果数据表已经存在使用 execute() 方法删除表。
    sql = "DROP TABLE IF EXISTS `%s/%s/%s-%s`"%(datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day,Roomid)
    cursor.execute(sql)

    # 创建数据表SQL语句
    sql = "create table `%s/%s/%s-%s` as(select distinct UID,NICKNAME,TEXT,TIMELINE,VIP,SVIP,ISADMIN,GUARDLEVEL,MEDALLEVEL,MEDAL from `%s`)"%(datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day,Roomid,Roomid)
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

def insert(value):#向表中插入记录

    # 打开数据库连接
    db = pymysql.connect(host='localhost',port=3306,user=user,passwd=passwd,database=database,charset='utf8',connect_timeout=10)

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 插入语句
    sql = "INSERT INTO `%s`(UID,NICKNAME,TEXT,TIMELINE,VIP,SVIP,ISADMIN,GUARDLEVEL,MEDALLEVEL,MEDAL)VALUES(%s,' %s',' %s',' %s', %s, %s, %s, %s, %s,' %s')"%(value[0],value[1],value[2],value[3],value[4],value[5],value[6],value[7],value[8],value[9],value[10])
    try:
        cursor.execute(sql)
        db.commit()
        print('插入数据成功')
    except:
        db.rollback()
        print("插入数据失败")
    db.close()

def ShowTables():#显示database已有的所有表单

     # 打开数据库连接
    db = pymysql.connect(host='localhost',port=3306,user=user,passwd=passwd,database=database,charset='utf8',connect_timeout=10)

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # 显示database已有的所有表单
    cursor.execute("show tables;")
    ShowTables_var.set(cursor.fetchall())
    
    #关闭游标连接
    cursor.close()

    # 关闭数据库连接
    db.close()

def DeleteTable(TableName):#自动删除表单所用
    
    #打开数据库连接
    db = pymysql.connect(host='localhost',port=3306,user=user,passwd=passwd,database=database,charset='utf8',connect_timeout=10)
    
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    
    # 如果数据表已经存在使用 execute() 方法删除表。
    sql = "DROP TABLE IF EXISTS `%s`"%(TableName)
    cursor.execute(sql)

    #关闭游标连接
    cursor.close()

    # 关闭数据库连接
    db.close()

def DeleteSelectedTable():#手动删除表单所用
    
    #打开数据库连接
    db = pymysql.connect(host='localhost',port=3306,user=user,passwd=passwd,database=database,charset='utf8',connect_timeout=10)
    
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    
    # 如果数据表已经存在使用 execute() 方法删除表。
    sql = "DROP TABLE IF EXISTS `%s`"%(ShowTables_list.get(ShowTables_list.curselection()))#DeleteSelectedTable_var.get()
    try:
        cursor.execute(sql)
        db.commit()
        print('删除表单成功')
    except:
        db.rollback()
        print("删除表单失败")
    db.close()

def Crawling():#多线程循环爬取弹幕，这里可以填写任何需要循环显示的内容

    global start_sign
    global Roomid

    ShowTables()


    if start_sign and Roomid:
            response=requests.post(url=url,headers=headers,data=dat)
            dic_data=response.json()
            content=[item for item in dic_data['data']['room']]
            for item in content:
                if len(item['medal']):#判断是否有牌子
                    value=[Roomid,item['uid'],item['nickname'],item['text'],item['timeline'],item['vip'],item['svip'],item['isadmin'],item['guard_level'],item['medal'][0],item['medal'][1]]
                else:
                    value=[Roomid,item['uid'],item['nickname'],item['text'],item['timeline'],item['vip'],item['svip'],item['isadmin'],item['guard_level'],0,'medal']
                insert(value)

    global timer
    timer = threading.Timer(1, Crawling)#利用定时器外加一个线程,在Tkinter中循环执行该函数
    timer.start()


"""绘制热点词云图"""
import jieba#jieba分词用的库
from wordcloud import WordCloud##制作词云用的库
import matplotlib.pyplot as plt#matplotlib是python上的一个2D 绘图库，提供一个类似matlab的绘图框架
from  imageio  import imread#读写图像
import os
def wordmap():
    # 建立数据库连接
    db = pymysql.connect(host='localhost',port=3306,user=user,passwd=passwd,database=database,charset='utf8',connect_timeout=10)

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    if  stopwords_var.get()=='':
        sql = "SELECT TEXT FROM `%s`" % tables_var.get()
    else:
        sql = "SELECT TEXT FROM `%s` WHERE TEXT NOT REGEXP '%s' " % (tables_var.get(), stopwords_var.get()) #将mysql指定表的数据导入
    #执行SQL查询
    cursor.execute(sql)


    """获取全部匹配数据"""
    Danmu_text = cursor.fetchall()
    contents = ' '
    for s in Danmu_text:
        contents+=s[0]
    result = " ".join(jieba.lcut(contents)) #jieba模块将字符串分词
    print(result)  # 每个字符串空一格
    color_mask = imread('大象.jpg')  # 建议图片背景颜色为白色
    wordcloud = WordCloud(
    font_path=r"C:\Windows\Fonts\STZHONGS.TTF",  # 不是所有的字体都可以，楷体没问题
    background_color="white",
    width=1080,
    mask=color_mask,
    height=960)

    """制作词云"""
    wordcloud.generate(result)  # 加载文本
    wordcloud.to_file("cy.png")  # 保存图片
    plt.imshow(wordcloud)  # 背景图片
    plt.show()
    os.system('cy.png')
    # 关闭数据库连接
    db.close()


"""弹幕数、用户数-时间曲线图"""
from pyecharts import options as opts
from pyecharts.charts import Line
from pyecharts.globals import ThemeType
import pymysql
import webbrowser

def text_time():
    # 建立数据库连接
    db = pymysql.connect(host='localhost',port=3306,user=user,passwd=passwd,database=database,charset='utf8',connect_timeout=10)

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    sql = "SELECT TIMELINE FROM `%s`" %(ShowTables_list.get(ShowTables_list.curselection())) #将mysql指定表的数据导入
    # 执行SQL查询
    cursor.execute(sql)

    """获取全部匹配数据"""
    data = cursor.fetchall()
    timeline = []
    minute = []
    for s in data:
        timeline.append(str(s[0]))

    for i in range(len(timeline)):
        minute.append(timeline[i][11:16])  # 2020-05-21 21:48:19

    dicte = {}
    for key in minute:
        dicte[key] = dicte.get(key, 0) + 1

    timeline_list = []
    text_list = []
    # uid_list=[]

    timeline_list = list(dicte.keys())
    text_list = list(dicte.values())

    line = (
        Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
            .add_xaxis(timeline_list)  # 横轴为时间
            .add_yaxis('弹幕量', text_list,
                       markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_='max')]), #标记峰值
                       markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_='average')]),#标记平均值
                      )  # 纵轴一弹幕数量
            # .add_yaxis('用户', uid_list)      # 纵轴二用户数量
            .set_global_opts(
            title_opts=opts.TitleOpts(title='弹幕-时间图', subtitle="折线图"),  # 图表名称
            xaxis_opts=opts.AxisOpts(name='时间'),  # 设置x轴名字属性
            tooltip_opts=opts.TooltipOpts(trigger='axis', axis_pointer_type='cross'),  #提示框组件配置
            toolbox_opts=opts.ToolboxOpts(is_show=True, orient='vertical', pos_left='right'), #工具栏组件配置
        )

    )

    # line.render_notebook()
    line.render('弹幕-时间图.html')  # 输出为html
    webbrowser.open("弹幕-时间图.html")   #调用默认浏览器打开
    # 关闭数据库连接
    db.close()


"""定时器"""
timer = threading.Timer(1, Crawling)
timer.start()

"""窗口主体"""
root = tk.Tk()
root.title("弹幕小助手")
root.geometry("760x620")


"""输入文本框"""
def inputint():
    global Roomid
    global dat
    try:
        Roomid = int(InputRid_var.get())
        dat['roomid'] = Roomid
    except:
            InputRid_var.set('Not a valid integer.')

InputRid_label = tk.Label(root, text = '请输入要爬取的B站直播房间号', anchor = tk.CENTER, 
                        font = ("Arial", 10) )
InputRid_label.pack()

InputRid_var = tk.StringVar()
InputRid_Entry = tk.Entry(root, textvariable=InputRid_var)
InputRid_Entry.pack()

btn1 = tk.Button(root, text='检验输入的房间号并确定', command=inputint)
btn1.pack()

"""开始爬取按钮"""
def StartCrawling():
    global start_sign
    global button
    global Roomid
    global start_info
    if button == True:
        start_sign=False
        start_info.set("开始爬取")
        create(Roomid)
        DeleteTable(Roomid)
        button = False
    else:
        start_sign=True
        start_info.set("终止爬取")
        create_temp(Roomid)
        button = True

start_info = tk.StringVar()
start_info.set("开始爬取")
start_button = tk.Button(root, textvariable = start_info, font = 20, 
                          width = 8, command = StartCrawling)
start_button.pack()

"""显示已有表单且可以选择房间号"""
ShowTables_label = tk.Label(root, text = '显示已有表单，点击可以选定进行操作', anchor = tk.CENTER, 
                        font = ("Arial", 10) )
ShowTables_label.pack()

ShowTables_var = tk.StringVar()
ShowTables_list= tk.Listbox(root,listvariable=ShowTables_var)
ShowTables_list.pack()

"""表单输入框"""
tables_var = tk.StringVar()
tables_Entry = tk.Entry(root, textvariable=tables_var)
tables_Entry.pack()

"""词云图按键"""
wordmap_button = tk.Button(root, text="热词云图", font=20, command=wordmap)
wordmap_button.pack()

"""曲线图按键"""
text_time_button = tk.Button(root, text="弹幕时间图全体查询", font=20, command=text_time)
text_time_button.pack()

"""删除记录所用按钮"""
DeleteSelectedTable_button = tk.Button(root, text = "删除选定表单", font = 20, 
                           command = DeleteSelectedTable)
DeleteSelectedTable_button.pack()

"""过滤所需的输入文本框"""
stopwords_label = tk.Label(root, text = '屏蔽包含关键词的弹幕，请用|分隔屏蔽词', anchor = tk.CENTER,
                        font = ("Arial", 10) )
stopwords_label.pack()

stopwords_var = tk.StringVar()
stopwords_Entry = tk.Entry(root, textvariable=stopwords_var)
stopwords_Entry.pack()

"""关键词时间曲线图"""
def keywords_time():
    # 建立数据库连接
    db = pymysql.connect(host='localhost',port=3306,user=user,passwd=passwd,database=database,charset='utf8',connect_timeout=10)

    # 使用cursor()方法获取操作游标

    key_words= keywords_var.get()
    print(key_words)
    cursor = db.cursor()
    if level_var.get()== '':
        level = 0
    else:
        level = int(level_var.get())


    #sql = "SELECT TIMELINE FROM `%s` WHERE TEXT REGEXP '%s' " %(tables_var.get(),key_words) #将mysql指定表的数据导入
    if  keywords_var.get()=='':
        if stopwords_var.get() == '':
            sql="SELECT TIMELINE FROM `%s`  where MEDALLEVEL >= %d" % (tables_var.get(), level)
        else:
            sql = "SELECT TIMELINE FROM (SELECT * FROM `%s` WHERE TEXT  NOT REGEXP '%s')as t where t.MEDALLEVEL >= %d" % (tables_var.get(), stopwords_var.get(), level)
    else:
        if stopwords_var.get() == '':
            sql = "SELECT TIMELINE FROM (SELECT * FROM `%s` WHERE TEXT  REGEXP '%s')as t where t.MEDALLEVEL >= %d" % (tables_var.get(), keywords_var.get(), level)
        else:
            sql = "SELECT TIMELINE FROM (SELECT * FROM `%s` WHERE TEXT  NOT REGEXP '%s')as t where t.TEXT REGEXP '%s' AND t.MEDALLEVEL >= %d" % (tables_var.get(), stopwords_var.get(), keywords_var.get(),level)

    # 执行SQL查询
    cursor.execute(sql)

    """获取全部匹配数据"""
    data = cursor.fetchall()
    timeline = []
    minute = []
    for s in data:
        timeline.append(str(s[0]))

    for i in range(len(timeline)):
        minute.append(timeline[i][11:16])  # 2020-05-21 21:48:19

    dicte = {}
    for key in minute:
        dicte[key] = dicte.get(key, 0) + 1

    timeline_list = []
    text_list = []

    timeline_list = list(dicte.keys())
    text_list = list(dicte.values())

    line = (
        Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
            .add_xaxis(timeline_list)  # 横轴为时间
            .add_yaxis('keywords', text_list,
                       markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_='max')]), #标记峰值
                       markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_='average')]),#标记平均值
                      )  # 纵轴一弹幕数量
            # .add_yaxis('用户', uid_list)      # 纵轴二用户数量
            .set_global_opts(
            title_opts=opts.TitleOpts(title='高级弹幕-时间图', subtitle="折线图"),  # 图表名称
            xaxis_opts=opts.AxisOpts(name='时间'),  # 设置x轴名字属性
            tooltip_opts=opts.TooltipOpts(trigger='axis', axis_pointer_type='cross'),  #提示框组件配置
            toolbox_opts=opts.ToolboxOpts(is_show=True, orient='vertical', pos_left='right'), #工具栏组件配置
        )

    )

    line.render('高级弹幕-时间图.html')  # 输出为html
    webbrowser.open("高级弹幕-时间图.html")   #调用默认浏览器打开
    # 关闭数据库连接
    db.close()

"""关键词所用输入文本框和按钮"""
keywords_label = tk.Label(root, text = '检索包含关键词的弹幕，请用|分割关键词', anchor = tk.CENTER, 
                        font = ("Arial", 10) )
keywords_label.pack()

keywords_var = tk.StringVar()
keywords_Entry = tk.Entry(root, textvariable=keywords_var)
keywords_Entry.pack()



"""等级所需的输入文本框"""
level_label = tk.Label(root, text = '请输入用户等级', anchor = tk.CENTER,
                        font = ("Arial", 10) )
level_label.pack()
level_var = tk.StringVar()
level_var.set('')
level_Entry = tk.Entry(root, textvariable=level_var)
level_Entry.pack()

""""""
keywords_button = tk.Button(root, text="弹幕时间图高级查询", font=20,
                                command=keywords_time)
keywords_button.pack()
"""窗口循环"""
root.mainloop()
