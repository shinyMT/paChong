#-*- coding = utf-8 -*-
# 引入模块
import sys
from bs4 import BeautifulSoup
import re
import urllib.request,urllib.error
import xlwt
import sqlite3

# 创建一个正则表达式对象，表示规则
# 匹配存放电影链接的标签，因为都是用a标签存放，所以都会以 <a href="xxx">的形式出现
# .*?是万能匹配，即其中是什么内容都可以
findLink = re.compile(r'<a href="(.*?)">')
findImg = re.compile(r'<img.* src="(.*?)" ',re.S)
findTitle = re.compile(r'<span class="title">(.*?)</span>',re.S)
findStar = re.compile(r'<span class="rating_num".*>(.*?)</span>')
findJudge = re.compile(r'<span>(\d*)人评价</span>')
findInq = re.compile(r'<span class="inq">(.*?)</span>')
findInfo = re.compile(r'<p class="">(.*?)</p>',re.S)

def getData(baseurl):
    '''
    爬取网页，并逐一解析数据
    :param baseurl:基础url，不带参数
    :return: 返回数据列表
    '''
    # 存取所有电影
    dataList = []
    # 调用获取页面新的函数，10次
    for i in range(0,10):
        url = baseurl + str(i*25)
        # 保存获取到的网页源码
        html = askUrl(url)

        # 解析获取到的网页源码
        soup = BeautifulSoup(html, "html.parser")
        # 逐一地解析数据
        # 根据网页源码，找到class=item的div
        for item in soup.find_all('div', class_="item"):
            # print(item)
            # 保存一部电影的所有信息
            movieList = []
            # 将html节点全部转换成字符串
            item = str(item)
            # 存放电影的链接地址，因为会以列表形式返回，所以[0]是提取出列表中的第一个元素即链接
            link = re.findall(findLink, item)[0]
            movieList.append(link)
            # 存放影片的图片链接地址
            img = re.findall(findImg, item)[0]
            # 将值追加到列表中
            movieList.append(img)
            # 存放影片片名
            titles = re.findall(findTitle, item)
            if len(titles) == 2:
                # 中文片名
                ctitle = titles[0]
                movieList.append(ctitle)
                # 英文片名，并去掉无关的/符号
                etitle = titles[1].replace(u"\xa0", " ")
                movieList.append(etitle)
                pass
            else:
                movieList.append(titles[0])
                # 英文名为空的情况下就留一个占位符
                movieList.append(' ')
                pass
            # 存放影片评分
            star = re.findall(findStar, item)[0]
            movieList.append(star)
            # 存放影片的评价次数
            judge = re.findall(findJudge, item)[0]
            movieList.append(judge)
            # 存放影片概况
            inq = re.findall(findInq, item)
            # 如果有概况就存，没有的话就留个空位占位
            if len(inq) != 0:
                movieList.append(inq)
                pass
            else:
                movieList.append(' ')
                pass
            # print(inq)
            # 存放影片的导演等信息
            info = re.findall(findInfo, item)[0].replace(u"\xa0", " ")
            # 把br后的一个或多个空格和tab都替换成空
            infoNew = re.sub('<br/>(\s+)?', ' ', info)
            # 追加到列表并去除前后空格
            movieList.append(infoNew.strip())
            # print(info)
            # 将处理好的一部电影信息放到dataList中
            dataList.append(movieList)
            # print(dataList)
            pass
        pass

    return dataList
    pass

def saveData(savePath,dataList):
    '''
    保存数据
    :param savePath: 数据的保存路径
    :return:
    '''
    # 创建excel对象
    book = xlwt.Workbook(encoding='utf-8')
    # 创建表单对象
    sheet = book.add_sheet('豆瓣电影Top250')
    # 设置表单中的列名
    col = ("电影链接","图片链接","影片中文名","影片英文名","评分","评价数","概况","演员信息")

    # 向表单中写入列名
    for i in range(0,8):
        # 写入列名
        sheet.write(0,i,col[i])
        pass
    # 向列表中写入内容
    for i in range(0,250):
        print('这是第{}条数据'.format(i))
        # 取出一部电影的数据
        data = dataList[i]
        for j in range(0,8):
            sheet.write(i+1,j,data[j])
            pass
        pass
    # 保存表单
    book.save(savePath)
    pass

def initDB(dbPath):
    '''
    创建数据库函数
    :return:
    '''
    # 创建数据库连接
    conn = sqlite3.connect(dbPath)
    # 获取数据库的游标
    cusor = conn.cursor()
    # 书写sql语句
    sql = '''
        create table movie250
        (
            id integer primary key autoincrement,
            movie_link text,
            pic_link text,
            chinese_name varchar ,
            foreign_name varchar ,
            star numeric ,
            judge numeric ,
            introduction text,
            info text
        );
    '''
    # 执行sql语句
    cusor.execute(sql)
    # 提交数据库操作
    conn.commit()
    # 关闭数据库连接
    conn.close()
    pass

def saveData2DB(dbPath,dataList):
    '''
    将数据保存到sqlite3数据库中
    :param dbPath: 数据库路径
    :param dataList: 所有的电影信息
    '''
    # 初始化数据库
    initDB(dbPath)
    # 创建数据库连接
    conn = sqlite3.connect(dbPath)
    # 获取数据库的游标
    cursor = conn.cursor()
    # 读取dataList的内容，将信息添加到数据库中
    for data in dataList:
        # 给每列的数据值添加格式，例如字符串添加双引号
        for i in range(len(data)):
            if i==4 or i ==5:
                # 如果是评分和评价人数，则不加引号，进行下一次循环
                continue
                pass
            # 单引号是为了将双引号和值拼接起来
            data[i] = '"'+str(data[i])+'"'
            pass
        # 插入数据，值用%s进行占位，值之间用逗号进行分割,join后的循环是因为概况是以列表存储的而不是直接的字符串
        sql = '''
                insert into movie250 (
                movie_link,pic_link,chinese_name,foreign_name,star,judge,introduction,info) 
                values (%s)
        ''' % ",".join('%s' % a for a in data)
        # print(sql)
        # 执行sql语句
        cursor.execute(sql)
        # 提交数据库操作
        conn.commit()
        pass
    # 关闭数据库连接
    cursor.close()
    conn.close()
    pass

def askUrl(url):
    '''
    得到指定某个URL的网页内容
    :return:返回网页结构
    '''
    # 添加浏览器的header信息，伪装成浏览器
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
    }
    req = urllib.request.Request(url,headers=head)
    try:
        # 发送请求
        response = urllib.request.urlopen(req)
        # 读取响应的内容
        html = response.read().decode('utf-8')
        # print(html)
        pass
    except urllib.error.URLError as msg:
        # 打印异常的状态码和原因
        if hasattr(msg,"code"):
            print(msg.code)
            pass
        if hasattr(msg,"reason"):
            print(msg.reason)
            pass
        pass
    return html
    pass

def main():
    baseUrl = 'https://movie.douban.com/top250?start='
    # 1. 爬取网页并解析数据
    dataList = getData(baseUrl)
    askUrl(baseUrl)
    # 2. 保存数据----保存到Excel
    # 设置保存路径为当前目录下的xls文件
    # savePath = '豆瓣电影Top250.xls'
    # saveData(savePath, dataList)
    # 保存数据-----保存到数据库
    # 设置保存到数据库的路径
    dbPath = 'movie.db'
    saveData2DB(dbPath,dataList)

    pass

if __name__ == '__main__':
    # 调用函数
    main()
    pass