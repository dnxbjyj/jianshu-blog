在做应用的时候，很多时候是不需要系统自带的标题栏的，而是自己去实现标题栏，这就要去掉系统的标题栏，下面总结了三种方法。全屏也是一样的道理，也总结了实现的三种方法。

# 去除标题栏
### 方法1
在`Activity`的`onCreate`方法中：
```java
requestWindowFeature(Window.FEATURE_NO_TITLE);//去掉标题栏
//注意这句一定要写在setContentView()方法的前面，不然会报错的
```
但是这种方法的缺陷是，因为在`onCreate`方法中才去掉标题栏，所以在这之前会发现标题栏还是会一闪而过，去的不彻底，那么用下面两种方法就能够避免这个问题。

### 方法2
在`AndroidManifest.xml`文件中定义：
```xml
<application 
android:icon="@drawable/icon"  
android:label="@string/app_name" 
android:theme="@android:style/Theme.NoTitleBar">
```
这样就会把整个应用的每个界面都去掉标题栏，如果只是想把某些活动去掉标题栏，那么把`android:theme="@android:style/Theme.NoTitleBar"`属性放在`Activity`标签即可。

### 方法3（推荐，便于维护和扩展）
* 先在`styles.xml`中定义名为`NoTitle`的`style`：
```xml
<style name="AppBaseTheme" parent="android:Theme.Light"></style>
<style name="NoTitle" parent="AppBaseTheme">
         <item name="android:windowNoTitle">true</item>
</style>
```
* 在`AndroidManifest.xml`文件中定义：
```xml
<activity
            android:name="XXX"
            android:label="@string/app_name" 
            android:theme="@style/NoTitle">
```

# 全屏
和去除标题栏的三种方法类似，全屏也有三种方法。
### 方法1
在`Activity`的`onCreate`方法中：
```java
getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN, WindowManager.LayoutParams.FLAG_FULLSCREEN);
```
### 方法2
在`AndroidManifest.xml`文件中定义：
```xml
android:theme="@android:style/Theme.NoTitleBar.Fullscreen"
```
### 方法3（推荐）
* `styles.xml`文件：
```xml
     <!-- 全屏style -->
     <style name="FullScreen" parent="AppBaseTheme">
        <item name="android:windowNoTitle">true</item>
        <item name="android:windowFullscreen">true</item>
    </style>
```
* `AndroidManifest.xml`：
```xml
<activity
             android:name="XXX"
             android:theme="@style/FullScreen">
```
