collections库是python内置的集合库，本文主要讲解以下5种数据结构的用法：

* namedtuple  命名元组，是tuple的子类
* deque  双向列表
* defaultdict  有默认值的字典，是dict的子类
* OrderedDict  key有序的字典，是dict的子类
* Counter  计数器，是dict的子类

# 准备工作


```python
from collections import namedtuple,deque,defaultdict,OrderedDict,Counter
```

# namedtuple (python 2.6+)

用法：namedtuple('名称',[属性列表])


```python
Point = namedtuple('Point',['x','y'])
p = Point(1,2)
```


```python
print '【Output】'
print p
print p.x,p.y
print p.count,p.index
print isinstance(p,Point)
print isinstance(p,tuple)
```

    【Output】
    Point(x=1, y=2)
    1 2
    <built-in method count of Point object at 0x038B2288> <built-in method index of Point object at 0x038B2288>
    True
    True
    

# deque (python 2.4+)

适用于队列和栈，插入和删除元素很高效。


```python
lst = ['a','b','c']
dq = deque(lst)
dq.append('d')
print dq
```

    deque(['a', 'b', 'c', 'd'])
    


```python
dq.pop()
```




    'd'




```python
print dq
```

    deque(['a', 'b', 'c'])
    


```python
dq.appendleft('-1')
```


```python
print dq
```

    deque(['-1', 'a', 'b', 'c'])
    


```python
dq.popleft()
```




    '-1'




```python
print dq
```

    deque(['a', 'b', 'c'])
    

# defaultdict (python 2.5+)

当key不存在的时候可返回一个默认值，默认值由传入的函数对象决定。


```python
dd = defaultdict(lambda:'N/A')
dd['key1'] = 'aa';
print dd['key1']
print dd['key2']
```

    aa
    N/A
    

# OrderedDict(python 2.7+)

key值有序的字典，顺序按照插入的顺序排序。


```python
data = [('a',1),('b',2),('c',3)]
d = dict(data)
print d
```

    {'a': 1, 'c': 3, 'b': 2}
    


```python
od = OrderedDict(data)
print od
```

    OrderedDict([('a', 1), ('b', 2), ('c', 3)])
    

# Counter (python 2.7+)

### 用序列生成Counter对象


```python
s = 'abcdeabcdabcaba'
c = Counter(s)
print c
```

    Counter({'a': 5, 'b': 4, 'c': 3, 'd': 2, 'e': 1})
    


```python
print c.most_common(3)
```

    [('a', 5), ('b', 4), ('c', 3)]
    


```python
print sorted(c)
```

    ['a', 'b', 'c', 'd', 'e']
    


```python
print ''.join(sorted(c.elements()))
```

    aaaaabbbbcccdde
    


```python
print c.values()
```

    [5, 3, 4, 1, 2]
    


```python
print c.elements()
```

    <itertools.chain object at 0x039BC630>
    

### 更新Counter对象


```python
d = Counter('bbb')
c.update(d)
```


```python
print c.most_common()
```

    [('b', 7), ('a', 5), ('c', 3), ('d', 2), ('e', 1)]
    

### 用字典生成Counter对象


```python
d = {'a':1,'b':2,'c':3}
c = Counter(d)
print c
```

    Counter({'c': 3, 'b': 2, 'a': 1})
    

### value值为字符串时，按照字典序排序


```python
d = {'a':'aa1','b':'ba1','c':'ca2'}
c = Counter(d)
print c
```

    Counter({'c': 'ca2', 'b': 'ba1', 'a': 'aa1'})
