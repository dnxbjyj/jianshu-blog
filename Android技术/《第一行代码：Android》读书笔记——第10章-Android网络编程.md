# WebView的用法
* WebView也是一个普通的控件。
* 常用用法：
```java
WebView webView = (WebView)findViewById(R.id.web_view);
webView.getSettings( ).setJavaScriptEnabled(true);    //让webView支持javascript脚本
webView.setWebViewClient(new WebViewClient( ){
    @Override
    public boolean shouldOverrideUrlLoading(WebView view, String url){
           view.loadUrl(url);    //根据传入的参数再去加载新的网页
           return true;    //表示当前WebView可以处理打开新网页的请求，不用借助系统浏览器
    }
});
webView.loadUrl("http://www.baidu.com");
```
* 使用任何网络功能的程序都要申请权限：
```xml
<uses-permission android:name="android.permission.INTERNET" />
```
# 使用HttpURLConnection访问网络
### 步骤如下
* 创建一个URL对象，然后使用其`openConnection`创建一个`HttpURLConnection`对象：
```java
URL url = new URL("http://www.baidu.com");
connection = (HttpURLConnection) url.openConnection();
```
* 设置`HttpURLConnection`是GET方法还是POST方法：
```java
connection.setRequestMethod("GET");
```
* 对`HttpURLConnection`进行其他的设置：
```java
connection.setConnectTimeout(8000);    //设置连接超时的毫秒数
connection.setReadTimeout(8000);    //设置读取超时的毫秒数
```
* 用`HttpURLConnection`对象的`getInputStream`方法获取服务器的返回输入流`InputStream`对象：
```java
InputStream in = connection.getInputStream();
```
* 对输入流进行读取：
```java
BufferedReader reader = new BufferedReader(
new InputStreamReader(in));
StringBuilder response = new StringBuilder();
String line;
while ((line = reader.readLine()) != null) {
    response.append(line);
}
```
* 用`disconnect`方法关闭这个HTTP连接：
```java
connection.disconnect();
```
### 注意事项
* 网络请求要放在子线程里。
* 在子线程里网络请求获取返回数据后，如果要进行UI操作，则要采用异步消息处理方法。
* 要申请网络权限。

# 使用HttpClient访问网络
HttpClient是一个接口类，是Apache提供的HTTP网络访问接口，从一开始就被引入到了Android API中。
### 使用步骤
* 创建HttpClient实例：
```java
HttpClient httpClient = new DefaultHttpClient();
```
* 根据发起请求的类型不同，步骤也不同：
```java
// GET请求：
HttpGet httpGet = new HttpGet("http://10.0.2.2:8081/get_data.xml");

// POST请求：
HttpPost httpPost = new HttpPost("http://www.baidu.com");
List<NameValuePair> params = new ArrayList<NameValuePair>();
params.add(new BasicNameValuePair("username","admin"));
params.add(new BasicNameValuePair("password","123456"));
UrlEncodedFormEntity entity = new UrlEncodedFormEntity(params, "utf-8");
httpPost.setEntity(entity);
```
* 获取服务器返回值：
```java
HttpResponse httpResponse = httpClient.execute(httpGet);
```
* 判断返回状态码，如果等于200就表示请求和响应都成功了：
```java
if (httpResponse.getStatusLine().getStatusCode() == 200) {
    HttpEntity entity = httpResponse.getEntity();
    String response = EntityUtils.toString(entity, "utf-8");
    ...    //其他操作
}
```
* 注意：HttpClient访问网络同样要放在子线程里，还要申请网络权限。

# 使用回调机制封装HttpURLConnection操作来创建HttpUtil类
* 创建`HttpCallbackListener`接口：
```java
public interface HttpCallbackListener {
    void onFinish(String response);    //在服务器成功响应请求时调用
    void onError(Exception e);    //进行网络操作出错时调用
}
```
* 创建HttpUtil类：
```java
import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class HttpUtil {
    public static void sendHttpRequest(final String address,final HttpCallbackListener listener) {
        new Thread(new Runnable() {
            @Override
            public void run() {
                HttpURLConnection connection = null;

                try {
                    URL url = new URL(address);
                    connection = (HttpURLConnection) url.openConnection();

                    connection.setRequestMethod("GET");
                    connection.setConnectTimeout(8000);
                    connection.setReadTimeout(8000);
                    connection.setDoInput(true);
                    connection.setDoOutput(true);

                    InputStream in = connection.getInputStream();
                    BufferedReader reader = new BufferedReader(
                            new InputStreamReader(in));
                    StringBuilder response = new StringBuilder();
                    String line;

                    while ((line = reader.readLine()) != null) {
                        response.append(line);
                    }

                    if (listener != null) {
                        // 回调onFinish方法
                        listener.onFinish(response.toString());
                    }

                } catch (Exception e) {
                    if (listener != null) {
                        listener.onError(e);
                    }
                } finally {
                    if (connection != null) {
                        connection.disconnect();
                    }
                }
            }
        }).start();
    }
}
```
* 使用时这样使用：
```java
HttpUtil.sendHttpRequest("http://www.baidu.com",new HttpCallBackListener(){
    @Override
    public void onFinish(String response){
        //在这里根据返回内容执行具体的逻辑
    }

    @Override
    public void onError(Exception e){
        //在这里对异常情况进行处理
    }
});
```
# 解析XML数据
* 安装Apache服务器：下载安装包，然后安装成功后启动服务器，在浏览器里输入`127.0.0.1`，会看到Apache的字样。
* 在Apache安装目录：`...\Apache\htdocs`目录下，可以新建一个xml文件，命名为`get_data.xml`，加入内容，然后在浏览器里输入：`127.0.0.1/get_data.xml`（在手机模拟器里要输入：`10.0.2.2/get_data.xml`），就会显示出该文件的内容。
* 编写的XML数据的格式如下：
```xml
<apps>
    <app>
        <id>1</id>
        <name>Google Maps</name>
        <version>1.0</version>
    </app>
    <app>
        <id>2</id>
        <name>Chrome</name>
        <version>1.8</version>
    </app>
    <app>
        <id>3</id>
        <name>Google Play</name>
        <version>3.2</version>
    </app>
</apps>
```
* 用Pull方式解析XML数据：
```java
private void parseXMLWithPull(String xmlData) {
        try {
            XmlPullParserFactory factory = XmlPullParserFactory.newInstance();
            XmlPullParser xmlPullParse = factory.newPullParser();
            xmlPullParse.setInput(new StringReader(xmlData));
            int eventType = xmlPullParse.getEventType();

            String id = "";
            String name = "";
            String version = "";

            while (eventType != XmlPullParser.END_DOCUMENT) {
                String nodeName = xmlPullParse.getName();
                switch (eventType) {
                // 开始解析某个结点
                case XmlPullParser.START_TAG: {
                    if ("id".equals(nodeName)) {
                        id = xmlPullParse.nextText();
                    } else if ("name".equals(nodeName)) {
                        name = xmlPullParse.nextText();
                    } else if ("version".equals(nodeName)) {
                        version = xmlPullParse.nextText();
                    }
                }
                    break;
                // 完成解析某个结点
                case XmlPullParser.END_TAG: {
                    if ("app".equals(nodeName)) {
                        Log.d("MainActivity", "id is " + id);
                        Log.d("MainActivity", "name is " + name);
                        Log.d("MainActivity", "version is " + version);
                    }
                }
                    break;
                default:
                    break;
                }

                eventType = xmlPullParse.next();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
```
* 用SAX方式解析XML数据步骤：
创建`ContentHandler `类继承自`DefaultHandler`并重写5个方法：
```java
import org.xml.sax.Attributes;
import org.xml.sax.SAXException;
import org.xml.sax.helpers.DefaultHandler;

import android.util.Log;

public class ContentHandler extends DefaultHandler {
    private String nodeName;
    private StringBuilder id;
    private StringBuilder name;
    private StringBuilder version;

    @Override
    public void startDocument() throws SAXException {
        id = new StringBuilder();
        name = new StringBuilder();
        version = new StringBuilder();
    }

    @Override
    public void startElement(String uri, String localName, String qName,
            Attributes attributes) throws SAXException {
        // 记录当前结点名
        nodeName = localName;
    }

    @Override
    public void characters(char[] ch, int start, int length)
            throws SAXException {
        // 根据当前结点名判断将内容添加到哪一个StringBuilder对象中
        if ("id".equals(nodeName)) {
            id.append(ch, start, length);
        } else if ("name".equals(nodeName)) {
            name.append(ch, start, length);
        } else if ("version".equals(nodeName)) {
            version.append(ch, start, length);
        }
    }

    @Override
    public void endElement(String uri, String localName, String qName)
            throws SAXException {
        // 用trim方法去掉空白字符
        if ("app".equals(localName)) {
            Log.d("MainActivity", "id is " + id.toString().trim());
            Log.d("MainActivity", "name is " + name.toString().trim());
            Log.d("MainActivity", "version is " + version.toString().trim());

            // 将StringBuilder清空
            id.setLength(0);
            name.setLength(0);
            version.setLength(0);
        }
    }

    @Override
    public void endDocument() throws SAXException {
    }
}
```
写具体方法：
```java
private void parseXMLWithSAX(String xmlData) {
        try {
            SAXParserFactory factory = SAXParserFactory.newInstance();
            XMLReader xmlReader = factory.newSAXParser().getXMLReader();
            ContentHandler handler = new ContentHandler();

            xmlReader.setContentHandler(handler);

            // 开始执行解析
            xmlReader.parse(new InputSource(new StringReader(xmlData)));
        } catch (Exception e) {
            e.printStackTrace();
        }
}
```
# 解析Json数据
详见：[Java-json系列（一）：用GSON解析Json格式数据](http://www.jianshu.com/p/1b7c83d70821)
，这里不再详写。
