本文主要总结一下python正则的一些内置属性的用法。

# 1. 编译标志：`flags`

首先来看一下`re.findall`函数的函数原型：


```python
import re 
print('【Output】')
print help(re.findall)
```

    【Output】
    Help on function findall in module re:
    
    findall(pattern, string, flags=0)
        Return a list of all non-overlapping matches in the string.
        
        If one or more groups are present in the pattern, return a
        list of groups; this will be a list of tuples if the pattern
        has more than one group.
        
        Empty matches are included in the result.
    
    None


可以看出，`re.findall`函数的最后一个参数是`flags`，默认值是0，这个`falgs`就是编译标志，即正则的内置属性，使用不同的编译标志可以让正则产生不同的匹配效果。那么`falgs`可以取哪些值呢？用`help(re)`来看一下`re`的`DATA`有哪些：


```python
print help(re)

# 【Output】
'''
...
DATA
    DOTALL = 16
    I = 2
    IGNORECASE = 2
    L = 4
    LOCALE = 4
    M = 8
    MULTILINE = 8
    S = 16
    U = 32
    UNICODE = 32
    VERBOSE = 64
    X = 64
...
'''
```

下面试验一下上面的每一种编译标志的作用。

# 2. DOTALL, S

使`.`匹配包括`\n`在内的所有字符（`.`默认是不能匹配`\n`的），举例：


```python
p = r'me.com'
print '【Output】'
print re.findall(p,'me.com')
print re.findall(p,'me\ncom')
print re.findall(p,'me\ncom',re.DOTALL)
print re.findall(p,'me\ncom',re.S)
```

    【Output】
    ['me.com']
    []
    ['me\ncom']
    ['me\ncom']

注：使用`re.S`模式时，正则表达式不能是编译后的正则（`re.compile()`函数），否则会出错。
使用`re.S`模式时，`^`字符变为文档开始符而不再是行开始符，`$`符变为文档结束符而不再是行结束符。

# 3. IGNORECASE, I

使匹配对大小写不敏感，举例：


```python
p = r'a'
print '【Output】'
print re.findall(p,'A')
print re.findall(p,'A',re.IGNORECASE)
print re.findall(p,'A',re.I)
```

    【Output】
    []
    ['A']
    ['A']


# 4. LOCALE, L

本地化匹配，使用了该编译标志后，`\w,\W,\b,\B,\s,\S`等字符的含义就和本地化有关了。

# 5. MULTILINE, M

开启多行匹配，影响`^`和`$`。举例：


```python
s = """
aa bb cc
bb aa
aa ccd
"""
p1 = r'^aa'
p2 = r'cc$'
print '【Output】'
print re.findall(p1,s)
print re.findall(p1,s,re.M)

print re.findall(p2,s)
print re.findall(p2,s,re.M)
```

    【Output】
    []
    ['aa', 'aa']
    []
    ['cc']


# 6. VERBOSE, X

开启正则的多行写法，使之更清晰。举例：


```python
p = r"""
\d{3,4}
-?
\d{7,8}
"""
tel = '010-12345678'
print '【Output】'
print re.findall(p,tel)
print re.findall(p,tel,re.X)
```

    【Output】
    []
    ['010-12345678']


# 7. UNICODE, U

以unicode编码进行匹配，比如用`\s`匹配中文全角的空格符：`\u3000`，不加该编译标志和加该编译标志的效果对比如下：


```python
s = u'\u3000'
p = r'\s'
print '【Output】'
print re.findall(p,s)
print re.findall(p,s,re.U)
```

    【Output】
    []
    [u'\u3000']


# 8. 如何同时使用多个编译标志？

有时候可能同时要用到多种编译标志，比如我既想在匹配的时候忽略大小写，又想让`.`匹配换行符号`\n`，前面的方式貌似不行了，那怎么办呢？

**方法：在正则的任意位置加上这句即可：`(?iLmsux)`**

其中`i`对应`re.I`，`L`对应`re.L`，`m`对应`re.M`，`s`对应`re.S`，`u`对应`re.U`，`x`对应`re.X`。举例：


```python
s = 'Abc\ncom'
p = r'abc.com(?is)'  # 注：编译标志(?is)可以加在正则的任意位置，这里加在了末尾
print '【Output】'
print re.findall(p,s)
```

    【Output】
    ['Abc\ncom']
