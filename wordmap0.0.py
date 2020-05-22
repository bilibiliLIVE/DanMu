"""引入模块"""
#百度搜索方法 ： 某某某的用法（空一格） python
import requests#引入requests请求模块
from bs4 import BeautifulSoup#从bs4模块中引入BeautifulSoup模块，最主要的功能是从网页抓取数据。
import pandas as pd#pandas是专门为处理表格和混杂数据设计的,清洗数据
import datetime#时间模块datetime是python内置模块，datetime是Python处理日期和时间的标准库。
import re#Python 的 re 模块（Regular Expression 正则表达式）提供各种正则表达式的匹配操作，在文本解析、复杂字符串分析和信息提取时是一个非常有用的工具
import jieba#jieba分词用的库
from wordcloud import WordCloud##制作词云用的库
import matplotlib.pyplot as plt#matplotlib是python上的一个2D 绘图库，提供一个类似matlab的绘图框架
from  imageio  import imread#读写图像

"""开始爬数据"""
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
}#模仿浏览器向对方服务器发送一个请求
url = 'http://comment.bilibili.com/121511739.xml'#浏览路径
response = requests.get(url=url, headers=header)  # 向对方服务器发送请求
response.encoding = response.apparent_encoding  # 设置字符编码（万能模式）。不确定是utf-8，这么写万无一失
data = response.text  # 获取文本
soup = BeautifulSoup(data, 'lxml')  # pip install lxml  解析
d_list = soup.find_all('d')  # 获取所有的d标签
dlst = []
for d in d_list:  # 循环拿出所有的d标签
    danmu = {}
    danmu['弹幕'] = d.text  # 获取文本信息
    #danmu['时间'] = datetime.datetime.now()
    # danmu['路径'] = url
    dlst.append(danmu)
df = pd.DataFrame(dlst)  # 转换成二维数组，类似于execl表格


f = open('sign.txt', 'w', encoding='utf-8')  # 打开文件，新建文件sign.txt，'w'写入内容
for i in df['弹幕'].values:  # 循环所有的文本信息
    pat = re.compile(r'[一-龥]+')  # 定义过滤数据的规则，所有的汉字
    filter_data = re.findall(pattern=pat, string=i)  # 执行过滤操作
    f.write("".join(filter_data))  # 写入文本
f.close()



"""制作词云的步骤二：使用jieba模块对词文件sign.txt进行分词"""
with open(r"D:\p.y\sign.txt", encoding="utf-8") as file_object:
    contents = file_object.read()
    result = " ".join(jieba.lcut(contents))
print(result)#每个字符串空一格


color_mask = imread('大象.jpg')#建议图片背景颜色为白色
wordcloud = WordCloud(
    font_path=r"C:\Windows\Fonts\STZHONGS.TTF",#不是所有的字体都可以，楷体没问题
    background_color="white",
    width=1080,
    mask=color_mask,
    height = 960)

"""制作词云的步骤三：制作词云"""
wordcloud.generate(result)#加载文本
wordcloud.to_file("cy.png")#保存图片
plt.imshow(wordcloud)#背景图片
plt.show()
