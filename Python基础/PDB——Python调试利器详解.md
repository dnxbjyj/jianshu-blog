> python 2.7 pdb官方文档：https://docs.python.org/2.7/library/pdb.html
 
pdb是ptyhon内置的一个调试库，是调试python代码的好帮手，本文是对其用法的详细介绍。

# QuickStart
### 待调试的代码内容
文件名：test.py：
```python
# coding:utf-8
import pdb
s1 = 'aaa'
pdb.set_trace()
s2 = 'bbb'
s3 = 'ccc'
pdb.set_trace()
s = s1 + s2 + s3
print s
```

可以看出在代码的第4、7行分别打了一个断点，使用的是`pdb.set_trace()`函数。

### 开始调试

在和代码文件相同路径下打开命令行窗口，输入命令：`python test1.py`

接着就进入了调试状态：
```bash
(.env) E:\code\python-basic\tools\pdb\sample>python test1.py
> e:\code\python-basic\tools\pdb\sample\test1.py(5)<module>()
-> s2 = 'bbb'
(Pdb)
```

可以看出直接执行到了第一个断点所在的下一行，并停在了这里。

这时可以执行命令：`n`进行下一步：
```
(Pdb) n
> e:\code\python-basic\tools\pdb\sample\test1.py(6)<module>()
-> s3 = 'ccc'
(Pdb)
```

使用`p <变量名>`命令打印已经出现过的变量的值：
```
(Pdb) p s1
'aaa'
(Pdb) p s2
'bbb'
(Pdb) p s3
*** NameError: NameError("name 's3' is not defined",)
(Pdb)
```

因为当前变量s3还没有被赋值，所以打印s3的时候提示`NameError`异常。 

使用`l`命令打印出当前的代码段：
```
(Pdb) l
  1     # coding:utf-8
  2     import pdb
  3     s1 = 'aaa'
  4     pdb.set_trace()
  5     s2 = 'bbb'
  6  -> s3 = 'ccc'
  7     pdb.set_trace()
  8     s = s1 + s2 + s3
  9     print s
[EOF]
(Pdb)
```

退出调试：`q`命令
```
(Pdb) q
Traceback (most recent call last):
  File "test1.py", line 6, in <module>
    s3 = 'ccc'
  File "test1.py", line 6, in <module>
    s3 = 'ccc'
  File "d:\programs\python27\Lib\bdb.py", line 49, in trace_dispatch
    return self.dispatch_line(frame)
  File "d:\programs\python27\Lib\bdb.py", line 68, in dispatch_line
    if self.quitting: raise BdbQuit
bdb.BdbQuit

(.env) E:\code\python-basic\tools\pdb\sample>
```

# PDB调试的另一种方式

QuickStart中使用的调试方式不够优雅，因为是通过修改代码的方式打断点的，用起来不太方便。那么能不能动态打断点呢？答案是当然可以，请接着往下看。

### 准备待调试的代码

删除掉QuickStart中代码中的`pdb.set_trace()`，剩下的代码如下：
文件名：test2.py
```python
# coding:utf-8
s1 = 'aaa'
s2 = 'bbb'
s3 = 'ccc'
s = s1 + s2 + s3
print s
```

### 开始调试

在test2.py相同路径下打开命令行，输入命令：`python -m pdb test2.py`
```
(.env) E:\code\python-basic\tools\pdb\sample>python -m pdb test2.py
> e:\code\python-basic\tools\pdb\sample\test2.py(2)<module>()
-> s1 = 'aaa'
(Pdb) l
  1     # coding:utf-8
  2  -> s1 = 'aaa'
  3     s2 = 'bbb'
  4     s3 = 'ccc'
  5     s = s1 + s2 + s3
  6     print s
[EOF]
(Pdb)
```

可以看到当前代码中我们还没有打任何断点，代码默认停在了第1行。

执行一个命令`n`：
```
(Pdb) n
> e:\code\python-basic\tools\pdb\sample\test2.py(3)<module>()
-> s2 = 'bbb'
(Pdb) l
  1     # coding:utf-8
  2     s1 = 'aaa'
  3  -> s2 = 'bbb'
  4     s3 = 'ccc'
  5     s = s1 + s2 + s3
  6     print s
[EOF]
(Pdb)
```

可以看到单步执行到了下一行。

如果我们想在第5行打一个断点，该怎么打呢？用`b <行号>`命令在某一行打一个断点：
```
(Pdb) b 5
Breakpoint 1 at e:\code\python-basic\tools\pdb\sample\test2.py:5
(Pdb) l
[EOF]
(Pdb) n
> e:\code\python-basic\tools\pdb\sample\test2.py(4)<module>()
-> s3 = 'ccc'
(Pdb) l
  1     # coding:utf-8
  2     s1 = 'aaa'
  3     s2 = 'bbb'
  4  -> s3 = 'ccc'
  5 B   s = s1 + s2 + s3
  6     print s
[EOF]
(Pdb)
```

这样就成功地在第5行打了一个断点。

查看当前打了哪些断点：`b`命令
```
(Pdb) b
Num Type         Disp Enb   Where
1   breakpoint   keep yes   at e:\code\python-basic\tools\pdb\sample\test2.py:5
(Pdb)
```

# PDB调试命令汇总

### 高级命令

以上的示例只是展示了最简单的顺序结构的代码的调试方法，而实际应用中遇到的大多数代码都有着较为复杂的逻辑结构，比如循环结构、分支结构、调用函数、调用其他模块的函数、使用类和对象等等。

针对这些场景还有很多更高级的调试命令，其实掌握了前面的几个简单的命令的用法后，下面的这些更高级的命令就都很容易上手了，多用几遍就能很快掌握了。

命令|命令全称|功能
---|---|---
h|help|查看帮助
n|next|执行下一条语句
s|step|执行下一条语句，如果是函数，则会执行到函数的第一句
b|break|列出当前的所有断点
b <行号>|/|在某一行打一个断点
b <文件名>:<行号>|/|在某个文件的某行打一个断点
b <函数名>|/|在某个函数的第一行打一个断点
cl|clear|清除所有断点
cl n1 n2 ...|/|清除编号为n1、n2...的断点
cl <行号> |/|清除某行的断点
cl <文件名>:<行号>|/|清除某个文件某行的断点
r|return|执行当前函数到结束
c|continue|执行到下一个断点
l|list|列出源码（前后11行代码）
l <行号>|/|列出某行周围11行代码
l <行号1> <行号2>|/|列出两个行号范围内的代码
p <变量名>|print <变量名>|输出变量的值
pp <变量名>|/|好看一点的输出
q|quit|退出debug
unt|until|退出循环或当期堆栈
run|/|重新启动debug
a|args|列出当前执行的函数的参数
w|where|打印当前执行堆栈

注：平时使用的时候通常用的都是各个命令的简写形式，当然用全称也是可以的（如果不嫌麻烦的话）。

### 补充

* 在命令行中进入调试模式的方法：`python -m pdb demo.py`
* 在调试模式中按一下`Enter`键表示执行一下上一条命令。
