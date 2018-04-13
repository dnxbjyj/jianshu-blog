Python中有许多功能丰富的内置函数，本文基于Python 2.7，就常用的一些函数的典型用法做一些积累，不断更新中。

# sorted函数的三种用法

```python
# coding:utf-8
# sorted函数的三种用法
from operator import itemgetter

data1 = [{'aa':22,'bb':11},{'aa':12,'cc':23},{'aa':67,'dd':103}]
data2 = [{'age':18,'name':'Tom'},{'age':10,'name':'Tim'},{'age':30,'name':'John'},{'age':18,'name':'Amy'}]

def sort1():
    # 对data1依据'aa'字段值的大小从小打到排序
    ret = sorted(data1,key = lambda item:item['aa'])  # 注：如果这里的key写'bb'或'cc'，会报KeyError，因为这两个属性并不是每个元素都有的
    print ret
    # 输出：
    '''
    [{'aa': 12, 'cc': 23}, {'aa': 22, 'bb': 11}, {'aa': 67, 'dd': 103}]
    '''

def sort2():
    # 对data1依据'aa'字段值的大小从小打到排序
    ret = sorted(data1,cmp = lambda x,y:cmp(x['aa'],y['aa']))
    print ret
    # 输出：
    '''
    [{'aa': 12, 'cc': 23}, {'aa': 22, 'bb': 11}, {'aa': 67, 'dd': 103}]
    '''

def sort3():
    # 使用itemgetter对data1依据'aa'字段值的大小从小打到排序
    ret = sorted(data1,key = itemgetter('aa'))
    print ret
    # 输出：
    '''
    [{'aa': 12, 'cc': 23}, {'aa': 22, 'bb': 11}, {'aa': 67, 'dd': 103}]
    '''

def sort4():
    # 对data2进行排序，先按照'age'从小到大排序，'age'相同的情况下，再按照'name'排序
    ret = sorted(data2,key = itemgetter('age','name'))
    print ret
    # 输出：
    '''
    [{'age': 10, 'name': 'Tim'}, {'age': 18, 'name': 'Amy'}, {'age': 18, 'name': 'Tom'}, {'age': 30, 'name': 'John'}]
    '''
```

# 执行命令行命令的三种方式

```python
# coding:utf-8
# 执行命令行命令的三种方式
import os
import commands

command = 'ls -al /root'

def method1():
    '''
    方式1
    '''
    os.system(command)
    # 执行结果：返回执行状态码

def method2():
    '''
    方式2
    '''
    out1 = os.popen(command)
    print out1.read()
    # 输出：执行结果字符串

def method3():
    '''
    方式3
    '''
    (status,out) = commands.getstatusoutput(command)
    # 输出：status是执行状态码，out是执行结果字符串
```

# zip函数的用法

```
Docstring:
zip(seq1 [, seq2 [...]]) -> [(seq1[0], seq2[0] ...), (...)]
Return a list of tuples, where each tuple contains the i-th element
from each of the argument sequences.  The returned list is truncated
in length to the length of the shortest argument sequence.
```

先来看看zip函数的文档，从文档中可以看出，zip函数接收1个或多个序列作为参数，返回一个由元组组成的列表。

结果列表的第i个元素是seq1~seqn的第i个元素组成的元组。

结果列表的长度等于seq1~seqn中最短的序列的长度。

一段测试代码如下：

```python
# coding:utf-8

def main():
    a = '1234'
    b = [4,6,7]

    print zip()
    # 输出：[]

    print zip(a)
    # 输出：[('1',), ('2',), ('3',), ('4',)]

    print zip(a,a)
    # 输出：[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')]

    print zip(a,[])
    # 输出：[]

    print zip(a,b)
    # 输出：[('1', 4), ('2', 6), ('3', 7)]

if __name__ == '__main__':
    main()
```

# map函数的用法

map函数是一个高阶函数，支持传入一个函数作为参数。先来看它的文档是怎么说的：

```
Docstring:
map(function, sequence[, sequence, ...]) -> list
Return a list of the results of applying the function to the items of
the argument sequence(s).  If more than one sequence is given, the
function is called with an argument list consisting of the corresponding
item of each sequence, substituting None for missing values when not all
sequences have the same length.  If the function is None, return a list of
the items of the sequence (or a list of tuples if more than one sequence).
```

从map函数的文档中可以看出，该函数的第一个参数为一个函数对象，后面可以跟一个或多个序列，函数的返回值是一个list.

对比zip函数的用法，可以发现其实map函数就是一个增强版的zip函数，与zip函数不同的是，map函数支持传入一个函数参数来处理序列。

如果第一个函数参数不为None，那么返回的结果list的第i个元素，是将该函数作用于每个序列的第i个元素的结果。如果传入的序列的长度不都是相同的，那么结果list的某些元素将会是None.

如果第一个函数参数为None，那么返回的的结果list的第i个元素，是每个序列第i个元素组成的n元组（n为序列的个数），如果每个序列的长度不都是相同的，那么结果list的某些元素将是None.

下面通过一段程序来看map函数的实际用法：

```python
# coding:utf-8

def main():
    a = [1,2,3,4]
    b = [3,5,9]
    c = [8,2,3]
    print map(None,a,b,c)
    # 输出：[(1, 3, 8), (2, 5, 2), (3, 9, 3), (4, None, None)]

    print map(lambda x : x ** 2,a)
    # 输出：[1, 4, 9, 16]

    # print map(lambda x,y : x + y,a)
    # 输出：TypeError <lambda>() takes exactly 2 arguments (1 given)

    print map(lambda x,y : x + y,b,c)
    # 输出：[11, 7, 12]

    # print map(lambda x,y,z : x + y + z,a,b,c)
    # 输出：TypeError: unsupported operand type(s) for +: 'int' and 'NoneType'

    print map(lambda x,y : x + y if x is not None and y is not None else None,a,b)
    # 输出：[4, 7, 12, None]

if __name__ == '__main__':
    main()
```

# reduce函数的用法

先看函数文档：

```
Docstring:
reduce(function, sequence[, initial]) -> value
Apply a function of two arguments cumulatively to the items of a sequence,
from left to right, so as to reduce the sequence to a single value.
For example, reduce(lambda x, y: x+y, [1, 2, 3, 4, 5]) calculates
((((1+2)+3)+4)+5).  If initial is present, it is placed before the items
of the sequence in the calculation, and serves as a default when the
sequence is empty.
```

reduce函数接收三个参数：function，seq，init，其中前两个是必选参数，最后一个为可选参数。

reduce函数做了这样一件事情：从左到右遍历seq，将seq[0]和seq[1]传入函数function进行运算（function为一个接收两个参数的函数），得到一个结果值，然后将这个结果值再和seq[2]传入fucntion进行运算再得到一个新的结果值...以此类推。最终得到一个值，就是该函数的返回值。

如果传入了init，那么init和seq[0]会作为第一次传入funciton的参数，如果seq为空，init也会作为reduce的返回值返回。

用法示例如下：

```python
# coding:utf-8

def main():
    lst = [1,2,3]
    f = lambda x,y:x*y
    print reduce(f,lst)
    # 输出：6

    print reduce(f,lst,-1)
    # 输出：-6

    print reduce(f,[],-2)
    # 输出：-2

if __name__ == '__main__':
    main()

```

# base64编解码

```python
# coding:utf-8
# 测试base64编解码
import base64

def main():
    s = '123abc'

    # 编码
    print base64.b64encode(s)
    # 输出：MTIzYWJj

    # 解码
    print base64.b64decode('MTIzYWJj')
    # 输出：123abc

if __name__ == '__main__':
    main()
```
