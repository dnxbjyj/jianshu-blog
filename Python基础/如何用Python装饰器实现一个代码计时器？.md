有时候我们很希望看到程序中某个函数或某个代码段的耗时情况，那么该如何办呢？本文用两种方式实现了代码计时器的功能，第一种方式是采用装饰器来实现，第二种方式采用上下文管理器实现。

其实计算代码的运行时间，最朴素的想法就是先记录下来某段代码刚开始运行时的时间，等到运行完之后，再看一下结束时的时间，最后和开始运行时的时间求个差值，就是这段代码所花费的时间。

下面两种计时器的实现方式就是用到这样一种非常简单的方法。

# 用装饰器实现函数计时器

```python
# coding:utf-8
from functools import wraps
import time

def func_timer(function):
    '''
    用装饰器实现函数计时
    :param function: 需要计时的函数
    :return: None
    '''
    @wraps(function)
    def function_timer(*args, **kwargs):
        print '[Function: {name} start...]'.format(name = function.__name__)
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        print '[Function: {name} finished, spent time: {time:.2f}s]'.format(name = function.__name__,time = t1 - t0)
        return result
    return function_timer

@func_timer
def test(x,y):
    s = x + y
    time.sleep(1.5)
    print 'the sum is: {0}'.format(s)

if __name__ == '__main__':
    test(1,2)
    # 输出结果
    '''
    [Function: test start...]
    the sum is: 3
    [Function: test finished, spent time: 1.50s]
    '''
```

# 用上下文管理器实现代码段计时器

上下文管理器其实是一个实现了`__enter__`和`__exit__`两个特殊方法的对象，可以用with语法调用。可以参照操作文件的`with oepn`操作，比如：

```python
with open('data.txt','r') as fin:
    data = fin.read()
```

使用with上下文管理器操作文件的好处就是，不用担心文件使用完之后忘记关闭，上下文管理器会自动帮你关闭。

那么下面就用上下文管理器来实现一个代码段计时器：

```python
# coding:utf-8
from functools import wraps
import time

class MyTimer(object):
    '''
    用上下文管理器计时
    '''
    def __enter__(self):
        self.t0 = time.time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        print '[finished, spent time: {time:.2f}s]'.format(time = time.time() - self.t0)

def test(x,y):
    s = x + y
    time.sleep(1.5)
    print 'the sum is: {0}'.format(s)

if __name__ == '__main__':
    with MyTimer() as t:
        test(1,2)
        time.sleep(1)
        print 'do other things'
    # 输出：
    '''
    the sum is: 3
    do other things
    [finished, spent time: 2.53s]
    '''
```

# 总结

可以看出，上述两种计时器的实现方式各有优缺点，用装饰器实现的计时器优点是使用起来非常方便，给要计时的函数加一个装饰器即可，但不足之处是无法对一个代码片段进行计时。而用上下文管理器实现的计时器就可以对任意一个代码段进行计时，弥补了装饰器计时器的缺陷。

具体用哪种计时器，还是要根据实际情况来选择。
