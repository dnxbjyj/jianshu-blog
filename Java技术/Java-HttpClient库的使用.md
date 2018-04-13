# 简介
`HttpClient`是Apache的一个开源库，相比于JDK自带的`URLConnection`等，使用起来更灵活方便。
使用方法可以大致分为如下八步曲：
* 创建一个HttpClient对象;
* 创建一个Http请求对象并设置请求的URL，比如GET请求就创建一个HttpGet对象，POST请求就创建一个HttpPost对象;
* 如果需要可以设置请求对象的请求头参数，也可以往请求对象中添加请求参数;
* 调用HttpClient对象的`execute`方法执行请求;
* 获取请求响应对象和响应Entity;
* 从响应对象中获取响应状态，从响应Entity中获取响应内容;
* 关闭响应对象;
* 关闭HttpClient.

# 在本地创建一个Servlet程序
在本地创建一个Servlet程序并跑在Tomcat服务器中，主要用于下一步测试HttpClient发送请求。
注：Servlet的创建方法详见：[Eclipse+Tomcat搭建本地服务器并跑通HelloWorld程序](http://www.jianshu.com/p/1d6b5098d99b)
* Servlet类：
```java
import java.io.PrintWriter;

import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class HelloWorld extends HttpServlet {
    private static final long serialVersionUID = 4601029764222607869L;

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) {
        // 1. 设置编码格式
        resp.setContentType("text/html");
        resp.setCharacterEncoding("UTF-8");

        // 2. 往返回体中写返回数据
        PrintWriter writer = null;
        try {
            writer = resp.getWriter();
            writer.print("Hello world! 你好，世界！！");
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            writer.close();
        }
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) {
        // 1. 获取请求的参数
        String userName = req.getParameter("username");
        String password = req.getParameter("password");

        // 2. 往返回体写返回数据
        PrintWriter writer = null;
        try {
            writer = resp.getWriter();
            writer.print("your username is:" + userName + "\nyour password is:" + password);
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            writer.close();
        }
    }

}
```
* `web.xml`（新加内容）：
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

# 测试HttpClient发送GET和POST请求
* `HttpClient`测试类：
```java
package com.test.method;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.List;

import org.apache.http.HttpEntity;
import org.apache.http.NameValuePair;
import org.apache.http.ParseException;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.util.EntityUtils;

/**
 * 测试HttpClient发送各种请求的方法
 * 
 * @author Administrator
 *
 */
public class HttpClientTest {
    // 发送请求的url
    public static final String REQUEST_URL = "http://localhost:8080/TomcatTest/hello";

    /**
     * 测试发送GET请求
     */
    public void get() {
        // 1. 创建一个默认的client实例
        CloseableHttpClient client = HttpClients.createDefault();

        try {
            // 2. 创建一个httpget对象
            HttpGet httpGet = new HttpGet(REQUEST_URL);
            System.out.println("executing GET request " + httpGet.getURI());

            // 3. 执行GET请求并获取响应对象
            CloseableHttpResponse resp = client.execute(httpGet);

            try {
                // 4. 获取响应体
                HttpEntity entity = resp.getEntity();
                System.out.println("------");

                // 5. 打印响应状态
                System.out.println(resp.getStatusLine());

                // 6. 打印响应长度和响应内容
                if (null != entity) {
                    System.out.println("Response content length = " + entity.getContentLength());
                    System.out.println("Response content is:\n" + EntityUtils.toString(entity));
                }

                System.out.println("------");
            } finally {
                // 7. 无论请求成功与否都要关闭resp
                resp.close();
            }
        } catch (ClientProtocolException e) {
            e.printStackTrace();
        } catch (ParseException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            // 8. 最终要关闭连接，释放资源
            try {
                client.close();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

    /**
     * 测试发送POST请求
     */
    public void post() {
        // 1. 获取默认的client实例
        CloseableHttpClient client = HttpClients.createDefault();
        // 2. 创建httppost实例
        HttpPost httpPost = new HttpPost(REQUEST_URL);
        // 3. 创建参数队列（键值对列表）
        List<NameValuePair> paramPairs = new ArrayList<NameValuePair>();
        paramPairs.add(new BasicNameValuePair("username", "admin"));
        paramPairs.add(new BasicNameValuePair("password", "123456"));

        UrlEncodedFormEntity entity;

        try {
            // 4. 将参数设置到entity对象中
            entity = new UrlEncodedFormEntity(paramPairs, "UTF-8");

            // 5. 将entity对象设置到httppost对象中
            httpPost.setEntity(entity);

            System.out.println("executing POST request " + httpPost.getURI());

            // 6. 发送请求并回去响应
            CloseableHttpResponse resp = client.execute(httpPost);

            try {
                // 7. 获取响应entity
                HttpEntity respEntity = resp.getEntity();

                // 8. 打印出响应内容
                if (null != respEntity) {
                    System.out.println("------");
                    System.out.println(resp.getStatusLine());
                    System.out.println("Response content is : \n" + EntityUtils.toString(respEntity, "UTF-8"));

                    System.out.println("------");
                }
            } finally {
                // 9. 关闭响应对象
                resp.close();
            }

        } catch (ClientProtocolException e) {
            e.printStackTrace();
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            // 10. 关闭连接，释放资源
            try {
                client.close();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

    public static void main(String[] args) {
        HttpClientTest test = new HttpClientTest();
        // 测试GET请求
        test.get();
        // 测试POST请求
        test.post();
    }
}
```
* 输出结果：
```
executing GET request http://localhost:8080/TomcatTest/hello
------
HTTP/1.1 200 OK
Response content length = 34
Response content is:
Hello world! 你好，世界！！
-----
executing POST request
http://localhost:8080/TomcatTest/hello
------
HTTP/1.1 200 OK
Response content is :
your username is:admin
your password is:123456
------
```
# 所需jar包下载
所需jar包打包下载地址：[https://pan.baidu.com/s/1mhJ9iT6](https://pan.baidu.com/s/1mhJ9iT6)

