SVN是一种代码版本管理工具，具有可视化的操作界面，使用简便，和git的功能类似。下面总结一下SVN的基本用法：

* 安装SVN软件，和安装一般的软件的步骤差不多，这里使用的版本是TortoiseSVN_1.9.5.27581_x64

百度网盘下载地址：https://pan.baidu.com/s/1boFNHk7

* 安装完成之后，电脑右键菜单中就会出现SVN的菜单选项：

![](http://upload-images.jianshu.io/upload_images/8819542-4239f3ae4bfb1e15.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

注：如果没有出现SVN的右键菜单，那么再重新执行一下安装包，并选择“修复模式”安装即可。

* 拉远程代码库中的代码到本地并在本地创建SVN仓库：

在任何一个文件夹点击鼠标右键，然后点击右键菜单的`SVN Checkout`，弹出一个窗口如下：

![](http://upload-images.jianshu.io/upload_images/8819542-fe8031671a9e308d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

其中`URL of repository`是远程代码仓库的地址，`Checkout directory`即为本地当前文件夹的路径。

* 点击第3步中的窗口的“OK”按钮，然后需要输入远程代码仓库的账号和密码（比如我这里是从百度应用引擎代码仓库上面拉代码，就需要输入百度账号密码），然后就可以把远程代码拉到本地并在本地创建好一个SVN仓库了。

* 在本地仓库路径下可以在空白处点击右键“SVN Update”菜单更新代码，也可以用`SVN Commit`菜单提交代码。需要注意的时，当新增文件后，需要先将文件Add进SVN仓库再Commit，如下图：

![](http://upload-images.jianshu.io/upload_images/8819542-7b905c945f677498.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![](http://upload-images.jianshu.io/upload_images/8819542-41d4b0c7c0a35f94.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

* 提交代码：在空白处点击右键->`SVN Commit`

![](http://upload-images.jianshu.io/upload_images/8819542-299122092fce2396.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

注：其中的Message内容必须填写，不能为空，否则可能会提交不成功。

* 经过以上几步之后就可以轻松地对远程代码进行代码的版本管理了。

* 此外，如果远程代码库的账号密码更换了，或者换其他远程代码库了，那么可以先清空SVN配置中保存的账号信息再SVN Checkout，如下图：

![](http://upload-images.jianshu.io/upload_images/8819542-6274dce95c61f5b5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![](http://upload-images.jianshu.io/upload_images/8819542-35c0c745909c479e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

* 还可以安装BCompare软件，这是一个代码比较工具，可以方便地比较不同版本的代码。安装完BCompare之后，可以将其安装路径添加到SVN的比较器中，如下：

![](http://upload-images.jianshu.io/upload_images/8819542-c631627800d7c730.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

* 右键菜单还可以查看SVN的日志：

![](http://upload-images.jianshu.io/upload_images/8819542-c91231663f600d4a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![](http://upload-images.jianshu.io/upload_images/8819542-daa556a313532b91.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

* 如果不想用当前本地的代码仓库了，直接删除代码仓库所在的文件夹即可。
