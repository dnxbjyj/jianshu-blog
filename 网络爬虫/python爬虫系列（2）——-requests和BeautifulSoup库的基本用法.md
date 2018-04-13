本文主要介绍python爬虫的两大利器：requests和BeautifulSoup库的基本用法。

# 1. 安装requests和BeautifulSoup库

可以通过3种方式安装：

* `easy_install`
* `pip`
* 下载源码手动安装

这里只介绍pip安装方式：

`pip install requests`
`pip install BeautifulSoup4`

# 2. requests基本用法示例

```python
# coding:utf-8
import requests

# 下载新浪新闻首页的内容
url = 'http://news.sina.com.cn/china/'
# 用get函数发送GET请求，获取响应
res = requests.get(url)
# 设置响应的编码格式utf-8（默认格式为ISO-8859-1），防止中文出现乱码
res.encoding = 'utf-8'

print type(res)
print res
print res.text

# 输出：
'''
<class 'requests.models.Response'>
<Response [200]>
<!DOCTYPE html>
<!-- [ published at 2017-04-19 23:30:28 ] -->
<html>
<head>
<meta http-equiv="Content-type" content="text/html; charset=utf-8" />
<title>国内新闻_新闻中心_新浪网</title>
<meta name="keywords" content="国内时政,内地新闻">
...
'''
```

下面将上面获取到的网页html内容写入到文件中，这里有一点需要注意的是：python是调用ASCII编码解码程序去处理字符流的，当字符不属于ASCII范围时会抛异常（`ordinal not in range(128)`），所以要提前设置程序的默认编码：

```python
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
```

然后再将响应的html内容存入文件中：

```python
with open('content.txt','w+') as f:
    f.write(res.text)
```

# 3. BeautifulSoup基本用法

## 1. 自定义测试html

```python
html = '''
<html>
    <body>
        <h1 id="title">Hello World</h1>
        <a href="#link1" class="link">This is link1</a>
        <a href="#link2" class="link">This is link2</a>
    </body>
</html>
'''
```

## 2. 从html文本中获取soup


```python
from bs4 import BeautifulSoup
# 这里指定解析器为html.parser（python默认的解析器），指定html文档编码为utf-8
soup = BeautifulSoup(html,'html.parser',from_encoding='utf-8')
print type(soup)

# 输出：<class 'bs4.BeautifulSoup'>
```

## 3. soup.select()函数用法

### (1) 获取指定标签的内容


```python
header = soup.select('h1')
print type(header)
print header
print header[0]
print type(header[0])
print header[0].text

# 输出：
'''
<type 'list'>
[<h1 id="title">Hello World</h1>]
<h1 id="title">Hello World</h1>
<class 'bs4.element.Tag'>
Hello World
'''
```


```python
alinks = soup.select('a')
print [x.text for x in alinks]

# 输出：[u'This is link1', u'This is link2']
```

### (2) 获取指定id的标签的内容（用'#'）


```python
title = soup.select('#title')
print type(title)
print title[0].text

# 输出：
'''
<type 'list'>
Hello World
'''
```

### (3) 获取指定class的标签的内容（用'.'）


```python
alinks = soup.select('.link')
print [x.text for x in alinks]

# 输出：[u'This is link1', u'This is link2']
```

### (4) 获取a标签的链接（href属性值）


```python
print alinks[0]['href']

# 输出：#link1
```

### (5) 获取一个标签下的所有子标签的text


```python
body = soup.select('body')[0]
print body.text

# 输出：
'''

Hello World
This is link1
This is link2
'''
```

### (6) 获取不存在的标签


```python
aa = soup.select('aa')
print aa

# 输出：[]
```

### (7) 获取自定义属性值


```python
html2 = '<a href="www.test.com" qoo="123" abc="456">This is a link.</a>'
soup2 = BeautifulSoup(html2,'html.parser')
alink = soup2.select('a')[0]
print alink['qoo']
print alink['abc']

# 输出：
'''
123
456
'''
```

## 4. soup.find()和soup.find_all()函数用法

### (1) find()和find_all()函数原型：

find和find_all函数都可根据多个条件从html文本中查找标签对象，只不过find的返回对象类型为`bs4.element.Tag`，为查找到的第一个满足条件的Tag；而find_all的返回对象为`bs4.element.ResultSet`（实际上就是Tag列表）,这里主要介绍find函数，find_all函数类似。

`find(name=None, attrs={}, recursive=True, text=None, **kwargs)`
注：其中name、attrs、text的值都支持正则匹配。

`find_all(name=None, attrs={}, recursive=True, text=None, limit=None, **kwargs)`
注：其中name、attrs、text的值都支持正则匹配。

### (2) find函数的用法示例


```python
html = '<p><a href="www.test.com" class="mylink1 mylink2">this is my link</a></p>'
soup = BeautifulSoup(html,'html.parser')
a1 = soup.find('a')
print type(a1)
# 输出：<class 'bs4.element.Tag'>

print a1.name
print a1['href']
print a1['class']
print a1.text
# 输出：
'''
a
www.test.com
[u'mylink1', u'mylink2']
this is my link
'''
```


```python
# 多个条件的正则匹配：
import re
a2 = soup.find(name = re.compile(r'\w+'),class_ = re.compile(r'mylink\d+'),text = re.compile(r'^this.+link$'))
# 注：这里的class属性之所以写成'class_'，是为了防止和python关键字class混淆，其他属性名写正常的名就行，不用这样特殊处理
print a2

# 输出：
'''
<a class="mylink1 mylink2" href="www.test.com">this is my link</a>
'''
```

```python
# find函数的链式调用
a3 = soup.find('p').find('a')
print a3

# 输出：
'''
<a class="mylink1 mylink2" href="www.test.com">this is my link</a>
'''
```

```python
# attrs参数的用法
# 注：支持正则匹配属性值（包括自定义属性）
import re
html = '<div class="myclass" my-attr="123abc"></div><div class="myclass" my-attr="abc">'
soup = BeautifulSoup(html,'html.parser')
div = soup.find('div',attrs = {'class':'myclass','my-attr':re.compile(r'\d+\w+')})
print div

# 输出：
'''
<div class="myclass" my-attr="123abc"></div>
'''
```

# 4. 网络爬虫基本架构
![](http://upload-images.jianshu.io/upload_images/8819542-a5ecb759e395944b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


# 5. 补充

## 1. 代理访问

有时候为了避免封IP，或者在某些公司内网访问外网时候，需要用到代理服务器发送请求，代理的用法示例：

```python
import requests
proxies = {'http':'http://proxy.test.com:8080','https':'http://proxy.test.com:8080'}  # 其中proxy.test.com即为代理服务器的地址
url = 'https://www.baidu.com'  # 这个url为要访问的url
resp = requests.get(url,proxies = proxies)
```

如果代理服务器需要账号、密码，则可以这样写proxies：

```python
proxies = {'http':'http://{username}:{password}@proxy.test.com:8080','https':'http://{username}:{password}@proxy.test.com:8080'} 
```

## 2. 向https的url发送请求

有时候向https的url发送请求会报错：`ImportError:no module named certifi.`

解决方法：在发送请求时关闭校验：`verify = False`，如：


```python
resp = requests.get('https://test.com',verify = False)
```

注：也可通过在headers中传相关鉴权参数来解决此问题。

## 3. httpbin.org

httpbin.org是requests库的作者开发的一个网站，可以专门用来测试requests库的各种功能，其页面如下：
![](http://upload-images.jianshu.io/upload_images/8819542-32fa15d8f1285016.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

但httpbin.org的服务器在国外，访问速度比较慢。所以需要在本地搭建一个该网站的镜像，方法如下：

* 前提：安装好requests库，才能基于该网站测试requests库的功能。
* `pip install gunicorn httpbin`
* `gunicorn httpbin:app`
* 浏览器输入：127.0.0.1:8000,即可访问。

注：以上步骤在windows下会报错：缺少模块`pwd.fcanl`，在linux下没问题。

## 4. requests库官方文档

http://docs.python-requests.org/en/master/
