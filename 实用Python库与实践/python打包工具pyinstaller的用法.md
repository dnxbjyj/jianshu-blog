> 本文讲述的核心库：`pyinstaller`

pyinstaller是一个很好用的python打包工具，在Windows环境下可以将python脚本打包成一个exe可执行文件，并且脚本中所依赖的各种第三方库在打包时候都会被统一处理到一起，这样打包成的exe文件就可以在没有安装这些库的电脑上执行，甚至也可以在没有安装任何python环境的电脑上执行。

## 安装

`pip install pyinstaller`

## 基本用法

在要打包的py脚本（比如名称为demo.py）所在的目录下，执行：

`pyinstaller -F -w -i icon.ico demo.py`

其中icon.ico是当前目录下的一个图标文件，在命令行中执行这条命令后，在当前目录下的dist目录中就会生成一个名为demo.exe的可执行文件，且其图标为icon.ico文件。

几项参数的含义：

* -F：打包为单文件

* -w：Windows程序，不显示命令行窗口，但是如果程序有命令行输入或输出，不要带此项参数！

* -i：后面跟图标文件路径，一定要是ico格式的文件，如果不是可以用格式工厂等软件先转换一下

* demo.py：要打包成exe文件的脚本文件

## 实例

当前目录下有一个名为argtest.py的脚本文件（内容如下），还有一个icon.ico的图片文件。

```python
# coding:utf-8
# 测试argparse模块的基本用法
import argparse

# 创建参数解析对象，并添加脚本用法帮助
parser = argparse.ArgumentParser(description = 'test the base usage of argparse.')

# 添加位置参数
# 所谓位置参数，就是指直接添加的参数而不用使用'-'、'--'等符号
# 添加了位置参数，它就是必选参数
parser.add_argument('arg0')

# 添加可选参数，但如果执行命令时带有该参数，后面必须跟参数值
# '-'后面跟短参数，'--'后面跟长参数
# help参数为该参数的帮助信息
parser.add_argument('-a1','--arg1',help = 'this is arg1')

# 添加可选参数，但后面不能跟参数值
parser.add_argument('-a2','--arg2',help = 'this is arg2',action = 'store_true')

# 添加可选参数并指定参数值数据类型为整型，且数据范围为[0,1,2]，且指定默认值为0,如果输入的值不是整型或值不在要求的范围内，则会报错
parser.add_argument('-a3','--arg3',type = int,choices = [0,1,2],default = 0,help = 'this is arg3')

# 添加一组可选的互斥参数
# a4和a5参数不能同时出现，否则会报错
group = parser.add_mutually_exclusive_group()
group.add_argument('-a4','--arg4',action = 'store_true')
group.add_argument('-a5','--arg5',action = 'store_true')

#####################################

# 执行解析参数
args = parser.parse_args()

# 打印出位置参数'arg0'
print 'arg0 is: ',args.arg0

# 打印出其他位置参数，注意这里要用参数的'--'名称（长参数）
if args.arg1:
    print 'arg1 is: ',args.arg1

# 因为arg2后面没有跟参数值，所以打印出来是True
if args.arg2:
    print 'arg2 is: ',args.arg2
    
if args.arg3:
    print 'arg3 is: ',args.arg3
    
if args.arg4:
    print 'arg4 is: ',args.arg4
    
if args.arg5:
    print 'arg5 is: ',args.arg5
    
```

在命令行当前目录下执行命令：`pyinstaller -F -i icon.ico argtest.py`

执行完之后，发现在当前目录下生成了两个新目录：build、dist以及一个文件：argtest.spec，build目录和argtest.spec都是pyinstaller在打包过程中产生的中间文件，而dist目录中则可以看到生成了一个名为argtest.exe的可执行文件，并且图标为icon.ico的图片。

在当前命令行中先cd到dist目录下，然后执行：`argtest.exe -h`，可以看到：

![](http://upload-images.jianshu.io/upload_images/8819542-0e33abf971f0ccb9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



再执行：`argtest.exe 000 -a1 111 -a3 2`，可以看到：

![](http://upload-images.jianshu.io/upload_images/8819542-b3f31373c33a89fb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
