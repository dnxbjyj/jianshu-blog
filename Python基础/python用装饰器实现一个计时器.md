直接上代码：

```python
import time
from functools import wraps

# 定义装饰器
def fn_timer(function):
    @wraps(function)
    def function_timer(*args,**kwargs):
        t0 = time.time()
        result = function(*args,**kwargs)
        t1 = time.time()
        print '[finished {func_name} in {time:.2f}s]'.format(func_name = function.__name__,time = t1 - t0)
        return result
    return function_timer

# 使用装饰器来计时
@fn_timer
def download(url):
    # 模拟下载3秒
    print 'start to download from {0}...'.format(url)
    time.sleep(3)
    print 'download finished!'

download('www.baidu.com')
```

    start to download from www.baidu.com...
    download finished!
    [finished download in 3.00s]
