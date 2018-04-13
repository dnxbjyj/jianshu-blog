本文主要介绍在python中如何使用MySQL数据库。

# 准备工作

### 安装mysql

* Linux (Ubuntu)

`apt-get install mysql-server`

安装完成之后在命令行中输入：`mysql -uroot -proot`，看是否能够成功登入MySQL命令行，如果能够成功登入，则说明安装成功。

* Windows

下载MSI安装包mysql-installer-community-5.7.19.0.msi安装，官网地址：https://dev.mysql.com/downloads/installer/

注：注意下载页面这样一句话：Note: MySQL Installer is 32 bit, but will install both 32 bit and 64 bit binaries.

也就是说32位版本和64位版本的安装包是二合一的。

下载之后打开一路Next安装即可，只需在有一步设置账号的时候设置好MySQL的登录用户名和密码即可（比如我设置的用户名/密码是：root/root）。

安装完成之后在命令行中输入：`mysql -uroot -proot`，看是否能够成功登入MySQL命令行，如果能够成功登入，则说明安装成功；如果提示找不到mysql命令，则还需要手工把mysql.exe的路径添加到环境变量，比如我的路径是：`C:\Program Files\MySQL\MySQL Server 5.7\bin`

### 安装MySQL-python驱动模块

* Linux (Ubuntu)

`pip install MySQL-python`

* Windows

Windows下直接用`pip install MySQL-python`命令安装会报错：_mysql.c(42) : fatal error C1083: Cannot open include file: 'config-win.h':No such file or directory

解决方法：

在命令行中输入`python`命令打开python控制台，查看本地安装的python是32位的还是64位的，然后根据本地python的位数来下载如下两个安装包的其中之一：

32位：MySQL-python-1.2.5.win32-py2.7.exe，下载地址：https://pan.baidu.com/s/1qYa5H4w

64位：MySQL-python-1.2.5.win-amd64-py2.7.exe，下载地址：https://pan.baidu.com/s/1qYa5H4w

在安装时可能还会遇到问题：python version 2.7 required which was not found in the registry

解决方法：下载register.py文件，并在命令行中用python命令执行该脚本即可，下载地址：https://pan.baidu.com/s/1mihz25M

### 验证安装是否成功

进入python交互式环境，输入：`import MySQLdb`,如果没有报错，则表明安装mysql及MySQL-python成功。

### 在virtualenv虚拟化环境中安装MySQL-python

如果日常使用的是virtualenv环境，因为virtualenv是相对独立的环境，所以还需要单独安装MySQL-python。

* Linux (Ubuntu)

`pip install MySQL-python`

* Windows

在主环境安装好MySQL-python后，进入python安装目录（如：C:\Python27）下的lib\site-packages目录下，找到如下四组文件/文件夹：

`MySQL_python-1.2.5-py2.7.egg-info`（文件夹）

`MySQLdb` （文件夹）

`_mysql_exceptions.py/_mysql_exceptions.pyc/_mysql_exceptions.pyo` （文件）

`_mysql.pyd`（文件）

然后把以上几个文件/文件夹都复制到virtualenv安装目录的lib\site-packages目录下。然后在virtualenv环境下进入pyton交互式环境，输入`import MySQLdb`验证是否成功。

### 预置mysql数据

* 在命令行中登录mysql（假如用户名/密码是：root/root）：`mysql -uroot -proot`

以下命令都是在登录mysql后的mysql命令行中执行的：

* 查看当前有哪些数据库：`show databases;`

* 创建一个新的名为info的数据库：`create database info;`

* 切换到info数据库：`use info;`

* 创建一个表person：`create table person(id int not null auto_increment primary key,name varchar(32),age int);`

* 查看当前有哪些表：`show tables;`

* 往person表中插入一些数据：

```bash
insert into person(name,age) values('Tom',18);
insert into person(name,age) values('John',23);
insert into person(name,age) values('Amy',15);
```

* 查询person表：`select * from person;`

```bash
mysql> select * from person;
+----+------+------+
| id | name | age  |
+----+------+------+
|  1 | Tom  |   18 |
|  2 | John |   23 |
|  3 | Amy  |   15 |
+----+------+------+
3 rows in set (0.00 sec)
```

# 用python操作数据库

### 连接mysql

导入包：


```python
import MySQLdb
```

获取数据库连接对象：


```python
conn = MySQLdb.connect(user = 'root',passwd = 'root',host = '127.0.0.1')
```

注：MySQLdb.connect()函数可以接收的常用的几个参数：

* host：连接的服务器主机名，默认为本机（localhost）

* user：数据库用户名，默认为当前用户

* passwd：用户登录密码，无默认值

* db：连接的数据库名，无默认值

* read_default_file：使用指定的mysql配置文件

* port：连接端口，默认为3306

* connect_timeout：连接超时时间，单位为秒

获取游标（相当于一个指针）：


```python
cur = conn.cursor()
```

设置当前数据库为info：


```python
conn.select_db('info')
```

注：不建议在python中操作数据库创建表。

### 执行sql语句插入数据

假如向person表中插入数据：


```python
sql = 'insert into person(name,age) values("Zhangsan",34)'  # 组装sql
cur.execute(sql)  # 执行sql
conn.commit()  # 提交，如果没有这句，更改不会生效
cur.close()
conn.close()  # 用完之后最好关闭游标和连接对象
```

此时去mysql中，进入info数据库，查询：`select * from person;`，结果如下：

```bash
mysql> select * from person;
+----+----------+------+
| id | name     | age  |
+----+----------+------+
|  1 | Tom      |   18 |
|  2 | John     |   23 |
|  3 | Amy      |   15 |
|  4 | Zhangsan |   34 |
+----+----------+------+
4 rows in set (0.00 sec)
```

发现成功插入一条数据。

### 批量插入数据

使用占位符和列表：


```python
sql = 'insert into person(name,age) values(%s,%s)'
cur.execute(sql,('Lisi',23))  # 插入一条数据
persons = [('Wangwu',32),('Zhaoliu',12),('Tianqi',45)]
cur.executemany(sql,persons)  # 插入多条
conn.commit()  # 提交
```

此时去mysql中，进入info数据库，查询：`select * from person;`，结果如下：

```bash
mysql> select * from person;
+----+----------+------+
| id | name     | age  |
+----+----------+------+
|  1 | Tom      |   18 |
|  2 | John     |   23 |
|  3 | Amy      |   15 |
|  4 | Zhangsan |   34 |
|  5 | Lisi     |   23 |
|  6 | Wangwu   |   32 |
|  7 | Zhaoliu  |   12 |
|  8 | Tianqi   |   45 |
+----+----------+------+
8 rows in set (0.07 sec)
```

### 删除数据


```python
sql = 'delete from person where name = "Tianqi"'
cur.execute(sql)
conn.commit()
```

```bash
mysql> select * from person;
+----+----------+------+
| id | name     | age  |
+----+----------+------+
|  1 | Tom      |   18 |
|  2 | John     |   23 |
|  3 | Amy      |   15 |
|  4 | Zhangsan |   34 |
|  5 | Lisi     |   23 |
|  6 | Wangwu   |   32 |
|  7 | Zhaoliu  |   12 |
+----+----------+------+
7 rows in set (0.00 sec)
```

### 更新数据


```python
sql = 'update person set age = 88 where name = "Zhaoliu"'
cur.execute(sql)
conn.commit()
```

```bash
mysql> select * from person;
+----+----------+------+
| id | name     | age  |
+----+----------+------+
|  1 | Tom      |   18 |
|  2 | John     |   23 |
|  3 | Amy      |   15 |
|  4 | Zhangsan |   34 |
|  5 | Lisi     |   23 |
|  6 | Wangwu   |   32 |
|  7 | Zhaoliu  |   88 |
+----+----------+------+
7 rows in set (0.00 sec)
```

### 查询数据


```python
sql = 'select * from person'
cur.execute(sql)
# 取查到的所有结果，并把游标移到结尾
print '【Output 1】'
print cur.fetchall()

# 把游标移到开头
cur.scroll(0,'absolute')

# 取查到的前n条数据，并把游标移到第n+1位置
print '【Output 2】'
print cur.fetchmany(3)

# 把游标移到开头
cur.scroll(0,'absolute')

# 取查到的一条数据，并把游标向后移动一位
print '【Output 3】'
print cur.fetchone()
print cur.fetchone()
```

    【Output 1】
    ((1L, 'Tom', 18L), (2L, 'John', 23L), (3L, 'Amy', 15L), (4L, 'Zhangsan', 34L), (5L, 'Lisi', 23L), (6L, 'Wangwu', 32L), (7L, 'Zhaoliu', 88L))
    【Output 2】
    ((1L, 'Tom', 18L), (2L, 'John', 23L), (3L, 'Amy', 15L))
    【Output 3】
    (1L, 'Tom', 18L)
    (2L, 'John', 23L)
