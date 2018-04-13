> 本文讲述的核心库：`virtualenv`

# 介绍

virtualenv是一种虚拟化环境，可以理解为创建了一个虚拟化的pyhon运行空间，可以从新安装各种库，而与本机环境以及其他虚拟化环境互不影响，互相隔离。

# 简单的安装及使用

1. 首先要安装包管理工具pip（pip的使用详见：[python包管理工具pip的安装和使用](http://www.jianshu.com/p/eb46d00fc7ba)）
2. `pip install virtualenv`
3. 在当前目录下初始化一个虚拟化文件夹env（是隐藏文件夹）：`virtualenv .env`
4. 激活：
```bash
Linux/Mac环境：source .env/bin/activate
Windows：.env\Scripts\activate
```
5. 这样就可以在虚拟化环境中愉快地玩耍了。
6. 离开虚拟化环境：`deactivate`

# 详细参数配置
用`pip`安装`virtualenv`后，在命令行中输入：`virtualenv -h`就可以看到详细帮助如下，可以看到virtualenv的详细用法：
```
E:\>virtualenv -h
Usage: virtualenv [OPTIONS] DEST_DIR

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -v, --verbose         Increase verbosity.
  -q, --quiet           Decrease verbosity.
  -p PYTHON_EXE, --python=PYTHON_EXE
                        The Python interpreter to use, e.g.,
                        --python=python2.5 will use the python2.5 interpreter
                        to create the new environment.  The default is the
                        interpreter that virtualenv was installed with
                        (d:\programs\python27\python.exe)
  --clear               Clear out the non-root install and start from scratch.
  --no-site-packages    DEPRECATED. Retained only for backward compatibility.
                        Not having access to global site-packages is now the
                        default behavior.
  --system-site-packages
                        Give the virtual environment access to the global
                        site-packages.
  --always-copy         Always copy files rather than symlinking.
  --unzip-setuptools    Unzip Setuptools when installing it.
  --relocatable         Make an EXISTING virtualenv environment relocatable.
                        This fixes up scripts and makes all .pth files
                        relative.
  --no-setuptools       Do not install setuptools in the new virtualenv.
  --no-pip              Do not install pip in the new virtualenv.
  --no-wheel            Do not install wheel in the new virtualenv.
  --extra-search-dir=DIR
                        Directory to look for setuptools/pip distributions in.
                        This option can be used multiple times.
  --download            Download preinstalled packages from PyPI.
  --no-download, --never-download
                        Do not download preinstalled packages from PyPI.
  --prompt=PROMPT       Provides an alternative prompt prefix for this
                        environment.
  --setuptools          DEPRECATED. Retained only for backward compatibility.
                        This option has no effect.
  --distribute          DEPRECATED. Retained only for backward compatibility.
                        This option has no effect.
```
其中可以看到有一个`-p`参数，后面跟的是想要创建的虚拟化环境所使用的Python可执行文件的绝对路径。如果不指定该参数，默认值是用安装`virtualenv`包时候所使用的Python解释器的可执行文件的路径。

# 在电脑上配置Python2.x和Python3.x共存的环境
有的时候需要同时在电脑上配置Python2和Python3的环境，比如我电脑上本来使用的环境是Python2的，但是我要使用一个库，只支持Python3，而我的Python2环境还要用呢，不能简单暴力地卸载Python2换成Python3。那么怎么解决这种场景的需求呢？

`virtualenv`就可以完美地解决这个问题，还记得上一小节讲的在用`virtualenv`创建虚拟化环境时候的`-p`参数吗？是的，你没猜错，这个参数就可以指定所创建的虚拟环境使用的Python版本，从而可以实现在同一台电脑上创建Python2.x和Python3.x共存的虚拟化环境。下面来详细讲解一下配置的步骤（Windows操作系统下）:
* 首先假设当前电脑上安装的是Python2的环境，并且已经使用`pip`工具安装好了`virtualenv`包。
* 下载Python3的安装包，比如`python-3.6.0.exe`，官网下载速度非常慢，可以到CSDN下载去找一找，也可以下载本人上传到百度云的这个（是32位版本，64位操作系统也可以使用）：https://pan.baidu.com/s/1raohS4k
* 安装Python3，在安装的时候勾选`安装pip`选项。
* 安装完成之后，打开Python3的安装目录，比如我的安装目录是：`D:\Programs\Python36`，将`python.exe`文件重命名为：`python3.exe`
* 将以下两个路径添加到系统环境变量：`D:\Programs\Python36`和`D:\Programs\Python36\Scripts`
* 打开命令行，输入命令：`python3`，查看安装是否成功：
![](http://upload-images.jianshu.io/upload_images/8819542-d448c0b7409030c8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
* 创建Python3虚拟化环境：打开命令行，cd到某个目录下（比如：`E:\code\env`），执行命令：`virtualenv -p D:\Programs\Python36\python3.exe .py3env`，其中`virtualenv`命令的`-p`参数后面跟的是Python3的可执行文件的路径，`.py3env`为要创建的虚拟化环境的目录名，如下：
![](http://upload-images.jianshu.io/upload_images/8819542-6a3c5567b1272686.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

* 激活虚拟化环境：`.py3env\Scripts\activate`
![](http://upload-images.jianshu.io/upload_images/8819542-e54a8d3ea2be8037.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

* 测试虚拟化环境安装是否成功：使用`pip3`命令安装一个Python3环境才能安装成功的库，这里以安装视频下载神器——`you-get`库为例，如果安装成功，表明Python3虚拟化环境配置成功（注：用Python2安装`you-get`库会报错）：
![](http://upload-images.jianshu.io/upload_images/8819542-4318a02adf43935c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
