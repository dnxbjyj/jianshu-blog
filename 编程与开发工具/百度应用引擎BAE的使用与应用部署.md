百度应用引擎（BAE）是百度推出的网络应用开发平台，开发者使用BAE不需要进行服务器的配置、维护等繁琐的工作，也不需要进行域名的申请、备案等工作，而只需要上传自己的WEB应用即可在公网上访问。使用及部署应用的步骤如下：

* 注册百度账号，并在百度云官网注册、审核成为开发者，还需要进行身份证实名认证才能申请BAE，实名认证审核大概需要2、3个工作日（以上步骤略，见官网介绍）。

百度云首页：https://cloud.baidu.com/

* 注册、审核通过之后，登录https://cloud.baidu.com/，点击页面上的“管理控制台”按钮进入控制台，然后点击右侧“应用引擎BAE”菜单，如下：

![](http://upload-images.jianshu.io/upload_images/8819542-98475bd132f38b6c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

* 点击下图中的“添加部署”，进入申请页面：

![](http://upload-images.jianshu.io/upload_images/8819542-d717df53ccffcb59.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

* 添加部署页面主要填一些基础配置，重点是这几项，其他使用默认值即可：

![](http://upload-images.jianshu.io/upload_images/8819542-e0985f37f246b691.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

其中域名和应用名称是自己填，类型我们选择java8-tomcat，代码版本工具选择SVN。

* 最后是支付，BAE基础版每天的费用是0.4元，还是很划算的，可以在百度云账户中多充值几块钱，防止应用因欠费被停掉。

* 支付完成后，过几分钟，应用就创建成功了，如图：

![](http://upload-images.jianshu.io/upload_images/8819542-9780c6a555ed8840.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

其中域名就是刚刚我们设置的域名，点击代码管理方式下的“点击复制”按钮，就可以复制远程代码库的地址，然后就可以把代码库使用SVN软件拉到本地代码仓库中了。

具体SVN的用法详见：[SVN代码版本管理工具的使用](http://www.jianshu.com/p/c31126975e8b)

* 在本地Eclipse里创建一个Tomcat程序，具体的创建方法详见：[Eclipse+Tomcat搭建本地服务器并跑通HelloWorld程序](http://www.jianshu.com/p/1d6b5098d99b)


然后在工程上点击右键->Export->WAR File，把导出路径设置为第6步中创建的本地SVN仓库的路径。

* Commit代码，然后到百度云控制台部署列表中点击应用的“快捷发布”按钮即可发布应用。

* 在浏览器中输入应用的域名即可访问应用。
