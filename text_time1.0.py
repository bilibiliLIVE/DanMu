# -*- coding: utf-8 -*-
"""
Created on Wed Ma

@author: HP
"""

"""弹幕数-时间曲线图"""

from pyecharts import options as opts
from pyecharts.charts import Line
from pyecharts.globals import ThemeType
import pymysql
import webbrowser
#  timeline_list= [1,2,3,4,5,6,7,8,9,10,11,12]
#  text_list = [5,10,26,30,35,30,20,26,40,46,40,50]
#  uid_list = [8,20,24,36,40,36,40,45,50,53,48,58]

def uid_text_time():

    # 建立数据库连接
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='qzw3066906793', database='BiliBiliDanMu', charset='utf8',connect_timeout=10)

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    sql="SELECT TIMELINE FROM `%s`"%(DeleteSelectedTable_var.get())  #将mysql指定表的数据导入
    #执行SQL查询
    cursor.execute(sql)

    """获取全部匹配数据"""
    data = cursor.fetchall()
    timeline=[]
    minute=[]
    for s in data:
        timeline.append(str(s[0]))
        
    for i in range(len(timeline)):
        minute.append(timeline[i][11:16]) #2020-05-21 21:48:19
    
    dicte = {}
    for key in minute:
        dicte[key] = dicte.get(key, 0) + 1
 

    timeline_list=[]
    text_list=[]
    #uid_list=[]   

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
