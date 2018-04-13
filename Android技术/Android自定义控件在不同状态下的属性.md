在写代码的时候，有时候需要控件在不同状态下显示不同的外观，比如在按钮按下的时候要变颜色，EditText获取焦点时候边框要变颜色等。那么下面就来梳理一下这些是怎么实现的。

# 按钮按下时候变颜色
* 在项目的`drawable`目录下创建`selector_title_imagebutton_bg.xml`文件，内容如下：
```xml
<?xml version="1.0" encoding="utf-8"?>
<selector xmlns:android="http://schemas.android.com/apk/res/android">

    <!-- title栏ImageButton按下去时候的颜色 -->
    <item android:drawable="@drawable/LightBlue" android:state_pressed="true"/>

    <!-- title栏ImageButton正常时候的颜色 -->
    <item android:drawable="@drawable/ThemeDefault"/>


    <!-- 注：LightBlue和ThemeDefault都是在color.xml文件中定义的drawable类型的颜色值 -->

</selector>
```
* 在`values`目录下`styles.xml`文件中增加一个style项，如下：
```xml
    <!-- 标题栏ImageButton的style -->
    <style name="TitleIbStyle" parent="@android:style/Widget.ImageButton">
        <item name="android:background">@drawable/selector_title_imagebutton_bg</item>
    </style>
```
* 在布局xml文件中，创建`ImageButton`时只需设置其style属性为`TitleIbStyle`即可：
```xml
　　　<ImageButton
            android:id="@+id/title_base_left_ib"
            style="@style/TitleIbStyle"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:padding="5dp" />
```

# EditText获取焦点时候边框变颜色
* 在项目的`drawable`目录下新建一个`selector_edittext_bg.xml`文件：
```xml
<?xml version="1.0" encoding="utf-8"?>
<selector xmlns:android="http://schemas.android.com/apk/res/android">

    <item android:drawable="@drawable/et_pressed" android:state_focused="true"/>
    <item android:drawable="@drawable/et_normal"/>
    
    <!-- 注：et_pressed和et_normal是drawable目录下两张相同大小、填充颜色都为白色但边框颜色不同的圆角矩形的png图片 -->
    
</selector>
```
* 在`values`目录下`styles.xml`文件中增加一个`style`项，如下：
```xml
  <!-- EditText的自定义风格 -->
    <style name="MyEtStyle" parent="@android:style/Widget.EditText">
        <item name="android:background">@drawable/selector_edittext_bg</item>
    </style>
```
* 在布局xml文件中，创建`EditText`时只需设置其style属性为`MyEtStyle`即可：
```xml
　　　　　<EditText
                    android:id="@+id/content_et"
                    style="@style/MyEtStyle"
                    android:layout_width="wrap_content"
                    android:layout_height="wrap_content"
```

# 总结
通过上述方式，其实还可以实现很多种其他的自定义效果，有待进一步探索。
