* 登录数据库
`mysql -uroot -p12345`  (12345为密码)

* 创建数据库
`create database senguocc;` (senguocc为数据库名)

* 查看当前有哪些数据库
`show databases;`

* 使用某个数据库
`use senguocc;`

* 显示当期数据库中的所有表
`show tables;`

* 命令行下忘记写分号
`输入'\c'再按回车.`

* 显示当前表的结构
`desc 表名;`

* 创建用户
`insert into mysql.user(Host,User,Password) values('localhost','newname',password('1234'));`

* 给用户赋权限
`grant all privileges on senguocc.* to monk@localhost identified by 'test123';`
(注:senguocc为数据库名,monk为用户名,'test123'为密码)

* 刷新系统权限表
`flush privileges;`
(注：每次为新创建的用户赋权限之前都要先刷新系统权限表才行)

* 修改root密码
```
update mysql.user set password = password('新密码') where User = 'root';
flush privileges;
```

* 修改用户密码
`mysqladmin -u用户名 -p旧密码 password 新密码;`

* 向数据库中导入.sql数据文件
`source filename.sql;`

* 将时间转换为时间戳(int 型)
`select unix_timestamp('2009-10-26 10-06-07');`

* 将时间戳转换为时间类型
`select from_unixtime(1256540102);`
注：时间戳表示从1970-1-1 0:0:0到现在时刻的秒数．
sqlalchemy用法：
```
data_timestamp = shop.create_date_timestamp
print(self.session.query(func.from_unixtime(data_timestamp)).scalar())　
```
（注：func后可以跟任何数据库支持的函数）

* sqlalchemy截取日期类型方法
```
data_trans = '2015-5-27'
data_result = self.session.query(func.date_format(data_trans,'%Y-%m-%d')).scalar()
print (data_result)
```
mysql用法：
```
select date_format('1997-10-04 22:23:00','%y %M %b %D %W %a %Y-%m-%d %H:%i:%s %r %T');
```
结果：
```
97 October Oct 4th Saturday Sat 1997-10-04 22:23:00 10:23:00 PM 22:23:00
```

* 使用senguocc的order表时候要加前缀senguocc.order，否则会出错，因为order为关键字．

* count用法小结
①统计所有宠物的数目：`select count(*) from pet;`
②统计每个主人所拥有宠物的数目：`select owner,count(*) from pet group by owner;`
③统计每种宠物的数目：`select species,count(*) from pet group by species;`
④统计每种性别的宠物的数量：`select sex,count(*) from pet group by sex;`
⑤统计每种宠物不同性别的数量：`select species,sex,count(*) from pet group by species,sex;`
⑥查询猫和狗不同性别的数目：`select species,sex,count(*) from pet where species = 'dog' or species = 'cat' group by species,sex;`

* 修改主键：先删除，再添加
```
alter table tablename drop primary key;
alter table tablename add primary key(id);(注：id 不能有重复的)
```

* 删除已经建好的表中的一列
`alter table tablename drop columnname;`

* sum函数用法
```
user 表：primary key(id,num)
id 　　　num
1              15
1              22
1              28
２　　　5
```

`select sum(num) from user where id = 1;`
输出：65

* 向表尾增加一列
`alter table tablename add column columnname int(10) not null default 0;`

往现有表name列后增加新的一列
`alter table tablename add column columnname int(10) not null default 0 after name;`

在表首增加一列
`alter table tablename add column columnname int(10) not null default 0 first;`

* mysql数据库中，假定有学生-成绩表grade，现在从其中查询成绩，如果及格则显示分数，如果不及格显示"不及格"
`select id,grades,case when grades < 60 then '不及格' when grades > 60 then grades end from grade;`

* 导出某数据库到sql文件（在系统命令行中执行该命令，而不是进入数据库中）
`mysqldump -u用户名 -p密码 数据库名 > 数据库名.sql`

* 查看当前用户
`select user();`
