> 廖雪峰的官方网站：http://www.liaoxuefeng.com/

本文是学习廖雪峰的官方网站上git教程git基本用法的总结，详细内容可以进入廖雪峰的官方网站查看。

注：本文中的主要内容都是基于Linux环境进行操作的，使用的git版本为最新的2.10.2版本。文中命令示例中方括号里面的内容都表示是可选参数。

# 1. git与版本控制系统

* git：分布式版本控制系统。

* svn：集中式版本控制系统。

无论是分布式还是集中式版本控制系统，都只能对纯文本文件进行版本控制，而对二进制文件（如MS Word、MS Excel文档等）却都是无能为力的。

注意一点：文本文件必须统一使用utf-8格式编码，千万不要使用gbk编码！

# 2. 安装git

## 1. Linux环境（以Ubuntu为例）

### (1) 查看当前有没有安装git

`git`

### (2) 安装git

`sudo apt-get install git`

### (3) 查看git版本

`git --version`

### (4) 查看git帮助文档

有两种方法：

`git`

`git --help`

## 2. Windows环境

到 https://git-for-windows.github.io 上下载EXE安装包安装，安装完成后会有一个git bash命令行，然后在git bash命令行中其他操作和Linux下一致。

# 3. 配置git

## 1. 全局配置：

`git config --global user.name "your_name"`

`git config --global user.email "your_email@example.com"`

## 2. 在当前目录下初始化一个git版本库

`git init`

创建成功后，在当前目录下使用`ls -al`命令，可以看到创建了一个新的隐藏目录：.git，这就是git的版本库，注意不要手动修改其中的任何内容！

# 4. git工作区和暂存区、分支的关系

初始化成功一个git版本库后，会自动创建一个默认版本分支：master，以及一个暂存区（stage）。那么工作区（即用`git init`命令初始化后的硬盘文件夹）、暂存区、分支三者之间的关系是什么呢？搞清楚这一点对后面学习git的很多用法都非常重要，一图胜千言，见下图：
![](http://upload-images.jianshu.io/upload_images/8819542-5cc9c47d57d8e5c1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

# 5. git 常用操作

准备：假如当前目录位于learngit文件夹，是一个空文件夹，首先在learngit目录初始化一个git版本库：

`git init`

这时发现在learngit文件夹下新建了一个隐藏目录：.git，然后在learngit目录下新建一个文本文件：readme.txt，并向其中任意添加一些内容。

## 1. 将readme.txt文件添加到版本库暂存区

`git add readme.txt`

附：`git add`的其他用法：

* 添加工作区的所有修改（包括新建、修改和删除文件这三种修改）：`git add -A`

* 添加工作区中新建和修改文件的改动到暂存区，但不包括删除文件的改动：`git add * `或 `git add . `

* 添加工作区修改和删除文件的改动到暂存区，但不包括新建文件的改动：`git add -u`

* 撤销单个或多个文件的add操作：`git reset 文件名1 文件名2...`

* 撤销当前所有add到暂存区的操作：`git reset`

## 2. 删除文件

`git rm 文件名1 文件名2...`

## 3. 从暂存区提交修改（包括`git add`和`git rm`操作）到主分支

`git commit -m "create a new file readme.txt"`

注：`git commit`操作只会提交已经add到暂存区的修改，而工作区还未被add进暂存区的修改是不会被提交的。

## 4. 查看工作区状态

`git status`

## 5. 查看工作区和当前版本库最新版本之间的差别

`git diff HEAD [-- 文件名1 文件名2...]`

## 6. 撤销暂存区的修改（包括git add和git rm操作）

`git reset HEAD [文件名1 文件名2...]`

## 7. 查看commit操作的历史记录

`git log [--pretty=oneline]`

注：`--pretty=oneline`参数是为了在一行显示一条历史记录。

## 8. HEAD的理解

HEAD其实相当于一个指针，它指向的版本号就是当前版本库的最新版本。

* HEAD：当前版本

* HEAD^ ：上一个版本

* HEAD^^ ：上上个版本

* ......

* HEAD~100：往前100个版本

HEAD的指针作用可以用如下示意图表示：
![](http://upload-images.jianshu.io/upload_images/8819542-63c13526d01402d9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


从上图也可以看出，HEAD指针可以指向不同的版本，而这也正是下面要讲的版本回退和切换的原理。

## 9. 回退到某一个版本

* 回退到上一个版本：`git reset --hard HEAD^`

* 回退到某个版本：`git reset --hard 版本号`

注：版本号可通过`git log`命令查看，只需要写前几位即可，git会自动识别匹配。

## 10. 回到未来

假如回退到之前的某个版本后，又后悔了不想回退了，想要撤销回退（即想要回到回退前的版本），可以使用如下命令：

* 先查看commit和reset命令的所有操作历史记录：`git reflog`

* 找到想要回到的未来的某个版本号，回到未来：`git reset --hard 版本号`
