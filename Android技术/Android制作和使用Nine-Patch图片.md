Nine-Patch图片是一种经过特殊处理的png图片，能够指定图片的哪些区域可以被拉伸而哪些区域不可以。

# 普通图片被拉伸时的缺陷
有如下xml文件，其中子LinearLayout的背景图片设置成一个名为chat的png图片：
```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical" >

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:background="@drawable/chat" >
    </LinearLayout>

</LinearLayout>
```
显示效果如下：
![](http://upload-images.jianshu.io/upload_images/8819542-a6003d0b7cf2897b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
而chat.png的原图是这样的：
![](http://upload-images.jianshu.io/upload_images/8819542-5171309690a1b37f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
可见严重变形，因为chat.png的宽度不足以填满整个屏幕的宽度，整张图片被均匀拉伸了，这是不能容忍的！于是我们就要把它处理成Nine-Patch图片。

# Nine-Patch图片的制作方法
* 在Android SDK的tools文件夹下，有一个`draw9patch.bat`的文件，就用它来制作Nine-Patch图片。

* 打开这个软件后，点击`File—>Open 9-patch`将chat.png加载进来，如下：
![](http://upload-images.jianshu.io/upload_images/8819542-a8bd41622775edec.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
* 可以在图片的四个边框绘制一个个小黑点，上边框和左边框的部分表示当图片需要拉伸时就拉伸黑点标记的区域，下边框和右边框绘制的部分则表示内容会被放置的区域，如下图：
![](http://upload-images.jianshu.io/upload_images/8819542-16680b9a4fe8938c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
* 修改好后点击`File—>Save 9-patch`，把绘制好的图片保存成`chat.9.png`，然后把`chat.9.png`再复制到工程的`drawable`目录下，并删除原来的`chat.png`，这时再看效果就没有拉伸变形丑陋的情况了（注意：此时xml中仍然写成：`android:background="@drawable/chat"`而不是：`android:background="@drawable/chat.9"`）
![](http://upload-images.jianshu.io/upload_images/8819542-30e8ebc1a5dad4ed.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
* 注意：制作Nine-Patch图片时每条边的黑线必须是连续的，不能断开，否则图片会失效。
