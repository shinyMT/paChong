import sqlite3

# 打开或创建数据库文件
conn = sqlite3.connect("test.db")
print("open database successfully")
# 获取数据库的游标
c = conn.cursor()
# 书写sql语句
# sql = '''
#     create table company
#     (
#         id int primary key not null ,
#         name text not null ,
#         age int not null,
#         address char(50),
#         salary real
#     );
# '''
# 插入数据
# sql = '''
#     insert into company values (1,'zhangsan',21,'朝阳区',50000)
# '''
# # 查询数据
sql = '''
    select * from company
'''
# 执行sql语句
result = c.execute(sql)
for row in result:
    print('id = {}'.format(row[0]))
    print('name = {}'.format(row[1]))
    print('salary = {}'.format(row[4]))
    pass
# 提交数据操作
# conn.commit()
# 关闭数据库连接
conn.close()