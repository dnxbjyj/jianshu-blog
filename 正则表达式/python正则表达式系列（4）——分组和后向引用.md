分组，即分组匹配，也称为捕获组，是正则中的一种比较重要的匹配方式。此外后向引用和分组相结合，可以写出很多复杂匹配场景的正则。

# 1. 分组

分组的方法：将子表达式用小括号括起来，如：`(exp)`，表示匹配表达式`exp`，并捕获文本到自动命名的组里。举例：


```python
import re
s = 'c1c b2b c3c'
p = re.compile(r'c(\d)c')
print '【Output】'
print re.findall(p,s)
```

    【Output】
    ['1', '3']


```python
s = 'a1b2 c3d4 ea7f'
p1 = re.compile(r'[a-z]\d[a-z]\d')

print '【Output 1】'
print re.findall(p1,s)

p2 = re.compile(r'[a-z]\d[a-z](\d)')

print '\n【Output 2】'
print re.findall(p2,s)

p3 = re.compile(r'[a-z](\d)[a-z](\d)')

print '\n【Output 3】'
print re.findall(p3,s)
```

    【Output 1】
    ['a1b2', 'c3d4']
    
    【Output 2】
    ['2', '4']
    
    【Output 3】
    [('1', '2'), ('3', '4')]
    

```python
s = 'age:13,name:Tom;age:18,name:John'
p = re.compile(r'age:(\d+),name:(\w+)')
it = re.finditer(p,s)
print '【Output】'
for m in it:
    print '------'
    print m.group()
    print m.group(0)
    print m.group(1)
    print m.group(2)
```

    【Output】
    ------
    age:13,name:Tom
    age:13,name:Tom
    13
    Tom
    ------
    age:18,name:John
    age:18,name:John
    18
    John


# 2. 忽略某个分组

有时候给正则的某个子表达式加括号并不是为了分组，而仅仅是为了看起来更清晰，因此在匹配结果中并不想匹配该子表达式，那么该怎么办呢？答案是忽略该分组，方法：`(?:exp)`。举例：只想匹配name，不想匹配age：


```python
s = 'age:13,name:Tom'
p1 = re.compile(r'age:(\d+),name:(\w+)')
print '【Output】'
# 不忽略分组
print re.findall(p1,s)

# 忽略分组
p2 = re.compile(r'age:(?:\d+),name:(\w+)')
print re.findall(p2,s)
```

    【Output】
    [('13', 'Tom')]
    ['Tom']


# 3. 后向引用

所谓后向引用，就是对前面出现过的分组再一次引用，使用默认的分组名称进行后向引用：`\1,\2,\3...`（注：从1开始）

举例：


```python
# 匹配字符串中连续出现的两个相同的单词
s = 'hello blue go go hello'
p = re.compile(r'\b(\w+)\b\s+\1\b')  # 这里的'\1'就对应前面的(\w+)
print '【Output】'
print re.findall(p,s)
```

    【Output】
    ['go']


# 4. 自定义名称分组的后向引用

python正则可以对分组自定义名称，然后可以使用自定义名称进行后向引用，使用自定义分组名称比使用默认分组名称更加清晰、更容易让人理解。对分组自定义名称的方法：


```python
(?P<myname>exp)
```

后向引用的方式：


```python
(?P=myname)
```

这里要注意的是，其他语言的正则与python正则的分组自定义名称的语法不太一样，其他语言是这样写的：


```python
# 自定义名称
(?<name>exp)
# 后向引用
\K<name>
```

举个例子：


```python
s = 'hello blue go go hello'
p = re.compile(r'\b(?P<my_group1>\w+)\b\s+(?P=my_group1)\b')
print '【Output】'
print re.findall(p,s)
```

    【Output】
    ['go']

# 5.嵌套分组

```python
s  = '2017-07-10 20:00'
p = re.compile(r'(((\d{4})-\d{2})-\d{2}) (\d{2}):(\d{2})')
re.findall(p,s)
# 输出：
# [('2017-07-10','2017-07','2017','20','00')]

se = re.search(p,s)
print se.group()
print se.group(0)
print se.group(1)
print se.group(2)
print se.group(3)
print se.group(4)
print se.group(5)

# 输出：
'''
'2017-07-10 20:00'
'2017-07-10 20:00'
'2017-07-10'
'2017-07'
'2017'
'20'
'00'
'''
```
可以看出，分组的序号是以左小括号`(`从左到右的顺序为准的。

# 6. 后向引用的应用

## 1. 匹配"ABAB"型字符串


```python
s = 'abab cdcd efek'
p = re.compile(r'(\w\w)\1')
print '【Output】'
print re.findall(p,s)
```

    【Output】
    ['ab', 'cd']


## 2. 匹配"AABB"型字符串


```python
s = 'abab cdcd xxyy'
p = re.compile(r'(\w)\1(\w)\2')
print '【Output】'
print re.findall(p,s)
```

    【Output】
    [('x', 'y')]


## 3. 匹配"AABA"型字符串


```python
s = 'abab cdcd xxyx'
p = re.compile(r'(\w)\1(?:\w)\1')
print '【Output】'
print re.findall(p,s)
```

    【Output】
    ['x']


## 4. 匹配"ABBA"型字符串


```python
s = 'abab toot'
p = re.compile(r'(\w)(\w)\2\1')
print '【Output】'
print re.findall(p,s)
```

    【Output】
    [('t', 'o')]


## 5. 向字符串中的某些位置插入字符

有一个需求：在一个字符串中的所有通配符`% _ [ ]`前都加上`\`符进行转义，如果通配符前面本来就有`\`，则不再插入。举例：


```python
s = 'abc\\_de%fgh[c][]c'
special = r'[%_\[\]]'
print '【Output】'
print 's = {0}'.format(s)
print re.sub(r'([^\\])(?=%s)' % special,r'\1\\',s)
# 注：这里的"(?=%s)"是零宽断言，匹配一个位置，零宽断言在后面会讲
```

    【Output】
    s = abc\_de%fgh[c][]c
    abc\_de\%fgh\[c\]\[\]c


## 6. 在字符串中从后往前每隔3个字符插入一个`,`符号


```python
s = '1234567890'
s = s[::-1]
print '【Output】'
print s
s = re.sub(r'(...)',r'\1,',s)
print s[::-1]
```

    【Output】
    0987654321
    1,234,567,890
