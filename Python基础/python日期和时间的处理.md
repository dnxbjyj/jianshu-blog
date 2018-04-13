总结一下python中对日期和时间的常用处理方法。

# 准备


```python
import time,datetime
```

# 常用操作

### 输出当前的日期时间

方式一：


```python
now = time.localtime()

print '【Output】'
print type(now)
print now
print now[:3]
```

    【Output】
    <type 'time.struct_time'>
    time.struct_time(tm_year=2017, tm_mon=8, tm_mday=21, tm_hour=23, tm_min=15, tm_sec=42, tm_wday=0, tm_yday=233, tm_isdst=0)
    (2017, 8, 21)
    

输出当前时间戳（单位：秒）：


```python
print '【Output】'
print time.time()
```

    【Output】
    1503329021.99
    

方式二：


```python
now = datetime.datetime.now()
print '【Output】'
print now.strftime('%Y-%m-%d %H:%M:%S')
```

    【Output】
    2017-08-21 23:23:46
    

### 格式化输出当前时间


```python
t = time.localtime()
print '【Output】'
print time.strftime('%Y-%m-%d %H:%M:%S',t)
time.sleep(2)
print time.strftime('%Y-%m-%d %H:%M:%S')  # 如果不指定时间，输出的就是当前时间
```

    【Output】
    2017-08-21 23:17:57
    2017-08-21 23:17:59
    

附：格式化字符串总结

* %a  英文星期简称
* %A  英文星期全称
* %b  英文月份简称
* %B  英文月份全称
* %c  本地日期时间
* %d  日期，1~31
* %H  小时，0~23
* %I  小时，0~12
* %m  月，01~12
* %M  分钟，0~59
* %S  秒，0~59
* %j  年中当天的天数
* %w  星期数，1~7
* %W  年中的第几周
* %x  当天日期，格式：01/31/17
* %X  本地的当天时间
* %y  年份，00~99
* %Y  年份完整拼写

### 字符串转为日期时间对象


```python
t = time.strptime('2000-1-1 10:00','%Y-%m-%d %H:%M')  # 注：前后格式要保持一致，否则转换会出错
print '【Output】'
print type(t)
print t
```

    【Output】
    <type 'time.struct_time'>
    time.struct_time(tm_year=2000, tm_mon=1, tm_mday=1, tm_hour=10, tm_min=0, tm_sec=0, tm_wday=5, tm_yday=1, tm_isdst=-1)
    

### 构造datetime对象


```python
dt = datetime.datetime(2010,1,1,23)
print '【Output】'
print type(dt)
print dt
```

    【Output】
    <type 'datetime.datetime'>
    2010-01-01 23:00:00
    
注：**月份的数值是从1开始的。**

### 将struct_time对象转为时间戳（秒）


```python
now = time.localtime()
timestamp = time.mktime(now)
print '【Output】'
print timestamp
```

    【Output】
    1503329307.0
    

### 将时间戳（秒）转为struct_time对象


```python
timestamp = 1480000000
print '【Output】'
print time.localtime(timestamp)
```

    【Output】
    time.struct_time(tm_year=2016, tm_mon=11, tm_mday=24, tm_hour=23, tm_min=6, tm_sec=40, tm_wday=3, tm_yday=329, tm_isdst=0)
    
### 求一个日期n天之后（或之前）的日期
```
In [10]: d1 = datetime.datetime(2012,4,15)

In [11]: d1
Out[11]: datetime.datetime(2012, 4, 15, 0, 0)

# 求2012-4-15后80天的日期
In [12]: d2 = d1 + datetime.timedelta(days = 80)

In [13]: d2
Out[13]: datetime.datetime(2012, 7, 4, 0, 0)

# 天数差值可以是一个负数，表示求一个日期之前n天的日期
In [21]: d2 = d1 + datetime.timedelta(days = -1)

In [23]: d2
Out[23]: datetime.datetime(2012, 4, 14, 0, 0)
```

### 求两个日期之间相差的天数
```
In [24]: d1 = datetime.datetime(2012,4,15)

In [25]: d2 = datetime.datetime(2012,4,18)

In [26]: d2 - d1
Out[26]: datetime.timedelta(3)

In [27]: d1 - d2
Out[27]: datetime.timedelta(-3)

In [28]: d1 = datetime.datetime(2012,4,15,11,0,0)

In [29]: d2 = datetime.datetime(2012,4,18,15,0,0)

# 这里的3表示相差3天，14400表示再多出来的秒数
In [30]: d2-d1
Out[30]: datetime.timedelta(3, 14400)
```
