本文讲述Python json模块的基本用法。

# 准备工作

```python
import json

# 准备数据：
d = dict(name = 'Tom',age = 18)
json_str = '{"name":"Tom","age":18}'
# 注：json字符串中的引号必须为双引号，若为单引号会转换出错。
```

# json数据类型和python数据类型的对应关系

* {} <——> dict
* [] <——> list
* "string" <——> "str"或u"unicode"
* 123.4 <——> int或float
* true/false <——> True/False
* null <——> None

# 常用方法

### 字典转成json字符串

```python
ret = json.dumps(d)
print ret
print type(ret)
```
输出：
```
    {"age": 18, "name": "Tom"}
    <type 'str'>
```

### json字符串转成字典

```python
ret = json.loads(json_str)
print ret
print type(ret)
```
输出：
```
    {u'age': 18, u'name': u'Tom'}
    <type 'dict'>
```


### 字典转换成json字符串并写入文件

```python
with open('out.txt','w+') as f:
    json.dump(d,f)
```

### 从文件中读取json字符串并转为字典

```python
# 文件(out.txt)内容：{"age": 18, "name": "Tom"}
with open('out.txt','r') as f:
    ret = json.load(f)
    print ret
    print type(ret)
```
输出：
```
    {u'age': 18, u'name': u'Tom'}
    <type 'dict'>
```
### 自定义对象转成json字符串

```python
class Student(object):
    def __init__(self,name,age):
        self.name = name
        self.age = age

s = Student('Tom',18)
print json.dumps(s)
#　输出：
# TypeError: <__main__.Student object at 0x7f7ab808cf10> is not JSON serializable
```
出错原因：Student对象不是一个可序列化为json的对象。

* 解决方法1：写个转换函数

```python
def student2dict(std):
    return {'name':std.name,'age':std.age}
print json.dumps(s,default = student2dict)
```
输出：
```
    {"age": 18, "name": "Tom"}
```

* 解决方法2：传入Student对象内置属性：__dict__

```python
print json.dumps(s,default = lambda obj:obj.__dict__)
```
输出：
```
    {"age": 18, "name": "Tom"}
```

### json字符串转为自定义对象

```python
def dict2student(d):
    return Student(d['name'],d['age'])
ret = json.loads(json_str,object_hook = dict2student)
print ret
print ret.__dict__
print type(ret)
```

    <__main__.Student object at 0x7f7aaa713ad0>
    {'age': 18, 'name': u'Tom'}
    <class '__main__.Student'>


# 补充

### 更好地输出json
```python
json.dumps(json.loads(json_str),indent = 4)  # indent为缩进的字符数
```
输出：
```
    '{\n    "age": 18, \n    "name": "Tom"\n}'
```

### 保持json字符串中属性的顺序

```python
from collections import OrderedDict
data = json.loads(json_str,object_pairs_hook = OrderedDict)
print data
```
输出：
```
    OrderedDict([(u'name', u'Tom'), (u'age', 18)])
```
> 引申：object_pairs_hook是个什么玩意？

这时候就有疑惑了，这个object_pairs_hoo参数是个什么玩意？为什么加上：`object_pairs_hook = OrderedDict`这样一个参数，解析的字典就可以有序了？

为了揭开这个谜团，首先去看看json.loads()函数文档，发现文档中对object_pairs_hook参数的描述是这样的：

```
``object_pairs_hook`` is an optional function that will be called with the
    result of any object literal decoded with an ordered list of pairs.  The
    return value of ``object_pairs_hook`` will be used instead of the ``dict``.
    This feature can be used to implement custom decoders that rely on the
    order that the key and value pairs are decoded (for example,
    collections.OrderedDict will remember the order of insertion). If
    ``object_hook`` is also defined, the ``object_pairs_hook`` takes priority.
```
大致意思就是：object_pairs_hook实际上是一个函数对象（钩子函数），它的入参是json文本的有序键值对的列表（ordered list of pairs），返回值是一个经过自定义处理的值，json.loads()函数的返回值也会是这个钩子函数的返回值。

说了半天估计也没看明白，那就实际写个demo试一把，先看最简单的一个demo：
```python
# coding:utf-8
import json

def deal_with_pairs(pairs):
    '''
    自定义的钩子函数，处理从json文本中解析出的有序键值对列表
    :param pairs: 从json文本中解析出的有序键值对列表
    :return: 自定义的对象
    '''
    return pairs

json_str = '{"a":"111","b":"222"}'
data = json.loads(json_str,object_pairs_hook = deal_with_pairs)
print data
```
输出：
```
[(u'a', u'111'), (u'b', u'222')]
```
可以看出，输出的就是json文本中的有序键值对列表。
下面继续看一个稍微复杂一点的demo：
```python
# coding:utf-8
import json

# 存放json中重复的key列表
duplicate_keys = []

def deal_with_pairs(pairs):
    '''
    自定义的钩子函数，处理从json文本中解析出的有序键值对列表
    :param pairs: 从json文本中解析出的有序键值对列表
    :return: 自定义的对象
    '''
    data = {}
    for k,v in pairs:
        # 如果键已经在data的键中存在了，那么把它添加到duplicate_keys列表
        if k in data:
            duplicate_keys.append(k)
        # 否则添加到data中
        else:
            data[k] = v

    return data

json_str = '{"a":"111","b":"222","a":"345"}'
data = json.loads(json_str,object_pairs_hook = deal_with_pairs)
print data
print duplicate_keys
```
输出：
```
{u'a': u'111', u'b': u'222'}
[u'a']
```
可以看出，上面这个程序的作用就是找出了json文本中有哪些键是重复的。
最后再来一个嵌套的有重复key的json字符串，来看看效果：
```python
# coding:utf-8
import json
# 存放json中重复的key列表
duplicate_keys = []

def deal_with_pairs(pairs):
    '''
    自定义的钩子函数，处理从json文本中解析出的有序键值对列表
    :param pairs: 从json文本中解析出的有序键值对列表
    :return: 自定义的对象
    '''
    print 'pairs is: {0}'.format(pairs)
    data = {}
    for k,v in pairs:
        # 如果键已经在data的键中存在了，那么把它添加到duplicate_keys列表
        if k in data:
            duplicate_keys.append(k)
        # 否则添加到data中
        else:
            data[k] = v

    return data

json_str = '{"a":"111","b":{"b1":"b111","b2":"b222","b1":"b123"},"a":"345"}'
data = json.loads(json_str,object_pairs_hook = deal_with_pairs)
print data
print duplicate_keys
```
输出：
```
pairs is: [(u'b1', u'b111'), (u'b2', u'b222'), (u'b1', u'b123')]
pairs is: [(u'a', u'111'), (u'b', {u'b1': u'b111', u'b2': u'b222'}), (u'a', u'345')]
{u'a': u'111', u'b': {u'b1': u'b111', u'b2': u'b222'}}
[u'b1', u'a']
```
可以看出这里输出了两个pairs列表，第一个是内层的子json的键值对列表，第二个是外层的json键值对列表。最终查找出来的重复的键有：'b1'和'a'，和我们的预期相符。
