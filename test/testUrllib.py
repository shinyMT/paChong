import urllib.request
import urllib.parse

# 获取一个get请求
# response = urllib.request.urlopen('http://www.baidu.com')
# print(response.read().decode('utf-8'))

# 获取一个Post请求
# data = bytes(urllib.parse.urlencode({"hello":"world"}),encoding='utf-8')
# response = urllib.request.urlopen("http://httpbin.org/post",data=data)
# print(response.read().decode('utf-8'))

# try:
#     response = urllib.request.urlopen('http://www.baidu.com',timeout=0.01)
#     print(response.read().decode('utf-8'))
#     pass
# except urllib.error.URLError as msg:
#     print("time out !")
#     pass
# response = urllib.request.urlopen('http://www.baidu.com')
# print(response.status)

# 模拟浏览器
url = 'https://douban.com'
headers = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
}
req = urllib.request.Request(url=url,headers=headers,method="GET")
response = urllib.request.urlopen(req)
print(response.read().decode('utf-8'))
