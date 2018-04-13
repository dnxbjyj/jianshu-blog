在编写爬虫爬取数据的时候，因为很多网站都有反爬虫措施，所以很容易被封IP，就不能继续爬了。在爬取大数据量的数据时更是瑟瑟发抖，时刻担心着下一秒IP可能就被封了。

本文就如何解决这个问题总结出一些应对措施，这些措施可以单独使用，也可以同时使用，效果更好。

# 伪造User-Agent

在请求头中把`User-Agent`设置成浏览器中的`User-Agent`，来伪造浏览器访问。比如：

```python
headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
resp = requests.get(url,headers = headers)
```
还可以先收集多种浏览器的`User-Agent`，每次发起请求时随机从中选一个使用，可以进一步提高安全性：
```python
In [7]: import requests,random

In [8]: user_agents = ['User-Agent:Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1','User-Agent:Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, li
   ...: ke Gecko) Version/5.1 Safari/534.50','User-Agent:Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11']

In [9]: def get_html(url):
   ...:     headers = {'User-Agent':random.choice(user_agents)}
   ...:     resp = requests.get(url,headers = headers)
   ...:     return resp.text

```
注：一些常见浏览器的`User-Agent`可参见：https://blog.csdn.net/qianxing111/article/details/79415857

# 在每次重复爬取之间设置一个随机时间间隔

```python
# 比如：
time.sleep(random.randint(0,3))  # 暂停0~3秒的整数秒，时间区间：[0,3]
# 或：
time.sleep(random.random())  # 暂停0~1秒，时间区间：[0,1)
```

# 伪造cookies

若从浏览器中可以正常访问一个页面，则可以将浏览器中的cookies复制过来使用，比如：

```python
cookies = dict(uuid='b18f0e70-8705-470d-bc4b-09a8da617e15',UM_distinctid='15d188be71d50-013c49b12ec14a-3f73035d-100200-15d188be71ffd')
resp = requests.get(url,cookies = cookies)
```

```python
# 把浏览器的cookies字符串转成字典
def cookies2dict(cookies):
    items = cookies.split(';')
    d = {}
    for item in items:
        kv = item.split('=',1)
        k = kv[0]
        v = kv[1]
        d[k] = v
    return d
```

注：用浏览器cookies发起请求后，如果请求频率过于频繁仍会被封IP，这时可以在浏览器上进行相应的手工验证（比如点击验证图片等），然后就可以继续正常使用该cookies发起请求。

# 使用代理

可以换着用多个代理IP来进行访问，防止同一个IP发起过多请求而被封IP，比如：

```python
proxies = {'http':'http://10.10.10.10:8765','https':'https://10.10.10.10:8765'}
resp = requests.get(url,proxies = proxies)
# 注：免费的代理IP可以在这个网站上获取：http://www.xicidaili.com/nn/
```

# 附：GitHub上的一个"反反爬虫"项目
道高一尺魔高一丈，你有反爬虫措施，那我也有各种"反反爬虫"的措施，GitHub上就有一位大神专门整理了一个这样的项目：[Anti-Anti-Spider](https://github.com/luyishisi/Anti-Anti-Spider)，可以研究一下。
