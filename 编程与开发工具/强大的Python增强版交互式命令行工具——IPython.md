本文主要介绍IPython这样一个交互工具的基本用法。
#1. 简介
IPython是《利用Python进行数据分析》一书中主要用到的Python开发环境，简单来说是对原生python交互环境的增强。作者进行Python开发最经典的开发环境搭配是：**IPython外加一个文本编辑器**。其实我自己平时写python代码也差不多是这样的开发环境：Windows系统下是IPython加notepad++，Linux系统下是IPython加vim，写起代码来体验很流畅，很容易获取到写代码时候的那种“流体验”。

书中讲到，IPython的设计目的是在交互式计算和软件开发这两个方面最大化地提高生产力，它鼓励一种“执行-探索”的工作模式，支持matplotlib等库的绘图操作。同时IPython还提供一个基于WEB的交互式浏览器开发环境（Jupyter Notebook），用起来也很不错。


#2. 基础用法
## 1. Tab键自动补全
　　和其他命令行环境的Tab自动补全功能类似，不过会隐藏那些以下划线开头的方法和属性（为了防止内容太多）。厉害的是哪怕是在python字符串中也可以自动补全类似文件路径的字符串。比如：
![](http://upload-images.jianshu.io/upload_images/8819542-e98dfafd7f52e724.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


##2. 内省
在方法或变量的前面或后面加一个问号（`?`）就可以将有关该方法或变量的一些通用信息都显示出来，这叫做内省；使用`??`还可以显示函数的源代码。见下：
![](http://upload-images.jianshu.io/upload_images/8819542-6d7810779b2fedda.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![](http://upload-images.jianshu.io/upload_images/8819542-0f29524f8fe480d8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![](http://upload-images.jianshu.io/upload_images/8819542-c743c83f7607b04a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


##3. `?`和通配符结合使用搜索命名空间
![](http://upload-images.jianshu.io/upload_images/8819542-02b9f6a4ec77bba9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


##4. `%run`命令
`%run xxx.py`：可以执行一个python脚本`xxx.py`，脚本是在一个空的命名空间中运行的。成功运行脚本后，在IPython中可以使用脚本中定义的变量和函数。
如果希望在脚本中能访问IPython之前定义的变量和函数，那么需要用-i参数执行：
`%run -i xxx.py`

##5. 执行剪贴板中的代码
`%paste`：直接执行。
`%cpaste`：可以修改后再执行。

##6. IPython键盘快捷键
* `Ctrl + P或上箭头`：后向搜索命令历史记录中以当前输入的文本开头的命令。
* `Ctrl + N或下箭头`：前向搜索命令历史记录中以当前输入的文本开头的命令。
* `Ctrl + R`：按行读取的反向历史搜索（部分匹配）。
* `Ctrl + Shift + V`：从剪贴板中粘贴文本。
* `Ctrl + C`：终止当前正在执行的代码。
* `Ctrl + A`：将光标移动到行首。
* `Ctrl + E`：将光标移动到行尾。
* `Ctrl + K`：删除从光标开始到行尾的文本。
* `Ctrl + U`：删除从行首到光标处的文本。
* `Ctrl + F`：将光标向前移动一个字符。
* `Ctrl + B`：将光标向后移动一个字符。
* `Ctrl + L`：清屏。

##7. 魔术命令
以`%`开头的一些命令，比如`%run`就是一个魔术命令，可以使用`%run?`来查看其详细用法。
* `%quickref`：显示IPython的快速参考。
* `%magic`：显示所有魔术命令的详细文档。
* `%debug`：从最新的异常跟踪的底部进入交互式调试器。
* `%hist`：打印命令的输入（可选输出）历史。
* `%pdb`：在异常发生后自动进入调试器。
* `%paste`：执行剪贴板中的python代码。
* `%cpaste`：打开一个特殊特提示符以便手工粘贴待执行的python代码。
* `%reset`：删除interactive命名空间中的全部变量/名称。
* `%page OBJECT`：通过分页器打印输出OBJECT。
* `%run xxx.py`：执行xxx.py脚本文件。
* `%prun statement`：通过cProfile执行statement，并打印分析器的输出结果。
* `%time statement`：计算statement的执行时间。
* `%timeit statement`：多次执行（次数可以通过参数配置）statement以计算平均执行时间。对那些执行时间非常短的代码很有用。
* `%who`：显示interactive命名空间中定义的变量，如下：
![](http://upload-images.jianshu.io/upload_images/8819542-a770250fa94e55f3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


* `%who_ls`：显示interactive命名空间中定义的变量（列表形式），如下：
![](http://upload-images.jianshu.io/upload_images/8819542-1e27843dc421f697.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

* `%whos`：显示interactive命名空间中定义的变量（详情形式），如下：
![](http://upload-images.jianshu.io/upload_images/8819542-231fa29bb16bcbc0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

* `%xdel variable`：删除变量variable，并尝试清除其在IPython中的对象上的一切引用。

##8. 打开`pylab`模式：
启动IPython时使用：`ipython --pylab`，这样就可以在IPython命令行中进行绘图等操作了，如下：
![](http://upload-images.jianshu.io/upload_images/8819542-29ec11f98c72d9c9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

##9. 输入和输出变量
最近的两个输出结果分别保存在下划线和双下划线两个变量中，如下：
![](http://upload-images.jianshu.io/upload_images/8819542-4d943d0e49b22ce3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


##10. 记录输入输出过的变量
某一行的输入变量：`_iX`（X为行号）
某一行的输出变量：`_X`（X为行号）
见下：
![](http://upload-images.jianshu.io/upload_images/8819542-a355e915cb25050a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


##11. 清理命名空间
当处理大数据集时，IPython的输入输出历史会影响到大量的变量的内存释放，所以及时用`%xdel`和`%reset`清理还是很有必要的。

##12. 记录日志
记录输入和输出日志：`%logstart -o`，将记录整个会话的日志（包括之前的命令），使用详情可以用`%logstart?`命令查看。

##13. 与操作系统交互
* `!cmd`：执行操作系统的shell命令。
* `output = !cmd`：执行shell命令，并将结果存到output中。
* `%alias new_name cmd`：为系统shell命令定义别名。
* `%bookmark`：使用IPython的目录书签系统。
* `%cd directory`：将工作目录切换到directory路径。
* `%pwd`：打印当前的工作目录。
* `%pushd directory`：将当前目录入栈，并转向目标目录。
* `%popd`：弹出栈顶目录，并转向该目录。
* `%dirs`：返回一个含有当前目录栈的列表。
* `%dhist`：打印目录访问历史。
* `%env`：以dict形式返回系统环境变量。

##14. 在执行shell命令时使用IPython环境中的变量
如下：
![](http://upload-images.jianshu.io/upload_images/8819542-5d937ec94940cc32.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


##15. 使用书签
如下：
![](http://upload-images.jianshu.io/upload_images/8819542-e4f0e6f04df99b70.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

#3. 进阶用法
##1. 代码执行时间分析
命令：`%time`、`%timeit`，如下：
![](http://upload-images.jianshu.io/upload_images/8819542-383225c1a1460f89.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![](http://upload-images.jianshu.io/upload_images/8819542-d804fb0ef8746f05.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![](http://upload-images.jianshu.io/upload_images/8819542-49e7c6cb6e234fc7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


##2. IPython HTML Notebook
HTML Notebook是在浏览器中使用的交互式环境，现在最新版本又叫做Jupyter Notebook，功能很强大，完全是一个B/S模式的IDE，体验非常棒。可以用以下命令打开：
* 安装notebook：`pip install notebook`
* 在命令行中打开notebook：`ipython notebook`（或者：`jupyter notebook`）
* 出现一个带token的url，把url复制到浏览器中，即出现如下页面：
![](http://upload-images.jianshu.io/upload_images/8819542-51b45651c8efc3c5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


* 点击右上角的`New`—>`python 2`，即可打开交互式环境：
![](http://upload-images.jianshu.io/upload_images/8819542-4223a1a5335916a2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


* 在输入行中输入`%pylab inline`命令并执行（Shift + Enter快捷键），即可无缝集成matplotlib的绘图功能到页面中，如图：
![](http://upload-images.jianshu.io/upload_images/8819542-5acf4179e3bc8c3c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

##3. IPython个性化配置
配置文件在如下目录：
Unix：`~/.config/ipython/`
Windows：`%HOME%/.ipython/`
根据配置文件中的注释，即可修改相应的配置。
