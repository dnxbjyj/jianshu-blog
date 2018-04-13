# 线程、进程和协程是什么
线程、进程和协程的详细概念解释和原理剖析不是本文的重点，本文重点讲述在Python中怎样实际使用这三种东西，因此此处引用其他朋友的文章仅粗略地讲解一下这三种东西（想要了解更多，请参看引用的文章）：
> 参考： [进程、线程、协程之概念理解](http://www.cnblogs.com/work115/p/5620272.html)
> * 进程（Process）是计算机中的程序关于某数据集合上的一次运行活动，是系统进行资源分配和调度的基本单位，是操作系统结构的基础。
> * 线程，有时被称为轻量级进程(Lightweight Process，LWP），是程序执行流的最小单元。
> * 协程：一个程序可以包含多个协程，可以对比于一个进程包含多个线程，因而下面我们来比较协程和线程：我们知道多个线程相对独立，有自己的上下文，切换受系统控制；而协程也相对独立，有自己的上下文，但是其切换由自己控制，由当前协程切换到其他协程由当前协程来控制。

# 准备工作
磨刀不误砍柴工，在用实例讲解线程、进程和协程怎么使用之前，先准备一些工具：
* 实际上多线程、多进程和协程，都属于并发编程，并发编程的最重要的目标就是提高程序运行的效率，那么我们需要一个计算一个函数耗时长度的工具，用于对比不同方式程序的运行时间，这里我们写一个函数计时装饰器`fn_timer`来完成这件事：
```python
def fn_timer(function):
    '''
    函数计时装饰器
    :param function: 函数对象
    :return: 装饰器
    '''
    @wraps(function)
    def function_timer(*args,**kwargs):
        # 起始时间
        t0 = time.time()
        # 调用函数
        result = function(*args,**kwargs)
        # 结束时间
        t1 = time.time()
        # 打印函数耗时
        print '[finished function:{func_name} in {time:.2f}s]'.format(func_name = function.__name__,time = t1 - t0)
        return result
    return function_timer
```
该装饰器的用法示例：
```python
# 测试
@fn_timer
def add(x,y):
    time.sleep(1.22)
    return x + y

if __name__ == '__main__':
    # 测试
    sum = add(1,2)
    print sum
```
运行代码输出：
```
[finished function:test in 1.23s]
3
```
* 实际使用中，大规模爬虫程序很适合用并发来实现，所以我们再准备一些网址放在`urls`列表中，用于测试爬虫程序的效率（都是百度百科的一些词条页面）：
```python
# 20个网页
urls = ['https://baike.baidu.com/item/%E8%87%AA%E7%94%B1%E8%BD%AF%E4%BB%B6',
        'https://baike.baidu.com/item/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%A8%8B%E5%BA%8F%E8%AE%BE%E8%AE%A1%E8%AF%AD%E8%A8%80',
        'https://baike.baidu.com/item/%E5%9F%BA%E9%87%91%E4%BC%9A',
        'https://baike.baidu.com/item/%E5%88%9B%E6%96%B02.0',
        'https://baike.baidu.com/item/%E5%95%86%E4%B8%9A%E8%BD%AF%E4%BB%B6',
        'https://baike.baidu.com/item/%E5%BC%80%E6%94%BE%E6%BA%90%E4%BB%A3%E7%A0%81',
        'https://baike.baidu.com/item/OpenBSD',
        'https://baike.baidu.com/item/%E8%A7%A3%E9%87%8A%E5%99%A8',
        'https://baike.baidu.com/item/%E7%A8%8B%E5%BA%8F/71525',
        'https://baike.baidu.com/item/%E7%BC%96%E7%A8%8B%E8%AF%AD%E8%A8%80',
        'https://baike.baidu.com/item/C%2B%2B',
        'https://baike.baidu.com/item/%E8%B7%A8%E5%B9%B3%E5%8F%B0',
        'https://baike.baidu.com/item/Web/150564',
        'https://baike.baidu.com/item/%E7%88%B1%E5%A5%BD%E8%80%85',
        'https://baike.baidu.com/item/%E6%95%99%E5%AD%A6',
        'https://baike.baidu.com/item/Unix%20shell',
        'https://baike.baidu.com/item/TIOBE',
        'https://baike.baidu.com/item/%E8%AF%BE%E7%A8%8B',
        'https://baike.baidu.com/item/MATLAB',
        'https://baike.baidu.com/item/Perl']
```
* 整合：把函数计时装饰器和urls列表封装在一个类：`utils.py`中：
```python
# coding:utf-8
from functools import wraps
import time

# 20个网页
urls = ['https://baike.baidu.com/item/%E8%87%AA%E7%94%B1%E8%BD%AF%E4%BB%B6',
        'https://baike.baidu.com/item/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%A8%8B%E5%BA%8F%E8%AE%BE%E8%AE%A1%E8%AF%AD%E8%A8%80',
        'https://baike.baidu.com/item/%E5%9F%BA%E9%87%91%E4%BC%9A',
        'https://baike.baidu.com/item/%E5%88%9B%E6%96%B02.0',
        'https://baike.baidu.com/item/%E5%95%86%E4%B8%9A%E8%BD%AF%E4%BB%B6',
        'https://baike.baidu.com/item/%E5%BC%80%E6%94%BE%E6%BA%90%E4%BB%A3%E7%A0%81',
        'https://baike.baidu.com/item/OpenBSD',
        'https://baike.baidu.com/item/%E8%A7%A3%E9%87%8A%E5%99%A8',
        'https://baike.baidu.com/item/%E7%A8%8B%E5%BA%8F/71525',
        'https://baike.baidu.com/item/%E7%BC%96%E7%A8%8B%E8%AF%AD%E8%A8%80',
        'https://baike.baidu.com/item/C%2B%2B',
        'https://baike.baidu.com/item/%E8%B7%A8%E5%B9%B3%E5%8F%B0',
        'https://baike.baidu.com/item/Web/150564',
        'https://baike.baidu.com/item/%E7%88%B1%E5%A5%BD%E8%80%85',
        'https://baike.baidu.com/item/%E6%95%99%E5%AD%A6',
        'https://baike.baidu.com/item/Unix%20shell',
        'https://baike.baidu.com/item/TIOBE',
        'https://baike.baidu.com/item/%E8%AF%BE%E7%A8%8B',
        'https://baike.baidu.com/item/MATLAB',
        'https://baike.baidu.com/item/Perl']


def fn_timer(function):
    '''
    函数计时装饰器
    :param function: 函数对象
    :return: 装饰器
    '''
    @wraps(function)
    def function_timer(*args,**kwargs):
        # 起始时间
        t0 = time.time()
        # 调用函数
        result = function(*args,**kwargs)
        # 结束时间
        t1 = time.time()
        # 打印函数耗时
        print '[finished function:{func_name} in {time:.2f}s]'.format(func_name = function.__name__,time = t1 - t0)
        return result
    return function_timer

# 测试
@fn_timer
def add(x,y):
    time.sleep(1.22)
    return x + y

if __name__ == '__main__':
    # 测试
    sum = add(1,2)
    print sum
    # 输出：
    '''
    [finished function:test in 1.23s]
    3
    '''
```

# 实例讲解多线程的用法
### 从听音乐、看电影讲起
我现在要做两件事情：听音乐、看电影，听一首音乐假如耗时1秒，看一部电影假如耗时5秒，用两个函数定义这两个任务如下：
```python
# 耗时任务：听音乐
def music(name):
    print 'I am listening to music {0}'.format(name)
    time.sleep(1)

# 耗时任务：看电影
def movie(name):
    print 'I am watching movie {0}'.format(name)
    time.sleep(5)
```
假如我现在要听10首音乐、看2部电影，那么我就有如下几种方案：
* 方案一：先一个个听完10首音乐，再一个个看完2部电影，顺序完成，代码如下：
```python
# 单线程操作：顺序执行听10首音乐，看2部电影
@fn_timer
def single_thread():
    for i in range(10):
        music(i)
    for i in range(2):
        movie(i)
```
让我们执行一下这段代码，输出如下：
```
    I am listening to music 0
    I am listening to music 1
    I am listening to music 2
    I am listening to music 3
    I am listening to music 4
    I am listening to music 5
    I am listening to music 6
    I am listening to music 7
    I am listening to music 8
    I am listening to music 9
    I am watching movie 0
    I am watching movie 1
    [finished function:single_thread in 20.14s]
```
可以看到，老老实实严格按照先后顺序来一件件做这些事情，所需的总时间和每件事情耗时加起来是一样多的。

* 方案二：刚刚的方案不太好，太费时间了，那么能不能同时进行一些事情呢？答案是可以的，可以同时听多首音乐，同时看多部电影进行，代码如下：
```python
# 多线程执行：听10首音乐，看2部电影
@fn_timer
def multi_thread():
    # 线程列表
    threads = []
    for i in range(10):
        # 创建一个线程，target参数为任务处理函数，args为任务处理函数所需的参数元组
        threads.append(threading.Thread(target = music,args = (i,)))
    for i in range(2):
        threads.append(threading.Thread(target = movie,args = (i,)))

    for t in threads:
        # 设为守护线程
        t.setDaemon(True)
        # 开始线程
        t.start()
    for t in threads:
        t.join()
```
执行上述代码，运行结果：
```
    I am listening to music 0
    I am listening to music 1
    I am listening to music 2
    I am listening to music 3
    I am listening to music 4
    I am listening to music 5
    I am listening to music 6
    I am listening to music 7
    I am listening to music 8
    I am listening to music 9
    I am watching movie 0
    I am watching movie 1
    [finished function:multi_thread in 5.02s]
```
这次只用了5秒就完成了，完成效率显著提升。这次试用多线程执行多个任务，所有任务最终的总耗时 = 耗时最长的那个单个任务的耗时，即看一部电影的5秒钟时间。

* 方案三：使用线程池。上面使用多线程的方式比较繁琐，下面使用线程池来实现：
```python
# 使用线程池执行：听10首音乐，看2部电影
@fn_timer
def use_pool():
    # 设置线程池大小为20，如果不设置，默认值是CPU核心数
    pool = Pool(20)
    pool.map(movie,range(2))
    pool.map(music,range(10))
    pool.close()
    pool.join()
```
执行结果：
```
    I am listening to music 0
    I am listening to music 1
    I am listening to music 2
    I am listening to music 3
    I am listening to music 4
    I am listening to music 5
    I am listening to music 6
    I am listening to music 7
    I am listening to music 8
    I am listening to music 9
    I am watching movie 0
    I am watching movie 1
    [finished function:use_pool in 6.12s]
```
可以看出使用线程池反而比手工调度线程多耗时一秒钟，可能是因为线程池内部对线程的调度和线程切换的耗时造成的。

### 实例：使用多线程下载网页
话不多说，直接上代码，用多线程并发下载20个百度百科网页的实例代码及运行结果如下：
```python
# coding:utf-8
# 测试多线程
import threading
import time
from utils import fn_timer
from multiprocessing.dummy import Pool
import requests
from utils import urls

# 应用：使用单线程下载多个网页的内容
@fn_timer
def download_using_single_thread(urls):
    resps = []
    for url in urls:
        resp = requests.get(url)
        resps.append(resp)
    return resps

# 应用：使用多线程下载多个网页的内容
@fn_timer
def download_using_multi_thread(urls):
    threads = []
    for url in urls:
        threads.append(threading.Thread(target = requests.get,args = (url,)))
    for t in threads:
        t.setDaemon(True)
        t.start()
    for t in threads:
        t.join()

# 应用：使用线程池下载多个网页的内容
@fn_timer
def download_using_pool(urls):
    pool = Pool(20)
    # 第一个参数为函数名，第二个参数一个可迭代对象，为函数所需的参数列表
    resps = pool.map(requests.get,urls)
    pool.close()
    pool.join()
    return resps

def main():
    # 1.使用单线程
    resps = download_using_single_thread(urls)
    print len(resps)
    # 输出：
    '''
    [finished function:download_using_single_thread in 6.18s]
    20
    '''
    # 2. 使用多线程
    download_using_multi_thread(urls)
    # 输出：
    '''
    [finished function:download_using_multi_thread in 0.73s]
    '''

    # 3.使用线程池
    resps = download_using_pool(urls)
    print len(resps)
    # 输出：
    '''
    [finished function:download_using_pool in 0.84s]
    20
    '''

if __name__ == '__main__':
    main()

```

# 实例讲解多进程的用法
### 多进程和进程池的使用
实例代码如下：
```python
# coding:utf-8
# 测试多进程
import os
import time
from multiprocessing import Process,Pool,Queue
from utils import fn_timer
import random

# 简单的任务
@fn_timer
def do_simple_task(task_name):
    print 'Run child process {0}, task name is: {1}'.format(os.getpid(),task_name)
    time.sleep(1.2)
    return task_name

@fn_timer
# 1. 测试简单的多进程
def test_simple_multi_process():
    p1 = Process(target=do_simple_task, args=('task1',))
    p2 = Process(target=do_simple_task, args=('task2',))
    print 'Process will start...'
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    print 'Process end.'

@fn_timer
# 2. 测试使用进程池
def test_use_process_pool():
    # 创建一个进程池，数字表示一次性同时执行的最大子进程数
    pool = Pool(5)
    # 任务返回值列表
    results = []
    # 任务名称列表
    task_names = []
    for i in range(7):
        task_names.append('task{0}'.format(i))
    # 并发执行多个任务，并获取任务返回值
    results = pool.map_async(do_simple_task,task_names)
    print 'Many processes will start...'
    pool.close()
    pool.join()

    print 'All processes end, results is: {0}'.format(results.get())

def main():
    test_simple_multi_process()
    # 输出：
    '''
    Process will start...
    Run child process 1524, task name is: task2
    Run child process 1728, task name is: task1
    [finished function:do_simple_task in 1.20s]
    [finished function:do_simple_task in 1.20s]
    Process end.
    [finished function:test_simple_multi_process in 1.34s]
    '''

    test_use_process_pool()
    # 输出：
    '''
    Many processes will start...
    Run child process 7568, task name is: task0
    Run child process 7644, task name is: task1
    Run child process 7628, task name is: task2
    Run child process 7620, task name is: task3
    Run child process 7660, task name is: task4
    [finished function:do_simple_task in 1.20s]
    Run child process 7568, task name is: task5
    [finished function:do_simple_task in 1.20s]
    Run child process 7644, task name is: task6
    [finished function:do_simple_task in 1.20s]
    [finished function:do_simple_task in 1.20s]
    [finished function:do_simple_task in 1.20s]
    [finished function:do_simple_task in 1.20s]
    [finished function:do_simple_task in 1.20s]
    All processes end, results is: ['task0', 'task1', 'task2', 'task3', 'task4', 'task5', 'task6']
    [finished function:test_use_process_pool in 2.62s]
    '''
if __name__ == '__main__':
    main()
```
### 进程之间的通信
进程间的通信采用队列来实现，实例代码如下：
```python
# coding:utf-8
# 测试进程间的通信
import os
import time
from multiprocessing import Process,Pool,Queue
from utils import fn_timer
import random

# 写进程执行的任务
def write(q):
    for value in ['A','B','C']:
        print 'Put value: {0} to queue.'.format(value)
        q.put(value)
        time.sleep(random.random())

# 读进程执行的任务
def read(q):
    while True:
        value = q.get(True)
        print 'Get value: {0} from queue.'.format(value)

# 测试进程间的通信
def test_communication_between_process():
    q = Queue()
    # 写进程
    pw = Process(target = write,args = (q,))
    # 读进程
    pr = Process(target = read,args = (q,))
    pw.start()
    pr.start()
    pw.join()
    # 因为读任务是死循环，所以要强行结束
    pr.terminate()

def main():
    test_communication_between_process()
    # 输出
    '''
    Put value: A to queue.
    Get value: A from queue.
    Put value: B to queue.
    Get value: B from queue.
    Put value: C to queue.
    Get value: C from queue.
    '''

if __name__ == '__main__':
    main()
```

# 实例讲解协程的用法
下面用协程下载同样的20个网页，实例代码如下：
```python
# coding:utf-8
# 测试协程
import requests
import gevent
import utils
from utils import fn_timer
from gevent.pool import Pool
from gevent import monkey
# 打动态补丁，把标准库中的thread/socket等替换掉，让它们变成非阻塞的
monkey.patch_all()

session = requests.Session()
session.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'

@fn_timer
def download_using_single_thread(urls):
    '''
    顺序执行下载多个网页
    :param urls: 要下载的网页内容
    :return: 响应列表
    '''
    resps = []
    for url in urls:
        resps.append(session.get(url))
    return resps

@fn_timer
def download_using_coroutine(urls):
    '''
    使用协程下载
    :param urls: 要下载的网页内容
    :return: 响应列表
    '''
    spawns = []
    for url in urls:
        spawns.append(gevent.spawn(session.get,url))
    # 在遇到IO操作时，gevent会自动切换，并发执行（异步IO）
    gevent.joinall(spawns)

@fn_timer
def download_using_coroutine_pool(urls):
    # 创建协程池，并设置最大并发量
    pool = Pool(20)
    pool.map(session.get,urls)

def main():
    # 1.使用单线程下载20个网页
    download_using_single_thread(utils.urls)
    # 输出：
    '''
    [finished function:download_using_single_thread in 1.83s]
    '''

    # 2.使用协程下载20个网页
    download_using_coroutine(utils.urls)
    # 输出：
    '''
    [finished function:download_using_coroutine in 0.69s]
    '''

    # 3.使用协程池下载20个网页
    download_using_coroutine_pool(utils.urls)
    # 输出：
    '''
    [finished function:download_using_coroutine_pool in 0.78s]
    '''

if __name__ == '__main__':
    main()
```
可以发现，协程的效率也是非常高的。

# 多线程、多进程和协程并发效率的对比
下面分别使用线程池、进程池和协程池下载100个相同的网页，来对比其效率：
```python
# coding:utf-8
# 对比多线程、多进程和协程下载网页
import requests
import utils
from utils import fn_timer
from multiprocessing.dummy import Pool as thread_pool
from multiprocessing import Pool as process_pool
from gevent.pool import Pool as gevent_pool
from gevent import monkey
# 打动态补丁，把标准库中的thread/socket等替换掉，让它们变成非阻塞的
monkey.patch_all()

session = requests.Session()
session.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'

# 1. 使用线程池下载多个网页的内容
@fn_timer
def download_using_thread_pool(urls):
    pool = thread_pool(100)
    # 第一个参数为函数名，第二个参数一个可迭代对象，为函数所需的参数列表
    resps = pool.map(session.get,urls)
    pool.close()
    pool.join()
    return resps

# 2. 测试使用进程池
@fn_timer
def download_using_process_pool(urls):
    # 创建一个进程池，数字表示一次性同时执行的最大子进程数
    pool = process_pool(100)
    # 任务返回值列表
    results = []
    # 并发执行多个任务，并获取任务返回值
    results = pool.map_async(session.get,urls)
    pool.close()
    pool.join()
    return results.get()

# 3. 使用协程池下载
@fn_timer
def download_using_coroutine_pool(urls):
    # 创建协程池，并设置最大并发量
    pool = gevent_pool(100)
    pool.map(session.get,urls)

def main():
    # 1. 使用线程池下载100个网页
    download_using_thread_pool(utils.urls * 5)
    # 输出：
    '''
    [finished function:download_using_thread_pool in 3.68s]
    '''

    # 2. 使用进程池下载100个网页
    download_using_process_pool(utils.urls * 5)
    # 输出：
    '''
    卡死了
    '''

    # 3.使用协程池下载20个网页
    download_using_coroutine_pool(utils.urls * 5)
    # 输出：
    '''
    [finished function:download_using_coroutine_pool in 3.46s]
    '''

if __name__ == '__main__':
    main()
```
从结果来看，使用协程池的效率还是略高一点。
