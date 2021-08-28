import xlwt

# 创建workbook对象，相当于一个文件
workbook = xlwt.Workbook(encoding="utf-8")
# 创建工作表，相当于一个表单
worksheet = workbook.add_sheet('sheet1')

row = 9
while row >=1:
    col = 1
    while col <= row:
        print("{} * {} = {}".format(row, col, row * col),end=' ')
        # 写入数据
        worksheet.write(row,col,row*col)
        col = col + 1
    print(" ")
    row = row - 1
    pass
# 保存数据表
workbook.save('student.xls')
