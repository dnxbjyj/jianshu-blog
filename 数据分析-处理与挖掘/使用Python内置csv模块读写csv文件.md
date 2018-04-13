> 参考资料：[csv模块官方文档](https://docs.python.org/2.7/library/csv.html)

csv文件（`Comma-Separated Values`）是一种以逗号作为分隔符（当然也可以以其他字符作为分隔符）、以行为数据单位的纯文本数据文件，比如像下面这样的一个文件`data.csv`：
```
id,name,age,score
1001,Tom,21,89
1005,Jim,23,100
1002,张三,19,78
1003,Jane,20,93
1004,李四,24,94
```
`data.csv`用Excel也可以打开，打开的效果是这样的：
![](https://upload-images.jianshu.io/upload_images/8819542-2b7140db57354f8d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
发现中文是乱码，那是因为`data.csv`文件的编码格式是utf-8而不是GBK，转为GBK即可在Excel中正常显示中文。

那么在Python代码中怎样读取csv文件呢？又怎样把程序中的数据写入到csv文件中呢？Python自带的csv模块就可以完成这些事情，下面以一个示例来演示一下具体做法。

# 直接上代码
```pyhton
# coding:utf-8
# 读写csv文件
import csv
import sys
from collections import OrderedDict
import json
reload(sys)
sys.setdefaultencoding('utf-8')

def read_csv2dicts(csv_file_path, field_names = None):
    '''
    读取csv文件数据到到字典列表中，支持指定特定的列、指定特定的列顺序读取
    :param csv_file_path: csv文件路径
    :param field_names: 指定的列名列表
    '''
    with open(csv_file_path,'r') as csv_file:
        # 读取csv文件表头列名列表
        header_line = csv_file.readlines()[0]
        headers = header_line.strip().split(',')
    
    # 用二进制格式读取csv文件
    with open(csv_file_path,'rb') as csv_file:
        # 用csv文件对象构建reader对象，reader对象可以看作是多个字典的列表（每行一个字典）
        reader = csv.DictReader(csv_file)
        
        # 行数据列表（每行数据为一个有序字典）
        datas = []
        for row_dict in reader:
            # 行数据JSON字符串
            row_json_str = ''
            # 使用有序字典，保持指定的列顺序
            ordered_row_dict = OrderedDict()
            # 根据指定的列名列表过滤
            if field_names:
                # 把原始行数据字典row_dict中的每个字段的数据按照field_names列表的顺序存入ordered_row_dict字典
                for field in field_names:
                    ordered_row_dict[field] = row_dict[field]
                # 因为csv模块只能正常处理ASCII字符，为了正常处理中文，这里还需要做个utf-8编码转换
                row_json_str = json.dumps(ordered_row_dict).encode('utf-8')
            # 不指定列名的情况，使用csv文件原有表头的列顺序
            else:
                # 指定顺序为原有表头顺序（注：如果不这样处理，csv会自动按照key的字典序进行排序）
                for field in headers:
                    ordered_row_dict[field] = row_dict[field]
                # 因为csv模块只能正常处理ASCII字符，为了正常处理中文，这里还需要做个utf-8编码转换
                row_json_str = json.dumps(ordered_row_dict).encode('utf-8')
            # 把当前行的数据字典对象添加到datas列表，字典保持原有顺序
            datas.append(json.loads(row_json_str,object_pairs_hook = OrderedDict))
        return datas

def write_dicts2csv(dicts,csv_file_path):
    '''
    把数据字典列表写入csv文件
    :param dicts: 数据字典列表
    :param csv_file_path: 要写入的csv文件路径
    '''
    with open(csv_file_path,'wb+') as csv_file:
        # 获取表头列名列表
        headers = dicts[0].keys()
        writer = csv.DictWriter(csv_file,fieldnames = headers)
        # 写入表头
        writer.writeheader()
        # 写入数据行
        writer.writerows(dicts)
        
# 用法示例
def sample():
    # 从csv文件读数据
    datas = read_csv2dicts('./data.csv')
    print json.dumps(datas,indent = 4)
    
    # 写数据到csv文件
    write_dicts2csv(datas,'./new_data.csv')
    
    print 'all finish!'
    
if __name__ == '__main__':
    sample()
```
运行上面代码，输出：
```
[
    {
        "id": "1001",
        "name": "Tom",
        "age": "21",
        "score": "89"
    },
    {
        "id": "1005",
        "name": "Jim",
        "age": "23",
        "score": "100"
    },
    {
        "id": "1002",
        "name": "\u5f20\u4e09",
        "age": "19",
        "score": "78"
    },
    {
        "id": "1003",
        "name": "Jane",
        "age": "20",
        "score": "93"
    },
    {
        "id": "1004",
        "name": "\u674e\u56db",
        "age": "24",
        "score": "94"
    }
]
all finish!
```
并在当前目录下生成了一个名为`new_data.csv`的文件，用notepad++打开该文件，其内容为：
```
id,name,age,score
1001,Tom,21,89
1005,Jim,23,100
1002,张三,19,78
1003,Jane,20,93
1004,李四,24,94
```
可以看到`new_data.csv`文件内容和原来的`data.csv`文件内容完全一样。

# 总结
用csv文件存储数据非常方便，其结构非常简单，对数据的读取和操作仅仅用Python的内置csv模块就可以轻松完成（上面的例子代码可以直接拿去用），而且数据以文件的形式存储，便于保存、读写、传输，是保存大量数据的不错选择。

上述代码已经上传到：[我的GitHub](https://github.com/dnxbjyj/python-basic/blob/master/libs/csv/csv_test.py)
