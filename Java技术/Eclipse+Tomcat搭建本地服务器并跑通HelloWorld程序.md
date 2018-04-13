# （一）环境准备

* Eclipse：要使用`for JavaEE`版本的Eclipse，因为要创建`Dynamic Web`（动态Web）程序，这里使用`eclipse-jee-mars-1-win32-x86_64`版本。Eclipse是绿色软件，下载后解压缩即可打开使用。

百度网盘下载链接：https://pan.baidu.com/s/1dFvaKrJ

* Tomcat：用于搭建本地服务器跑Servlet程序，这里使用`apache-tomcat-7.0.75-windows-x64`版本。Tomcat也是绿色软件，使用时只需把压缩包解压到自己喜欢的目录里即可。

百度网盘下载链接：https://pan.baidu.com/s/1bpiT6HL

# （二）在Eclipse里创建Dynamic Web工程

* 如图，新建一个`Dynamic Web`工程： 

![](http://upload-images.jianshu.io/upload_images/8819542-f47b607e0d03a2ff.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

* 只用填写图中红框中的几项即可，配置好了点`Next`按钮：

![](http://upload-images.jianshu.io/upload_images/8819542-6e94369986cd9270.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

其中第2步`Target Runtime`需要创建一个v7.0版本的Tomcat，如下：

![](http://upload-images.jianshu.io/upload_images/8819542-68fcdc43e3f68373.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![](http://upload-images.jianshu.io/upload_images/8819542-8cbb86f94fe35733.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

* 点"Next"按钮：

![](http://upload-images.jianshu.io/upload_images/8819542-89e75422a77f1b78.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

* 勾选上`Generate web.xml...`，然后点Finish按钮：

![](http://upload-images.jianshu.io/upload_images/8819542-a9cd9076a981a3ac.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

* 创建好的工程结构如下图，其中Servers是Tomcat的工程，不用管；TomcatTest是我们自己的工程，Java代码写在`Java Resources`目录中；`WEB-INF`目录下的lib目录主要存放第三方jar包，`web.xml`文件是Servlet的配置文件：

![](http://upload-images.jianshu.io/upload_images/8819542-28600dae8460af45.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

# （三）写一个简单的Servlet类并配置web.xml

下面我们就开始写一个最简单的Servlet类来实现输出Hello world的功能：

* 在`Java Resources`的src目录下创建一个`com.servlet`包，在其中创建一个HelloWorld类，继承自HttpServlet类，重写父类的doGet方法，代码如下：

![](http://upload-images.jianshu.io/upload_images/8819542-f65d18b623249689.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
```java
package com.servlet;

import java.io.IOException;
import java.io.PrintWriter;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class HelloWorld extends HttpServlet {
    private static final long serialVersionUID = 4601029764222607869L;

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        resp.setContentType("text/html");
        resp.setCharacterEncoding("UTF-8");
        PrintWriter out = resp.getWriter();
        out.print("Hello world! 你好，世界！");
        out.flush();
        out.close();
    }

}
```

* 配置`WEB-INF`目录下的`web.xml`文件，在其`web-app`标签之间增加如下内容，其中`url-pattern`就是一会运行后访问的url的尾部：
```xml
<servlet>
        <servlet-name>helloWorld</servlet-name>
        <servlet-class>com.servlet.HelloWorld</servlet-class>
    </servlet>

    <servlet-mapping>
        <servlet-name>helloWorld</servlet-name>
        <url-pattern>/hello</url-pattern>
    </servlet-mapping>
```

# （四）运行程序

* 右键点击TomcatTest工程，选择`Run as`->`Run on server`：

![](http://upload-images.jianshu.io/upload_images/8819542-e163dcc4140e661c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

* 选择创建工程时创建的Tomcat v7.0服务器，点击Finish按钮：

![](http://upload-images.jianshu.io/upload_images/8819542-703c7ee915778e6c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

* 此时在控制台的Servers标签中就可以看到TomcatTest工程就已经被添加到了Tomcat服务器中，并且Tomcat已经开始运行了：

![](http://upload-images.jianshu.io/upload_images/8819542-4808d93b0317a992.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

* 到浏览器中访问url：`http://localhost:8080/TomcatTest/hello`（Tomcat服务器默认是8080端口），就可以看到如下内容了，我们的HelloWorld程序也成功完成！

![](http://upload-images.jianshu.io/upload_images/8819542-0969faff09e3613f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

* 当修改Servlet类的内容后，要右键重启Tomcat服务器来进行更新，有时还需要清一下浏览器缓存才能看到更新后的内容（清理浏览器缓存快捷键：`Ctrl + Shift + Delete`）。
