微信公众号开发的时候，微信服务器是需要访问我们的一个公网服务器地址的，但我们又是在本地调试自己的程序的，那怎样让微信服务器能访问到我们本地的服务器呢？那就需要用外网映射工具，将本地IP映射成公网IP，这样就能在公网上访问本地服务了，这里使用ngrok。ngrok原版程序的服务器是在国外的，访问速度极慢或者干脆访问不了，所以这里提供一个服务器搭建在国内的基于ngrok的一个软件：qydev，百度网盘下载链接见文章结尾。

# 用法

* 在文末下载链接中下载windows版本的客户端，将`ngrok.exe`和`ngrok.cfg`两个文件解压到你喜欢的目录;

* 在cmd命令行下进入到上面两个文件所在的目录下;

* 执行命令：`ngrok -config=ngrok.cfg -subdomain xxx 8080` (xxx是你自定义的域名前缀);

* 如果开启成功，就可以使用`http://xxx.tunnel.qydev.com`来访问你本机的`127.0.0.1:8080` 的服务了（比如本地Tomcat）;

* 如果你自己有顶级域名，想通过自己的域名来访问本机的项目，那么先将自己的顶级域名解析到`123.57.165.240`(域名需要已备案)，然后执行命令：`ngrok -config=ngrok.cfg -hostname xxx.xxx.xxx 8080` (xxx.xxx.xxx是你自定义的顶级域名)，如果开启成功，你就可以使用你的顶级域名来访问你本机的`127.0.0.1:8080`的服务啦。

# 示例

* 本地启动Tomcat程序，url为：`http://localhost:8080/TomcatTest/hello`

在浏览器中访问效果如图：

![](http://upload-images.jianshu.io/upload_images/8819542-644375d3b6c51596.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

注：如何创建及启动Tomcat程序，参见另一篇博客：[微信公众号开发技术基础（一）：Eclipse+Tomcat搭建本地服务器并跑通HelloWorld程序]()

* cmd窗口中切换到到`ngrok.exe`和`ngrok.cfg`所在目录，启动ngrok：

`ngrok -config=ngrok.cfg -subdomain jyj 8080`

如图：

![](http://upload-images.jianshu.io/upload_images/8819542-71520967a9a1e6f3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

* 浏览器访问：`http://jyj.tunnel.qydev.com/TomcatTest/hello`（这就是本地8080端口的外网访问地址）即可看到和访问`localhost:8080/TomcatTest/hello`一样的效果：

![](http://upload-images.jianshu.io/upload_images/8819542-d1b0919014ce8adb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

# qydev ngrok的下载链接及相关网站

* qydev ngrok百度网盘下载链接：https://pan.baidu.com/s/1eS20qxs

* 帮助网站：http://qydev.com/

* 其他类似ngrok工具：http://ngrok.2bdata.com/ 
用法都类似。
