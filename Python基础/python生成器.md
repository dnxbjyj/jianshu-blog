本文讲解一下python生成器的基本用法。

# 生成器的使用场景

当数据量很大的时候，比如从一个超大文本文件中读取内容，如果一下子把数据全部放在列表中，相当于一下子把大量数据放在了内存中，有可能造成内存溢出。那么如何解决呢？

解决方案：不存储所有的数据，而是存储列表元素的生成算法（相当于递推公式），只在使用的时候再根据生成算法生成相应的元素（惰性计算），这就是生成器。

# 创建生成器的方式

### 把列表生成式的中括号改为小括号


```python
a = (x for x in range(3))
print '【Output】'
print type(a)
print a.next()
print '-----'
for x in a:
    print x
```

    【Output】
    <type 'generator'>
    0
    -----
    1
    2
    

### 用yield关键字

如果生成器的递推算法比较复杂，列表生成式的方式已经无法满足要求，那么可以用函数+yield关键字的方式来创建生成器。

如果一个函数中出现了yield关键字，那么这个函数就不再是一个普通函数了，而变成了一个生成器，例如：


```python
def getNum(max):
    x = 0
    while x < max:
        yield x  # 相当于把普通函数的return语句变成了yield语句
        x += 1
a = getNum(3)

print '【Output】'
print type(a)
for x in a:
    print x
```

    【Output】
    <type 'generator'>
    0
    1
    2
    

### 函数遇到yield就中断的特性


```python
def get():
    for i in range(3):
        print 'step' + str(i)
        yield i
    yield 111
    
    for i in range(10,12):
        print 'step' + str(i)
        yield i
    yield 222

a = get()
print '【Output】'
for x in a:
    print x
```

    【Output】
    step0
    0
    step1
    1
    step2
    2
    111
    step10
    10
    step11
    11
    222
    

# 生成器的应用：生成斐波那契数列


```python
def fib(max):
    a,m,n = 0,1,1
    while(a < max):
        yield m
        m,n = n,m+n
        a += 1
print '【Output】'
for x in fib(6):
    print x
```

    【Output】
    1
    1
    2
    3
    5
    8
