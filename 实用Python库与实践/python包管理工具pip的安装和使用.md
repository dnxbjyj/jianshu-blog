> 本文讲述的核心库：`pip`

pip是python的一个非常好用的包管理工具，可以用来很方便地安装和管理各种三方库，本文对其基本用法进行介绍。

# 安装pip

## Windows系统上安装

* 1. python 2.7.9及以上版本的windows版的安装包已经集成了pip，所以到python.org网站下载python-2.7.9.amd64.msi安装包并安装。
* 2. 安装时选择"安装pip"。
* 3. 安装好后添加python.exe和pip.exe文件所在路径到系统环境变量中。这两个路径分别为（假设我的python安装在了D:\Programs\Python27目录下）：
```bash
D:\Programs\Python27
D:\Programs\Python27\Scripts
```
* 4. 测试：打开cmd，输入：`pip install web.py`
* 5. 进入python命令行，输入：`import web`，若导入成功则说明pip安装成功。

## Linux系统上安装

* 1. 到pypi.python.org上搜索pip，下载最新版本的源码压缩包。
* 2. 在本地解压源码压缩包，进入源码路径，执行：`python setup.py install`即可安装。
* 3. 测试：打开cmd，输入：`pip install web.py`
* 4. 进入python命令行，输入：`import web`，若导入成功则说明pip安装成功。
* 5. 注：ubuntu系统可以直接使用该命令安装：`sudo apt-get install python-pip`

# pip常用命令

* 安装软件包：`pip install 包名`

注：这里的包名，也可以是已经下载好的whl文件或tar.gz压缩包文件路径，或者包所在的URL地址。

* 升级pip自身：`pip install --upgrade pip`

* 查看已经通过pip安装的包：`pip list`

* 显示当前已经通过pip安装的包及版本号：`pip freeze`，显示结果示例：
```bash
certifi==2017.7.27.1
chardet==3.0.4
idna==2.5
requests==2.18.2
urllib3==1.22
virtualenv==15.1.0
web.py==0.38
```

* 将`pip freeze`命令的结果重定向到requirements.txt文件中：`pip freeze > requirements.txt`

* 使用已有的requirements.txt文件在另一个环境上安装各种包（比如在一台新电脑上）：`pip install -r requirements.txt`
注：这个命令的好处就是，如果换了一个新的环境需要安装一个相同的python环境，那么只需要有requirements.txt文件即可快速安装，就不需要再思考要安装哪些包了。

* 查看某个已经安装的包的详情：`pip show 包名`

* 查看过期的包：`pip list --outdated`

* 安装包到用户目录：`pip install 包名 --user`

* 安装本地的安装包：`pip install 目录|文件名`

* 卸载包：`pip uninstall 包名`

* 升级包：`pip install 包名 --upgrade`

* 显示包所在目录：`pip show -f 包名`

* 搜索包：`pip search 关键字`

* 查询可升级的包：`pip list -o`

* 下载包但不安装：`pip install 包名 -d 目录`

* 打包：`pip wheel 包名`

# pip镜像源的设置与使用

## 国内pip镜像

* 豆瓣：http://pypi.douban.com/simple
* 中科大：http://pypi.mirros.ustc.edu.cn/simple

注：使用国内的镜像源，安装各种包速度会快一些。

## 指定单次安装源

`pip install 包名 -i 镜像url`

## 指定全局安装源

pip配置文件：

* Unix、Mac OS的pip配置文件位于：`$HOME/.pip/pip.conf`

* Windows的pip配置文件位于：`%HOME%\pip\pip.ini`
注：Windows下%HOME%路径一般为：`C:\Users\<UserName>\`

往pip配置文件写入如下内容（如果没有配置文件则在相应路径新建一个），这里以豆瓣的镜像为例：
```bash
[global]
trusted-host=pypi.douban.com
timeout=6000
index-url=http://pypi.douban.com/simple
```
**一个经验**：如果在指定国内的镜像源后，安装某些库速度还是比较慢，那么可以直接在浏览器打开镜像源网站地址（比如：http://pypi.douban.com/simple），在浏览器中直接搜索并下载所需的库，然后使用命令`pip install <文件名>`进行安装。如果搜索不到需要的库，还可以去这里碰碰运气：http://www.lfd.uci.edu/~gohlke/pythonlibs/，这是加利福尼亚大学尔湾分校一个生物医学研究中心的网站，上面有非常非常丰富的已经打包好的各种Python库的whl文件，堪称"Python轮子博物馆"。
