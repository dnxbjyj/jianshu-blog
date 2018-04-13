知乎上有一个问题：[Python 有什么奇技淫巧？](https://www.zhihu.com/question/27376156)其中有各种不按套路出牌的招数，也不乏一些惊为天人的"奇技淫巧"，会让你大呼：居然还有这种操作？？？

本文就是对日常使用过的或者觉得很精妙的"奇技淫巧"的归纳总结。

# Python版问号表达式


```python
x = 1
y = 2
print ('no','yes')[x==y]
```

    no
    

这里巧妙地利用了Python会把False当做序列下标0、把True当做序列下标1的特性，把否定条件的输出放在前面的元组的第一个元素，而把肯定条件的输出放在第二个元素。又比如：


```python
a = [1,2,3]
print a[False]
print a[True]
```

    1
    2
    

此时是不是一幅"黑人问号"脸呢？

# 列表的深度拷贝


```python
a = [1,2,3]
b = a[:]
print id(a)
print id(b)

c = a
print id(c)
```

    59952144
    60485304
    59952144
    

提到深度拷贝，是不是一下子就想起来了copy.deepcopy()函数了？但是对于列表来讲，深度拷贝根本不用那么麻烦，只需像上面那样：`b = a[:]`即可实现，就是这么简单。

注：如果a是元组，这样玩是不可以的，切记！比如：


```python
a = (1,2,3)
b = a[:]
print id(a)
print id(b)
```

    59570456
    59570456
    

可以看出a和b的id是相同的，那么就想还是乖乖用copy.deepcopy()来拷贝吧：


```python
a = (1,2,3)
b = copy.deepcopy(a)
print id(a)
print id(b)
```

    60481864
    60481864
    

但是结果又让我们诧异了，这是因为元组是不可变对象，在内存中同一个元组只会存在一个，再怎么深度拷贝也没用（同为不可变对象的字符串也是同理的）。

# 在命令行启动一个本地服务器

```python
python -m SimpleHTTPServer
```

打开系统命令行，输入上面这条命令，然后打开浏览器输入地址：`http://localhost:8000/`，回车，将会看到命令行所在当前目录下的所有文件和文件夹，简直就是一个浏览器版的文件管理器。

# 把一个字符串写在多行


```python
s = ('abc'
    'de'
    'fgh'
    )
print s
```

    abcdefgh
    

# 链式比大小


```python
n = 1
print 0 < n < 5
print 9 > n < 5
print 0 > n < 5
print -1 > 0 < n < 5
```

    True
    True
    False
    False
    

# 动态导入包


```python
d = __import__('json').loads('{"a":123,"b":"bbb"}')
print type(d)
print d
```

    <type 'dict'>
    {u'a': 123, u'b': u'bbb'}
    

注：动态导入包只在当前语句生效。

# 字典推导式


```python
dic = {i:i ** 2 for i in xrange(5)}
print dic
```

    {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
    

见过列表推导式、生成器推导式，那么有没有见过字典推导式呢？上面就是一例。

# 快速反转字符串


```python
s = '123456'
print s[::-1]
```

    654321
    

# 优雅地打开文件


```python
with open('test.txt','r') as f:
    content = f.read()
```

用with语句上下文管理器可以自动地管理文件的打开、关闭，不需手工干预。

# else，不止是else

### 普通用法


```python
a = -1
if a > 0:
    print 'big'
else:
    print 'small'
```

    small
    

### 循环语句搭配else

判断一个数是否是素数：


```python
import math
n = 97
for i in range(2,int(math.sqrt(n) + 2)):
    if n % i == 0:
        print '{0} is not a prime!'.format(n)
        break
else:
    print '{0} is a prime!'.format(n)
```

    97 is a prime!
    

可见，如果循环中有break语句，且直到循环结束都没有执行过break语句，那么就会继续走后面的else分支。

### 异常处理搭配else


```python
try:
    print 1/0
except Exception as msg:
    print str(msg)
else:
    print 'all is OK!'
```

    integer division or modulo by zero
    


```python
try:
    print 1/1
except Exception as msg:
    print str(msg)
else:
    print 'all is OK!'
```

    1
    all is OK!
    

可见，如果没有发生异常，就会走else分支。

# 优雅地格式化字符串
### 用位置参数格式化
```
In [33]: s = 'hello {0},I am {1}. My age is {2}.'.format('Tom','Ben',23)

In [34]: s
Out[34]: 'hello Tom,I am Ben. My age is 23.'
```
注：位置参数的索引是从0开始的。

### 用参数名称格式化
```
In [35]: s = 'My name is {name}, {name}, {name}!!! And age is {age}'.format(name = 'Tom',age = 22)

In [36]: s
Out[36]: 'My name is Tom, Tom, Tom!!! And age is 22'
```
注：当有多个同名参数的时候，赋值的时候只需赋一次即可。
