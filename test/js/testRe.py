#@Author 滕海怡
# 正则表达式 字符串模式（判断字符串是否符合一定的标准）
import re

# 创建模式对象
# 此处的AA是正则表达式，用来匹配验证其他的字符串
# pat = re.compile("AA")
# # search中的字符串是被校验的内容
# m = pat.search("ABCAAsjdlfskjdlAA")
# print(m)

# m = re.search("AB","fjslAB")
# print(m)
# m = re.findall("[a-z]+","asjABCdkjajsldja")
# print(m)

# sub应用
m = re.sub("a","A","abcdefga")
print(m)
