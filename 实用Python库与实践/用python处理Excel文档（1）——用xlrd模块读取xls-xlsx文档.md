> 本文讲述的核心库：`xlrd`

本文主要介绍xlrd模块读取Excel文档的基本用法，并以一个GDP数据的文档为例来进行操作。
# 1. 准备工作：
## 1. 安装xlrd：`pip install xlrd`
## 2. 准备数据集：从网上找到的1952~2012年中国国内GDP的数据，数据结构如下：
![](http://upload-images.jianshu.io/upload_images/8819542-6cf20680d35275af.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


# 2. 目标：将这份数据转换成json格式的数据

# 3. 上代码


```python
#!/usr/bin/python
# coding:utf-8
# 用xlrd读取Excel文件基本用法
import sys
import xlrd
import json

# 设置编码格式
reload(sys)
sys.setdefaultencoding('utf-8')

# 1. 从Excel文件中读取出Book对象
data = xlrd.open_workbook('./gdp_data.xls')
# print type(data)
# 输出：<class 'xlrd.book.Book'>

# 2. 获取sheet页对象
# 2.1 通过sheet索引获取
sheet1 = data.sheet_by_index(0)
# print sheet1
# 输出：<xlrd.sheet.Sheet object at 0x7efc10319ed0>

# 2.2 通过sheet名称获取
sheet2 = data.sheet_by_name(u'Sheet1')
# print sheet2
# 输出：<xlrd.sheet.Sheet object at 0x7efbfb72db10>

# 3. 获取sheet页的行数和列数
nrows = sheet1.nrows
ncols = sheet1.ncols
# print nrows,ncols
# 输出：62 5
# 说明表格有62行、5列

# 4. 获取第0行的值（是一个列表）
row_data = sheet1.row_values(0)
# print row_data
# 输出：[u'year', u'GDP', u'first industry', u'second industry', u'third industry']

# 5. 获取第0列的值（是一个列表）
col_data = sheet1.col_values(0)
# print col_data
# 输出：[u'year', 1952.0, 1953.0, 1954.0, 1955.0,...]

# 6. 使用行列索引（从0开始）获取单元格的数据
cell_A1 = sheet1.cell(0,0)
# print cell_A1
# print type(cell_A1)
# print cell_A1.value
# 输出：
'''
text:u'year'
<class 'xlrd.sheet.Cell'>
year
'''

# 7. 应用：将Excel文件中的数据转换成json数组
# 索引（即表头）
idx = sheet1.row_values(0)
# 最终的数据列表
data = []
# 从第1行开始遍历循环所有行，获取每行的数据
for i in range(1,nrows):
    row_data = sheet1.row_values(i)
    # 组建每一行数据的字典
    row_data_dict = {}
    # 遍历行数据的每一项，赋值进行数据字典
    for j in range(len(row_data)):
        item = row_data[j]
        row_data_dict[idx[j]] = item
        # 将年份字段转成整形
        row_data_dict['year'] = int(row_data_dict['year'])
    # 将行数据字典加入到data列表中
    data.append(row_data_dict)
    
print json.dumps(data,indent = 4)
# 输出：
'''
[
    {
        "GDP": 679.0, 
        "second industry": 141.8, 
        "first industry": 342.9, 
        "third industry": 194.3, 
        "year": 1952
    }, 
    {
        "GDP": 824.0, 
        "second industry": 192.5, 
        "first industry": 378.0, 
        "third industry": 253.5, 
        "year": 1953
    }, 
    {
        "GDP": 859.0, 
        "second industry": 211.7, 
        "first industry": 392.0, 
        "third industry": 255.3, 
        "year": 1954
    }, 
    ...
]
'''
```
