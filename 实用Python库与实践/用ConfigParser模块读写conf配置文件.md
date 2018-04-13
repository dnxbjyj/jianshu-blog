> 本文讲述的核心库：`ConfigParser`

ConfigParser是Python内置的一个读取配置文件的模块，用它来读取和修改配置文件非常方便，本文介绍一下它的基本用法。

## 数据准备

假设当前目录下有一个名为`sys.conf`的配置文件，其内容如下：

```bash
[db]
db_host=127.0.0.1
db_port=22
db_user=root
db_pass=root123

[concurrent]
thread  =    10
processor =    20
```

注：配置文件中，各个配置项其实是用等号'='隔开的键值对，这个等号两边如果有空白符，在处理的时候都会被自动去掉。但是key之前不能存在空白符，否则会报错。

## 配置文件介绍

配置文件即conf文件，其文件结构多为键值对的文件结构，比如上面的sys.conf文件。

conf文件有2个层次结构，`[]`中的文本是section的名称，下面的键值对列表是item，代表每个配置项的键和值。

注：配置文件也可以是`.ini`等其他后缀名的文件，只要是文本文件即可，配置文件中可用`#`号作为注释符，每行`#`后面的文本都是注释。

## 初始化ConfigParser实例


```python
import ConfigParser
```


```python
cf = ConfigParser.ConfigParser()
cf.read('./sys.conf')
```

## 读取所有的section列表

section即`[]`中的内容。


```python
s = cf.sections()
print '【Output】'
print s
```

    【Output】
    ['db', 'concurrent']
    

## 读取指定section下options key列表

options即某个section下的每个键值对的key.


```python
opt = cf.options('concurrent')
print '【Output】'
print opt
```

    【Output】
    ['thread', 'processor']
    

## 获取指定section下的键值对字典列表


```python
items = cf.items('concurrent')
print '【Output】'
print items
```

    【Output】
    [('thread', '10'), ('processor', '20')]
    

## 按照指定数据类型读取配置值

cf对象有get()、getint()、getboolean()、getfloat()四种方法来读取不同数据类型的配置项的值。


```python
db_host = cf.get('db','db_host')
db_port = cf.getint('db','db_port')
thread = cf.getint('concurrent','thread')

print '【Output】'
print db_host,db_port,thread
```

    【Output】
    127.0.0.1 22 10
    

## 修改某个配置项的值

比如要修改一下数据库的密码，可以这样修改：


```python
cf.set('db','db_pass','newpass')
# 修改完了要写入才能生效
with open('sys.conf','w') as f:
    cf.write(f)
```

## 添加一个section


```python
cf.add_section('log')
cf.set('log','name','mylog.log')
cf.set('log','num',100)
cf.set('log','size',10.55)
cf.set('log','auto_save',True)
cf.set('log','info','%(bar)s is %(baz)s!')

# 同样的，要写入才能生效
with open('sys.conf','w') as f:
    cf.write(f)
```

执行上面代码后，sys.conf文件多了一个section，内容如下：

```bash
[log]
name = mylog.log
num = 100
size = 10.55
auto_save = True
info = %(bar)s is %(baz)s!
```

## 移除某个section


```python
cf.remove_section('log')

# 同样的，要写入才能生效
with open('sys.conf','w') as f:
    cf.write(f)
```

## 移除某个option


```python
cf.remove_option('db','db_pass')

# 同样的，要写入才能生效
with open('sys.conf','w') as f:
    cf.write(f)
```
