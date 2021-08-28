# 测试文章解析
from bs4 import BeautifulSoup
import re

# with open('./index.html','rb') as fileObj:
#     html = fileObj.read()
#     # 指定解析的文档和使用的文档解析器
#     bs = BeautifulSoup(html,"html.parser")
#     # print(bs.input.attrs)
#     # print(type(bs.input.attrs))
#     # print(bs.a.string)
#     # print(type(bs.a.string))
#     pass

def name_is_exist(tag):
    return tag.has_attr("name")
    pass

with open('./index.html','rb') as fileObj:
    html = fileObj.read()
    bs = BeautifulSoup(html,"html.parser")
    # 文档的遍历
    # for content in bs.head.contents:
    #     print(content)
    #     pass
    # 文档的搜索
    # 查找所有input标签
    # inputList = bs.find_all("input")
    # print(inputList)
    # 使用search()通过正则表达式匹配内容
    # inputList = bs.find_all(re.compile("i"))
    # print(inputList)
    # inputList = bs.find_all(name_is_exist)
    # print(inputList)
    # tList = bs.find_all(class_=True)
    # for item in tList:
    #     print(item)
    #     pass
    # hList = bs.find_all(href="http://www.baidu.com")
    # print(hList)
    # tList = bs.find_all(text=["hao123","地图","新闻","你好"])
    # tList = bs.find_all("a",limit=2)
    # tList = bs.select("a[class='bri']")
    # for item in tList:
    #     print(item)
    #     pass
    tList = bs.select(".mnv ~ .bri")
    print(tList[0].get_text())
    pass

