本章主要介绍了通知、短信、调用摄像头和相册、播放多媒体文件等内容。　　

# 通知的用法

### 通知的基本用法
见如下代码（详细操作步骤在代码注释中）：
* 先创建一个布局文件，其中只有一个名为“发送通知”的Button，当点击这个按钮的时候发送一条通知：
```xml
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical" >

    <Button
        android:id="@+id/sent_notice_btn"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="发送通知" />

</LinearLayout>
```
* `MainActivity`：
```java
import android.app.Activity;
import android.app.Notification;
import android.app.NotificationManager;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;

public class MainActivity extends Activity implements OnClickListener {

    private Button sendNoticeBtn;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button sendNoticeBtn = (Button) findViewById(R.id.sent_notice_btn);
        sendNoticeBtn.setOnClickListener(this);
    }

    @Override
    public void onClick(View v) {
        switch (v.getId()) {
        case R.id.sent_notice_btn:
            // 1.通过getSystemService方法创建NotificationManager实例
            NotificationManager mgr = (NotificationManager) getSystemService(NOTIFICATION_SERVICE);
            
            // 2.创建Notification实例，它是在屏幕上方一闪而过的那种通知信息
            // 第一个参数表示图标，第二个参数表示通知内容，第三个参数用于指定通知被创建的时间，当下拉状态时，这个时间会显示在对应的通知上
            Notification notification = new Notification(
                    R.drawable.ic_launcher, "您有一条通知",
                    System.currentTimeMillis());
            
            // 3.对下拉状态栏后显示的通知的布局进行设定
            // 第一个参数表示context上下文，第二个参数表示通知的标题，第三个参数表示通知的内容，第四个参数表示点击通知后的行为，这里先传入null
            notification.setLatestEventInfo(this, "这是通知标题", "这是通知内容", null);
            
            // 4.使用NotificationManager的notify方法让通知显示出来
            // 第一个参数：通知的id，具有唯一性；第二个参数：Notification对象
            mgr.notify(1, notification);
            break;

        default:
            break;
        }
    }
}
```
### 为通知加上点击跳转功能（使用PendingIntent）
* 在以上代码的基础上，再创建另一个xml文件，作为点击通知后跳转到的页面：
```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical" >

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="这是通知跳转的页面" />

</LinearLayout>
```
* 创建活动`NotificationActivity`，在其中调用`NotificationManager`的`cancel`方法让状态栏的通知消失：
```java
import android.app.Activity;
import android.app.NotificationManager;
import android.os.Bundle;

public class NotificationActivity extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_notification);

        // 用于让状态栏上的通知消失,这里的1就是在MainActivity中创建通知时为通知设置的id
        NotificationManager mgr = (NotificationManager) getSystemService(NOTIFICATION_SERVICE);
        mgr.cancel(1);
    }
}
```
* 修改`MainActivity`活动的按钮点击事件：
```java
@Override
    public void onClick(View v) {
        switch (v.getId()) {
        case R.id.sent_notice_btn:
            // 1.通过getSystemService方法创建NotificationManager实例
            NotificationManager mgr = (NotificationManager) getSystemService(NOTIFICATION_SERVICE);

            // 2.创建Notification实例，它是在屏幕上方一闪而过的那种通知信息
            // 第一个参数表示图标，第二个参数表示通知内容，第三个参数用于指定通知被创建的时间，当下拉状态时，这个时间会显示在对应的通知上
            Notification notification = new Notification(
                    R.drawable.ic_launcher, "您有一条通知",
                    System.currentTimeMillis());

            // 3.对下拉状态栏后显示的通知的布局和点击行为进行设定
            // 第一个参数表示context上下文，第二个参数表示通知的标题，第三个参数表示通知的内容，第四个参数表示点击通知后的行为，这里先传入null

            // 3.1 创建Intent，用于在点击通知时跳转到NotificationActivity页面：
            Intent intent = new Intent(MainActivity.this,
                    NotificationActivity.class);
            // 3.2 创建PendingIntent
            PendingIntent pi = PendingIntent.getActivity(MainActivity.this, 0,
                    intent, PendingIntent.FLAG_CANCEL_CURRENT);

            notification.setLatestEventInfo(this, "这是通知标题", "这是通知内容", pi);

            // 4.使用NotificationManager的notify方法让通知显示出来
            // 第一个参数：通知的id，具有唯一性；第二个参数：Notification对象
            mgr.notify(1, notification);
            break;

        default:
            break;
        }
    }
```
* 最后注册`NotificationActivity`活动。

### 通知的高级技巧
* 在发送通知的时候同时播放一段音频：只用在发送通知按钮的点击事件中加入如下代码：
```java
...
　　　　　　　// +.在发送通知的时候播放一段音频,这里的路径是手机默认来电铃声
            Uri soundUri = Uri.fromFile(new File(
                    "/system/media/audio/ringtones/Basic_tone.ogg"));
            notification.sound = soundUri;

            // 4.使用NotificationManager的notify方法让通知显示出来
            // 第一个参数：通知的id，具有唯一性；第二个参数：Notification对象
            mgr.notify(1, notification);
　　　　　　　　...
```
* ：用R.E管理器进入`/system/media/audio`，里面有四个文件夹，分别是alarms（闹钟铃声），notifications（通知即短信铃声），ringtones（来电铃声），ui(一些应用程序操作的效果声音比如拍照等）。
* 发送通知时让手机振动：
```java
...
　　　　　　　// +.发送通知时让手机振动：
            // 说明：这个数组下标为0的值表示手机静止的时长（毫秒），下标为1的表示振动的时长，下标为2的表示静止的时长,...以此类推
            // 让手机振动需要申请权限：<uses-permission
            // android:name="android.permission.VIBRATE" />
            long[] vibrates = { 0, 1000, 1000, 1000 };
            notification.vibrate = vibrates;

            // 4.使用NotificationManager的notify方法让通知显示出来
            // 第一个参数：通知的id，具有唯一性；第二个参数：Notification对象
            mgr.notify(1, notification);
　　　　　　　...
```
* 控制LED灯亮
```java
...
            // +.发送通知的时候让LED灯亮
            notification.ledARGB = Color.GREEN; // 控制亮灯的颜色，一般可以选红绿蓝三种颜色
            notification.ledOnMS = 1000; // 灯亮的时长（毫秒）
            notification.ledOffMS = 2000; // 灯暗去的时长,在手机在锁屏状态且用户查看通知之前，灯会交替亮、暗下去
            notification.flags = Notification.FLAG_SHOW_LIGHTS; // 指定通知的行为，这里是亮灯
            // 4.使用NotificationManager的notify方法让通知显示出来
            // 第一个参数：通知的id，具有唯一性；第二个参数：Notification对象
            mgr.notify(1, notification);
            ...
```
* 通知的铃声、振动、灯光的设置使用系统默认值：
```java
            // +.铃声、振动、通知的设置使用系统默认值
            notification.defaults = Notification.DEFAULT_ALL;
```
