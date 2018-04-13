> 本文讲述的核心库：`xlsxwriter`
> 参考：《python自动化运维：技术与最佳实践》
 更多用法参考xlsxwriter官方文档：http://xlsxwriter.readthedocs.io/

本文主要总结一下如何使用xlsxwriter模块来自动化生成和处理Excel文档。

# 简单用法demo


```python
# !/usr/bin/python
# coding:utf-8
# xlsxwriter的基本用法
import xlsxwriter

# 1. 创建一个Excel文件
workbook = xlsxwriter.Workbook('demo1.xlsx')

# 2. 创建一个工作表sheet对象
worksheet = workbook.add_worksheet()

# 3. 设定第一列（A）宽度为20像素
worksheet.set_column('A:A',20)

# 4. 定义一个加粗的格式对象
bold = workbook.add_format({'bold':True})

# 5. 向单元格写入数据
# 5.1 向A1单元格写入'Hello'
worksheet.write('A1','Hello')
# 5.2 向A2单元格写入'World'并使用bold加粗格式
worksheet.write('A2','World',bold)
# 5.3 向B2单元格写入中文并使用加粗格式
worksheet.write('B2',u'中文字符',bold)

# 5.4 用行列表示法（行列索引都从0开始）向第2行、第0列（即A3单元格）和第3行、第0列（即A4单元格）写入数字
worksheet.write(2,0,10)
worksheet.write(3,0,20)

# 5.5 求A3、A4单元格的和并写入A5单元格，由此可见可以直接使用公式
worksheet.write(4,0,'=SUM(A3:A4)')

# 5.6 在B5单元格插入图片
worksheet.insert_image('B5','./demo.png')

# 5.7 关闭并保存文件
workbook.close()
```
运行之后生成的Excel文档效果如下：
![](http://upload-images.jianshu.io/upload_images/8819542-a53e8cb4fdab0cc9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


# 综合实例demo：绘制网站业务流量数据图表


```python
#!/usr/bin/python
# coding:utf-8
import xlsxwriter

# 创建一个Excel文件
workbook = xlsxwriter.Workbook('chart.xlsx')
# 创建一个工作表sheet对象，使用默认名称："Sheet1"
worksheet = workbook.add_worksheet()
# 创建一个图表对象
chart = workbook.add_chart({'type':'column'})

# 定义数据表头
title = [u'业务名称',u'星期一',u'星期二',u'星期三',u'星期四',u'星期五',u'星期六',u'星期日',u'平均流量']
# 定义业务名称列表
buname = [u'业务官网',u'新闻中心',u'购物频道',u'体育频道',u'亲子频道']
# 定义5个频道一周七天的数据列表
data = [
    [150,152,158,149,155,145,148],
    [89,88,95,93,98,100,99],
    [201,200,198,175,170,198,195],
    [75,77,78,78,74,70,79],
    [88,85,87,90,93,88,84]
]

# 定义数据formatter格式对象，设置边框加粗1像素
formatter = workbook.add_format()
formatter.set_border(1)
# 定义标题栏格式对象：边框加粗1像素，背景色为灰色，单元格内容居中、加粗
title_formatter = workbook.add_format()
title_formatter.set_border(1)
title_formatter.set_bg_color('#cccccc')
title_formatter.set_align('center')
title_formatter.set_bold()
# 定义平均值栏数据格式对象：边框加粗1像素，数字按2位小数显示
ave_formatter = workbook.add_format()
ave_formatter.set_border(1)
ave_formatter.set_num_format('0.00')

# 定义图表数据系列函数
def chart_series(cur_row):
    chart.add_series({
        'categories':'=Sheet1!$B$1:$H$1',
        'values':'=Sheet1!$B${}:$H${}'.format(cur_row,cur_row),
        'line':{'color':'black'},
        'name':'=Sheet1!$A${}'.format(cur_row)
    })
    # 注：其中categories表示x轴，values表示y轴，line表示线条样式，name表示图例项

# 下面分别以行和列的方式将标题栏、业务名称、流量数据写入单元格，并引用不同的格式对象
worksheet.write_row('A1',title,title_formatter)
worksheet.write_column('A2',buname,formatter)
# 写入第2到第6行的数据，并将第2~6行数据加入图表系列
for i in range(2,7):
    worksheet.write_row('B{}'.format(i),data[i-2],formatter)
    # 计算平均流量栏数据并写入
    worksheet.write_formula('I{}'.format(i),'=AVERAGE(B{}:H{})'.format(i,i),ave_formatter)
    # 将每一行数据加入图表序列
    chart_series(str(i))

# 设置图表大小
chart.set_size({'width':577,'height':287})
# 设置图表大标题
chart.set_title({'name':u'业务流量周报表'})
# 设置y轴小标题
chart.set_y_axis({'name':'Mb/s'})

# 在A8单元格插入图表
worksheet.insert_chart('A8',chart)

# 关闭Excel文档
workbook.close()
```
运行之后生成的Excel文档效果如下：
![](http://upload-images.jianshu.io/upload_images/8819542-ec3a55623df52f25.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
