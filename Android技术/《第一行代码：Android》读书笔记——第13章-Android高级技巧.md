# 全局获取Context
* 创建`ApplicationUtil`类继承自`Application`类：
```java
public class ApplicationUtil extends Application {

    private static Context context;

    @Override
    public void onCreate() {
        context = getApplicationContext();
    }

    public static Context getContext() {
        return context;
    }
}
```
* 在`AndroidManifest.xml`文件中将`application`标签的`name`属性（如果没有该属性则添加）改为：`包名.ApplicationUtil`。
* 在需要全局获取`Context`（如非`Activity`类中的`Toast`方法中）的地方使用`ApplicationUtil`类的静态方法`getContext`即可全局获取`Context`。

# 使用Intent传递对象
使用Intent传递对象主要有两种方式：`Serializable`方式和`Parcelable`方式。
