> 声明：本系列文章参考了《MATLAB 8.X实战指南（R2014a中文版）》（清华大学出版社，赵小川等编著），仅用于个人学习总结和交流，禁止作为商业用途转载或使用。

每种编程语言都有各自特定的语法，其实很多编程语言的基础语法都是非常类似的，比如大多数（高级）编程语言都会包含如下几种语法元素：
* 变量
* 运算符
* 控制语句：判断语句、循环语句等
* 函数

Matlab也不例外，本文将会对Matlab的基础语法进行一个梳理。

注：本文中使用的Matlab是超精简版、免安装的Matlab 5.3绿色版本（[下载地址](http://pan.baidu.com/s/1c1N0Vb6)）

# 变量
### 变量命名规则
可以由英文字母、数字或下划线组成，但必须以**字母**开头。注意：变量名不要使用Matlab中的保留关键字。用`iskeyword`函数可以查看Matlab中所有的关键字。

### 变量作用域
有如下三种作用域的变量：
* 局部变量
每个函数（函数会在后面细讲）中定义的变量，只能在当前函数体内访问到。

* 全局变量
在函数体中用`global`关键字声明的变量，它的作用域是：所有的函数和Matlab工作空间。任何一个地方改变了全局变量的值，其他所有使用到它的地方的值都会随着改变。建议尽量少使用全局变量。

* 静态变量
在一个函数中可以使用`persistent`关键字声明一个静态变量，只要函数存在，静态变量就不会被清除。

# 运算符
Matlab的运算符包括：加减乘除四则运算、幂指对、逻辑运算符等。

# 判断语句
### if语句
* if-end语句
举个栗子：
```m
?if 1 + 1 == 2
     disp('1+1 is 2!');
end
1+1 is 2!
?
```

* if-else-end语句
用法与`if-end`语句类似，不再举例。

* if-elseif-end语句

* if-elseif-else-end语句
注：这里的`elseif`可以有多个。

### switch语句
举个栗子：
```m
?x = 'C';
?switch x
    case {'A','a'}
       r = '优秀'
    case {'B','b'}
       r = '良好'
    case {'C','c'}
       r = '一般'
    case {'D','d'}
       r = '及格'
    otherwise
       r = '不及格'
end

r =

一般
```
注：switch语句可以没有otherwise分支。

# 循环语句
### for语句
for语句的格式：
```m
for index = start:increment:end
    语句块
end
% 其中index为循环变量，start为循环起始值，end为循环终止值，increment为每次的增量，可以不写，默认为1。如果increment为负数，则循环会在start小于end的时候终止。
```
举个栗子，求1~100的累加和：
```m
?sum = 0;
?for i = 1 : 100
    sum = sum + i;
end
?disp(sum)
        5050
```

### while语句
在循环次数未知的时候，就不能用for语句了，这个时候可以使用while语句，语法格式：
```m
while 逻辑表达式
    语句块
end
```
举个栗子，用while语句来计算1~100的累加和：
```m
?i = 1;
?sum = 0;
?while i <= 100
    sum = sum + i;
    i = i + 1;
end
?disp(sum)
        5050
```

### continue语句
如果想跳过某次循环，可以使用continue语句，比如下面的栗子是计算1~10之间偶数的和：
```m
?sum = 0;
?for i = 1:10
    if mod(i,2) ~= 0
        continue
    end
    sum = sum + i;
end
?disp(sum)
    30
```

### break语句
用于终止循环。举个栗子，遍历1~10，遇到7就终止循环：
```m
?for i = 1:10
  if i == 7
    break;
  end
end
?disp(i)
     7
```

# 异常处理语句
当程序发生异常时，需要捕获异常并对异常进行处理，这个时候需要用到`try-catch`语句，基本语法格式：
```m
try
    语句块1
catch
    语句块2
end
% 如果语句块1发生异常，会跳到语句块2
```

# Matlab脚本文件（m文件）
和其他编程语言一样，比如Java的代码文件为java文件，C++的代码文件为cpp文件，Python的代码文件为py文件，Matlab也有自己的代码文件，是以`.m`作为后缀名的文件。

一个m文件可以看作是一堆代码语句的集合，在m文件中可以加注释，每一行代码中`%`后面的内容都是注释。

# 函数
Matlab的函数分为两种，一种叫m函数，也叫主函数，是定义在和函数同名的m文件中的函数，可以供外部（Matlab命令行窗口或者其他m文件）调用；另一种叫子函数，也是写在m文件中，但是只能供同一m文件中的主函数或其他子函数调用。

### m函数
m函数需要定义在与函数同名的m文件中，一个m函数具有独立的工作空间。一般由5部分组成：函数定义行、H1行（紧跟函数定义行后面一行的注释文本，也是用`lookfor 函数名`命令时候可以看到的文本）、帮助文本（注释文本，用于对函数的功能、输入参数、输出参数等信息进行说明）、函数体、注释。

Matlab带有m文件编辑器，可以在Matlab命令行中输入`edit`命令打开m文件编辑器，然后在其中就可以编辑m文件。当然，在记事本或notepad++中也是可以编辑m文件的，就好比既可以在Eclipse中写Java代码，如果你喜欢也可以在记事本或vim编辑器中写。

下面举一个栗子来说明m函数的定义方法：
```m
function result = myadd(num1,num2)
% myadd(num1,num2) 自定义加法函数，计算num1和num2的和
% 输入参数为两个数
% 输出参数为两个数的和
% 程序作者：m2fox
% 程序开发日期：2017-11-21
result = num1 + num2
```
把上面一段代码保存成一个m文件，命名为：myadd.m，保存，比如保存在了`D:\mylearn\`目录下。

然后要把`D:\mylearn\`这个路径添加为Matlab的执行路径（相当于环境变量），否则无法在命令行窗口中调用myadd函数。添加执行路径的方法是：
![](http://upload-images.jianshu.io/upload_images/8819542-0d948f8a85130c7e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![](http://upload-images.jianshu.io/upload_images/8819542-75c015d33f33276b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![](http://upload-images.jianshu.io/upload_images/8819542-4217fda51e70db63.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

把`D:\mylearn\`这个路径按照上述方法添加到执行路径后，就可以到Matlab命令行中输入`myadd(num1,num2)`命令来求两个数的和了，示例程序如下：
```m
?myadd(1,2);

result =

     3

?help myadd

  myadd(num1,num2) 自定义加法函数，计算num1和num2的和
  输入参数为两个数
  输出参数为两个数的和
  程序作者：m2fox
  程序开发日期：2017-11-21

?lookfor myadd
myadd.m: % myadd(num1,num2) 自定义加法函数，计算num1和num2的和
```
可以看到，求出了`1+2`的结果：3，然后用`help`和`lookfor`命令也显示出了定义函数时写的函数帮助文本。

### 子函数
在文件中，和文件名同名的函数称为m函数，也叫主函数；而在m文件中定义的其他函数，则称为子函数。要注意的是，子函数之内被当前m文件内部的主函数以及其他子函数调用，不能被外部调用。下面举一个子函数的栗子，还是在刚刚的`myadd.m`文件中定义：
```m
function result = myadd(num1,num2)
% myadd(num1,num2) 自定义加法函数，计算num1和num2的平方和
% 输入参数为两个数
% 输出参数为两个数的平方和
% 程序作者：m2fox
% 程序开发日期：2017-11-21
result = square(num1) + square(num2)

function s = square(x)
% 这是一个子函数，用于算一个数的平方
s = x ^ 2;
```

保存文件，再在Matlab命令行中输入调用`myadd`函数：
```
?myadd(1,2);

result =

     5
```

### 函数句柄和匿名函数
如果你接触过Python，会知道在Python中函数也是一种对象，可以将一个函数赋值给一个变量。在Python中也有lambda表达式支持的匿名函数。

类似的，Matlab中也有类似函数对象的函数句柄以及匿名函数。

* 函数句柄：`变量名 = @函数名`，经过这一句的定义之后，就可以用自己定义的变量名来调用这个函数了。

* 匿名函数：`变量名 = @(输入参数列表)(运算表达式)`

注：函数句柄和匿名函数在精简版Matlab 5.3中不支持，所以此处不再给出示例程序。

### 获取一个函数的输入参数数量
举例如下，修改`myadd.m`文件的内容并保存：
```m
function result = myadd(num1,num2)
% 如果输入的参数只有一个，就输出这个数的绝对值；如果输入的参数有两个，就输出这两个数的和
if (nargin == 1)  % 用nargin这个特殊变量来获取输入参数的个数
   result = abs(num1)
elseif (nargin == 2)
   result = num1 + num2
end
```

在Matlab命令行中调用`myadd`函数：
```
?myadd(-3);

result =

     3

?myadd(4,5);

result =

     9
```

# 几点实用编程技巧
### 计算函数用时
在任意代码段的开始和结束使用`tic`和`toc`语句对，可以计算这段代码的用时，编写一个名为`myadd.m`的m函数如下：
```m
function sum = myadd()
tic
s = 0;
for i = 1:1000000
   s = s + 1/i;
end
sum = s;
toc
```
在命令行中调用`myadd`函数：
```
?myadd

elapsed_time =

    1.1740


ans =

   14.3927
```
可以看到`myadd`函数用时1.174秒，结果为14.3927

### 用向量化的操作来代替循环操作
向量化的操作相比循环操作而言，在数据量大的时候性能将会显著提高。
比如对比如下两个函数：
```m
function result = myadd1()
tic
s = 0;
for i = 1:1000000
   s = s + 1/i;
end
result = s;
toc
```
```m
function result = myadd2()
tic
i = 1:1000000;
result = sum(1./i);
toc

```

分别调用myadd1、myadd2函数，结果对比如下：
```
?myadd1

elapsed_time =

    1.1740


ans =

   14.3927
?myadd2

elapsed_time =

    0.0200


ans =

   14.3927
```
可以看出，采用向量化的操作后，相比使用循环，同样的数据量的计算效率得到了几十倍的提升。

### 次数多的循环放在内层，次数少的循环放在外层
可以防止损耗过多程序性能。

### 大型矩阵预先定维
先使用`zeros`或`ones`函数对大型矩阵预先定维，将会显著降低程序耗时。
