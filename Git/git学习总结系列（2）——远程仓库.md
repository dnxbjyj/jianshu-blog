本文主要介绍git本地仓库和GitHub远程仓库之间的交互和数据传输。

注：首先需要到github.com上注册一个账号。

# 1. 添加本地SSH Key到GitHub

要向GitHub远程仓库推送代码之前，需要做一个认证，即需要让GitHub知道向它推送代码的电脑是一个可以信赖的电脑。这就需要往GitHub上添加一个可以标示出本地电脑的SSH Key，然后才能往GitHub上推送代码。

## 1. 在本地生成一个SSH Key公钥和私钥

在任意目录下执行下面这条命令，执行完之后一路按回车即可：

`ssh-keygen -t rsa -C "yourgit@test.com"`

注：`yourgit@test.com`即为注册的GitHub账号邮箱地址。如果要在Windows下执行这个命令，必须在Git Bash窗口中执行，在Windows自带的cmd窗口中是没有这个命令的。

## 2. 切换到本地用户主目录：`cd ~`

此时在～目录用`ls -al`命令可以看到 一个.ssh隐藏目录

在.ssh目录中有两个密钥文件：id_rsa（私钥）、id_rsa.pub（公钥）,用vim或gedit打开公钥文件，复制其中的文本内容。
注意：原模原样复制，不要加任何多余的空格或空行。

## 3. 在GitHub创建SSH Key

用第1步中的GitHub账号从浏览器登录GitHub，点击右上角——>settings——>SSH and GPG Keys页面，点击创建一个SSH Key，标题可以随意写，将刚刚复制的公钥内容复制到"key"文本框中，并点击"Add SSH Key“按钮，这样就添加好了SSH Key。同一台电脑往一个GitHub账号只需添加一个SSH Key即可。

注：

* （1）允许添加多个SSH Key到同一个GitHub账号，这样就允许比如说我在家写了代码想推送到自己的GitHub账号上，同时也允许我在公司写完代码也可以推送到我的GitHub账号上去（如果公司允许的话）。

* （2）在GitHub上托管的公开代码仓库任何人都可以看到内容，但不可做修改（只有添加了SSH Key才可以做修改）。

* （3）要想不让别人看到自己的GitHub仓库的内容，有2种方法：第一种是向GitHub付费申请私有仓库，第二种是自己搭建一个git服务器。对于第一种，我的理解是GitHub本来就是一个倡导开源的组织，要想免费使用它的平台就要贡献出来一些东西（即开源自己的代码），如果不想开源那就要收费了（因为你没有贡献出来什么东西给大家）。

# 2. 提交本地代码到远程库

假如本地已经有了一个git仓库：learngit，现在想要把这个仓库的代码推送到GitHub上去，步骤如下：

## 1. 在GitHub上创建一个远程库

点击页面右上角的一个"+"按钮，创建一个空的远程仓库：learngit。

## 2. 建立本地库与远程仓库的联系

在本地learngit仓库目录下执行命令：

`git remote add origin git@github.com:xxx/learngit.git`

注：这是用SSH的方式进行推送，其中origin为默认的远程仓库名，xxx为你的邮箱账号名（@之前的字符串），learngit为刚刚第1步创建的远程仓库名。除了SSH的推送方式外，还有HTTPS的方式，但SSH的方式速度更快。最后的'.git'是一定要带上的。

补充：

查看本地仓库和远程仓库的联系信息：`git remote -v`

删除本地库与远程库的联系：`git remote remove origin`

## 3.拉远程仓库代码到本地

如果远程仓库创建了README.md等文件，那么先要把远程的文件拉到本地，否则下一步push的时候不会成功：

`git pull origin master:master`

注：此命令表明把远程的master分支拉到本地的master分支，前一个master指的是远程的master分支。

## 4. 推送代码

建立和远程仓库的联系后，就可以将本地仓库当前分支的代码推送到远程仓库了。将本地仓库的master分支的内容（默认分支为master）推送到远程库对应的分支上（master分支）：

`git push -u origin master`

注：首次推送要加`-u`参数，后面再推送就可以不加了，因为这第一次已经建立了和远程仓库的追踪链接，所以可以直接用：`git push origin master`

# 3. 从远程仓库克隆到本地

## 1. 创建远程仓库

在github上创建一个远程仓库：gitskills，并在创建时候顺便初始化一个readme.md文件
注：在创建远程仓库的时候，同时也可以创建.gitignore文件（有现成的各种语言的.gitignore文件可以选），也可以创建license文件。

## 2. 克隆远程库到本地

在本地任一目录下执行：

`git clone git@github.com:xxx/gitskills.git`

## 3. 成功克隆远程代码到本地

此时发现当前目录下多了一个gitskills目录，进去之后就可以看到第1步中创建的readme.md文件了

## 4. 其他下载方式

git远程库的其他下载方式：https，zip压缩包，但还是属ssh方式速度最快
