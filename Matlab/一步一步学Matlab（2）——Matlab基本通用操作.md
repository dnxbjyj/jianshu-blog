> 声明：本系列文章参考了《MATLAB 8.X实战指南（R2014a中文版）》（清华大学出版社，赵小川等编著），仅用于个人学习总结和交流，禁止作为商业用途转载或使用。

在上一篇中对Matlab做了一个初步的了解，本文继续来零距离亲身体验Matlab，来感受一下Matlab的一些基本、通用的操作。

# 命令行窗口
一打开Matlab就能看到命令行窗口，在我所用的这个精简版的Matlab界面上，命令行的每一行都是以问号"?"开头的，在问号后面可以输入任何命令、算式、表达式、代码。比如在第一篇中讲到的输出"Hello World"，其中的`disp`就是内置的一个函数，用于输出一些东西到屏幕上：
![](http://upload-images.jianshu.io/upload_images/8819542-da4282aa0ad6c06e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



## 常用的命令或操作

命令|命令说明
:-:|:--
help|查看一个操作或函数的详情
clc|清除工作窗口中所有显示的内容
disp|显示变量或文字内容
whos|显示当前内存中有哪些变量
clear|清理内存变量
lookfor|查找某个关键字对应的M文件
dos 函数名|查看某个函数的帮助文档
demo/demos|查看Matlab内置的示例程序

下面对上述命令一一进行举例介绍。

## 常用命令举例介绍

* help：查看一个函数或操作的详情。

比如我们想看看disp函数的详细用法是什么，就可以这样：

```
?help disp

 DISP Display array.
    DISP(X) displays the array, without printing the array name.  In
    all other ways it's the same as leaving the semicolon off an
    expression except that empty arrays don't display.
 
    If X is a string, the text is displayed.
 
    See also INT2STR, NUM2STR, SPRINTF, RATS, FORMAT.

 Overloaded methods
    help inline/disp.m
    help sym/disp.m
    help network/disp.m
```

* disp：显示变量或文本内容。

举例：

```
?disp(1+2)
     3

?disp('hi')
hi
```

* whos：显示当前内存中有哪些变量。

比如：当前内存中有a和b两个变量，a是一个数字，b是一个数组，那么就可以用`whos a`或`whos b`或`whos`来查看a和b的详情：

```
?a=1+2;
?b=[1,2,3];
?whos a
  Name      Size         Bytes  Class

  a         1x1              8  double array

Grand total is 1 elements using 8 bytes

?whos b
  Name      Size         Bytes  Class

  b         1x3             24  double array

Grand total is 3 elements using 24 bytes

?whos
  Name      Size         Bytes  Class

  a         1x1              8  double array
  b         1x3             24  double array

Grand total is 4 elements using 32 bytes
```

* celar：清理内存变量。

比如当前内存中有a和b两个变量，我不想再用a和b了，那么可以这样把a和b从内存中清理掉：

```
?whos
  Name      Size         Bytes  Class

  a         1x1              8  double array
  b         1x3             24  double array

Grand total is 4 elements using 32 bytes

?clear
?whos
?disp(a)
??? Undefined function or variable 'a'.
```

* lookfor：查找某个关键字对应的M文件（M文件是啥会在后面讲）。

比如想查看和sin函数对应的所有M文件：

```
?lookfor sin
SUBSINDEX Subscript index.
java.m: % Using Java from within MATLAB
ISINF  True for infinite elements.
ACOS   Inverse cosine.
ACOSH  Inverse hyperbolic cosine.
ASIN   Inverse sine.
ASINH  Inverse hyperbolic sine.
COS    Cosine.
COSH   Hyperbolic cosine.
SIN    Sine.
...
```

* dos：查看某个函数的帮助文档。

比如我想看disp函数的帮助文档，那么可以这样看：

```
?doc disp
??? Error using ==> doc
Could not locate help system home page.
Please make sure the help system files are installed.
```

可以发现报错了，那是因为我用的是精简版的Matlab，没有安装帮助文档系统。当然在完整版Matlab上是可以看到的。

* demo/demos：查看Matlab的简单的示例程序。

比如：
![](http://upload-images.jianshu.io/upload_images/8819542-e09adc58c9add147.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



可以看出在输入`demo`命令后，就弹出了一个示例程序窗口，可以跟着示例程序快速学习入门。

# 常用语法标点

Matlab有一些特殊的语法标点，掌握之后在写代码的时候会更加游刃有余，罗列如下：

标点|说明
:-:|:--
;|区分行或不显示命令的运行结果
{}|构造单元数组的界定符
%|注释符号，在%以后直到行末尾的字符都属于注释，不产生实际作用
!|调用DOS窗口命令

下面是对上面几个语法标点的用法示例：

```
?a = 1+2

a =

     3

?a = 1+2;
?b = {[1,2]}

b = 

    [1x2 double]

?c = 1  %这里是一些注释，你想写什么就写什么

c =

     1

?!dir  %这里调用DOS窗口命令行命令：dir，来显示当前目录下有哪些文件
 驱动器 D 中的卷是 软件 
 卷的序列号是 0003-558E 
 
 D:\coding\matlab\installer\MATLAB\bin 的目录 
 
找不到文件 
?
```
