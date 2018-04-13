日常写代码时候会遇到一些字符串替换的操作，比如把一大堆"驼峰"形式的字符串批量转换成下划线形式。"驼峰"形式的变量命名风格在Java中很常见，而下划线形式的变量命名风格在C、Python等语言的代码中更常见一些，两者没有严格的好坏区分。本文就用"驼峰"和"下划线"相互转换的实例，讲解一下Python的`re`模块`sub`函数的强大功能。

# 什么是"驼峰"和"下划线"风格的字符串

变量名、函数名等标识符的多个单词之间用下划线隔开，这样的字符串就是下划线风格的字符串，比如：

```
person_info
ipv6_address
book_id
get_tomorrow_weather()
```

而驼峰风格的字符串就是不同单词之间用大写字母进行分隔，比如：

```
personInfo
ipv6Address
bookId
getTomorrowWeather()
```

# re.sub函数

`re.sub`函数是Python内置的re模块的一个字符串替换函数，支持正则替换。函数文档如下：

```
help(re.sub)
Help on function sub in module re:
sub(pattern, repl, string, count=0, flags=0)
    Return the string obtained by replacing the leftmost
    non-overlapping occurrences of the pattern in string by the
    replacement repl.  repl can be either a string or a callable;
    if a string, backslash escapes in it are processed.  If it is
    a callable, it's passed the match object and must return
    a replacement string to be used.
```

`re.sub`函数的函数原型为：`sub(pattern, repl, string, count=0, flags=0)`

下面简单介绍一下每个参数的含义：

* `pattern`：是一个正则表达式，匹配要替换的子串。

* `repl`：可以是一个字符串，支持对pattern中分组的后向引用。注意到文档的最后一句话：

> If it is a callable, it's passed the match object and must return a replacement string to be used.

可见，`repl`也可以是一个`callable`对象（函数），这个函数的入参为pattern正则匹配到的对象，返回值为一个字符串，表示要替换成的字符串。

注：正则的分组及后向引用详见：[python正则表达式系列（4）——分组和后向引用](http://www.jianshu.com/p/5ce8100d30a0)

* `string`：要进行替换操作的字符串。

* `count`：要替换掉多少个子串（按从左到右的顺序），默认值为0，表示替换能被pattern匹配到的所有子串。

* `flags`：正则内置属性，默认值为0，表示不使用任何内置属性。

注：正则内置属性的用法详见：[python正则表达式系列（3）——正则内置属性](http://www.jianshu.com/p/e4a7cf3737d6)

# "驼峰"和"下划线"字符串之间的相互转换

通过对`re.sub`函数的深入了解，现在应该可以轻松写出"驼峰"和"下划线"字符串相互转换的代码了。直接上代码：

```python
# coding:utf-8
import re

def hump2underline(hunp_str):
    '''
    驼峰形式字符串转成下划线形式
    :param hunp_str: 驼峰形式字符串
    :return: 字母全小写的下划线形式字符串
    '''
    # 匹配正则，匹配小写字母和大写字母的分界位置
    p = re.compile(r'([a-z]|\d)([A-Z])')
    # 这里第二个参数使用了正则分组的后向引用
    sub = re.sub(p, r'\1_\2', hunp_str).lower()
    return sub

def underline2hump(underline_str):
    '''
    下划线形式字符串转成驼峰形式
    :param underline_str: 下划线形式字符串
    :return: 驼峰形式字符串
    '''
    # 这里re.sub()函数第二个替换参数用到了一个匿名回调函数，回调函数的参数x为一个匹配对象，返回值为一个处理后的字符串
    sub = re.sub(r'(_\w)',lambda x:x.group(1)[1].upper(),underline_str)
    return sub
```

代码中已经有详细的注释，还是比较好理解的。下面对这两个函数进行测试：

```python
def test_hump2underline():
    # 供测试用的一些驼峰形式的字符串
    attr1 = 'PersonNamePattern'
    attr2 = 'IPv6Address'
    attr3 = 'personDetailInfo'
    attr4 = 'CCTV'
    attr5 = 'CCTVAddress'
    attr6 = 'name'
    attrs = [attr1,attr2,attr3,attr4,attr5,attr6]

    # 遍历attrs进行匹配和转换，把驼峰形式的字符串转成下划线形式
    for attr in attrs:
        sub = hump2underline(attr)
        print sub

    # 输出：
    '''
    person_name_pattern
    ipv6_address
    person_detail_info
    cctv
    cctvaddress
    name
    '''

def test_underline2hump():
    attr1 = 'person_name_pattern'
    attr2 = 'ipv6_address'
    attr3 = 'person_detail_info'
    attr4 = 'cctv'
    attr5 = 'cctvaddress'
    attr6 = 'name'
    attrs = [attr1, attr2, attr3, attr4, attr5, attr6]

    for attr in attrs:
        sub = underline2hump(attr)
        print sub

    # 输出：
    '''
    personNamePattern
    ipv6Address
    personDetailInfo
    cctv
    cctvaddress
    name
    '''
```

# JSON字符串字段名的"驼峰"转"下划线"

JSON是一种非常通用、轻量型的数据交换格式，与Python中的字典、Java中的Map具有相同的结构。JSON中的字段名一般需要写成下划线的形式，但是有时候也会遇到字段名是"驼峰"形式的JSON文本，那么如何把一个JSON字符串中的所有字段名都从驼峰形式替换成下划线形式呢？

因为考虑到json可能具有多层嵌套的复杂结构，所以下面直接采用正则文本替换的方式进行处理，而不是采用把JSON字符串转成字典再进行处理。

上代码：

```python
def json_hump2underline(hump_json_str):
    '''
    把一个json字符串中的所有字段名都从驼峰形式替换成下划线形式。
    注意点：因为考虑到json可能具有多层嵌套的复杂结构，所以这里直接采用正则文本替换的方式进行处理，而不是采用把json转成字典再进行处理的方式
    :param hump_json_str: 字段名为驼峰形式的json字符串
    :return: 字段名为下划线形式的json字符串
    '''
    # 从json字符串中匹配字段名的正则
    # 注：这里的字段名只考虑由英文字母、数字、下划线组成
    attr_ptn = re.compile(r'"\s*(\w+)\s*"\s*:')

    # 使用hump2underline函数作为re.sub函数第二个参数的回调函数
    sub = re.sub(attr_ptn,lambda x : '"' + hump2underline(x.group(1)) + '" :',hump_json_str)
    return sub
```

对上面这个函数进行测试：

```python
def test_json_hump2underline():
    # 待测试json字符串
    json_str = '''
    {
        "englishName":"Tom",
        "age":18,
        "detailInfoTable": {
            "address":"USA",
            "sportsHobby": ["Basketball","Football","Swimming"],
            "contactList":{
                "tel" : "1234567",
                "emailAddress":"tom@test.com"
            }
        },
        "gender":"male"
    }
    '''
    print json_hump2underline(json_str)

    # 输出：
    '''
    {
        "english_name" :"Tom",
        "age" :18,
        "detail_info_table" : {
            "address" :"USA",
            "sports_hobby" : ["Basketball","Football","Swimming"],
            "contact_list" :{
                "tel" : "1234567",
                "email_address" :"tom@test.com"
            }
        },
        "gender" :"male"
    }
    '''
```

# 总结

经过以上实例可以看出，`re.sub`函数因为支持了正则替换及回调函数替换，在处理复杂文本替换需求时具有强大的优势，再一次展现了Python在文本处理领域功能强大又简单、易用的特点。
