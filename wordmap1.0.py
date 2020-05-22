# -*- coding: utf-8 -*-
"""
Created on Fri May 22

@author: HP
"""

import jieba#jieba分词用的库
from wordcloud import WordCloud##制作词云用的库
import matplotlib.pyplot as plt#matplotlib是python上的一个2D 绘图库，提供一个类似matlab的绘图框架
from  imageio  import imread#读写图像

def wordmap():
    # 建立数据库连接
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='qzw3066906793', database='BiliBiliDanMu', charset='utf8',connect_timeout=10)

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    sql="SELECT TEXT FROM `%s`"%(DeleteSelectedTable_var.get())  #获取mysql指定表全部弹幕内容
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
    # 关闭数据库连接
    db.close()
