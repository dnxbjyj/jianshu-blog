EditText在获取焦点后默认的边框都是黄色的，这可能和我在开发的应用的主题颜色不匹配，那怎么办呢？——用自定义的控件风格，比如说我想让EditText在获取焦点时候边框变成蓝色的，而失去焦点后边框变成灰色的，要实现这个目的方法如下：

* 先在PS中画两张png图片，一张为蓝色边框、白色填充的圆角矩形，另一张为灰色边框、白色填充的圆角矩形，两个矩形形状完全相同。这两种图片分别作为EditText在激活和未激活两个状态的背景图片。一张命名为`et_pressed.png`，另一张为`et_normal.png`，如下：
![](http://upload-images.jianshu.io/upload_images/8819542-34cf4b88bd3e941d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![](http://upload-images.jianshu.io/upload_images/8819542-bbb82f32ddf0c3b3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

* 使用draw9patch.bat工具（该工具的使用方法见这篇文章：[Android制作和使用Nine-Patch图片](https://www.jianshu.com/p/fd52c2f3be9b)）将上面两个图片制作成Nine-Patch图片，并分别命名为：`et_pressed.9.png`和`et_normal.9.png`，如下：
![](http://upload-images.jianshu.io/upload_images/8819542-42e2bd6b6d429c26.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![](http://upload-images.jianshu.io/upload_images/8819542-4fe8e9b3b8097efe.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

* 将这两个Nine-Patch图片放到项目的`res/drawable`目录下，并在`res/drawable`目录下新建一个名为`selector_edittext_bg.xml`的xml文件，内容如下：
```xml
<?xml version="1.0" encoding="utf-8"?>
<selector xmlns:android="http://schemas.android.com/apk/res/android">

    <item android:drawable="@drawable/et_pressed" android:state_focused="true"/>
    <item android:drawable="@drawable/et_normal"/>

</selector>
```

* 往`res/values/styles.xml`文件中添加如下内容：
```xml
<style name="MyEtStyle" parent="@android:style/Widget.EditText">
        <item name="android:background">@drawable/selector_edittext_bg</item>
</style>
```

* 在xml布局文件中只需这样设置EditText的style属性即可达到预期效果：
```xml
<EditText
                    android:id="@+id/input_et"
                    style="@style/MyEtStyle"
                    ...
/>
```

* 效果如下截图：
![](http://upload-images.jianshu.io/upload_images/8819542-4e31b30baf7949d2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![](http://upload-images.jianshu.io/upload_images/8819542-2931ec4b25d88a69.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

