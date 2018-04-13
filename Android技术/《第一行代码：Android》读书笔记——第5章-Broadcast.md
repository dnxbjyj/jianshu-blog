# 广播机制简介
### Android广播的分类：
如图所示：
![](http://upload-images.jianshu.io/upload_images/8819542-ce4c076ef776c8ef.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 发送和接收广播
* 发送广播：使用Intent
* 接收广播：Broadcast Receiver

# 接收系统广播
### 动态注册监听网络变化
示例程序：
* `MainActivity`（注：以下代码中的`ToastUtil`是自己简单封装的Toast显示功能的类）：
```java
package com.example.broadcasttest;

import android.app.Activity;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;

public class MainActivity extends Activity {

    private IntentFilter intentFilter;
    private NetworkChangeReceiver networkChangeReceiver;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // 1.创建IntentFilter实例
        intentFilter = new IntentFilter();
        // 2.用addAction方法添加action
        intentFilter.addAction("android.net.conn.CONNECTIVITY_CHANGE");

        // 3.创建内部类NetworkChangeReceiver实例
        networkChangeReceiver = new NetworkChangeReceiver();
        // 4.注册
        registerReceiver(networkChangeReceiver, intentFilter);
    }

    class NetworkChangeReceiver extends BroadcastReceiver {

        @Override
        public void onReceive(Context context, Intent intent) {
            // 创建ConnectivityManager实例
            ConnectivityManager connectivityManager = (ConnectivityManager) getSystemService(Context.CONNECTIVITY_SERVICE);
            // 创建NetworkInfo对象（需要申请权限ACCESS_NETWORK_STATE）
            NetworkInfo networkInfo = connectivityManager
                    .getActiveNetworkInfo();

            // 判断NetworkInfo的状态，即网络是否可用
            if (networkInfo != null && networkInfo.isAvailable()) {
                ToastUtil.showShort(MainActivity.this, "网络可用！");
            } else {
                ToastUtil.showShort(MainActivity.this, "网络不可用！");
            }

        }
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        unregisterReceiver(networkChangeReceiver);
    }

}
```
* 申请权限
```xm
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>
```
* xml文件：不需要添加什么内容。

### 静态注册实现开机启动
动态注册的一个缺点就是，必须要在程序启动之后才能接收到广播，而静态注册就可以在程序还未启动时就能接收到广播，利用这一点就可以实现诸如开机启动程序的功能。

示例程序：
* 新建类`BootCompleteReceiver`继承自`BroadcastReceiver`（注：`onReceive`方法中红不能放过于耗时的逻辑，因为其中不允许使用线程）：
```java
package com.example.broadcasttest;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;

public class BootCompleteReceiver extends BroadcastReceiver {

    @Override
    public void onReceive(Context context, Intent intent) {
        ToastUtil.showShort(context, "BroadcastTest开机启动");
    }

}
```
* 在`AndroidManifest.xml`静态注册广播：
```xml
<application
        android:allowBackup="true"
        android:icon="@drawable/ic_launcher"
        android:label="@string/app_name"
        android:theme="@style/AppTheme" >
        ...
        <receiver android:name=".BootCompleteReceiver" >
            <intent-filter>
                <action android:name="android.intent.action.BOOT_COMPLETED" />
            </intent-filter>
        </receiver>
    </application>
```
* 申请权限：
```xml
 <uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED" />
```

# 发送自定义广播
### 发送标准广播
* 在`BroadcastTes`t项目中：
创建`MyBroadcastReceiver`：
```java
public class MyBroadcastReceiver extends BroadcastReceiver {

    @Override
    public void onReceive(Context context, Intent intent) {
        ToastUtil.showShort(context, "在MyBroadcastReceiver中接收到了自定义广播！");
    }

}
```
在`AndroidManifest.xml`中注册广播接收器：
```xml
<receiver android:name=".MyBroadcastReceiver" >
             <intent-filter>
                 <action android:name="com.example.broadcasttest.MY_BROADCAST" />
             </intent-filter>
</receiver>
```
`activity_main.xml`:
```xml
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical" >

    <Button
        android:id="@+id/send_broadcast_btn"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="发送自定义广播" />

</LinearLayout>
```
`MainActivity`：
```java
package com.example.broadcasttest;

import android.app.Activity;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;

public class MainActivity extends Activity implements OnClickListener {

    private Button sendBroadcast;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        sendBroadcast = (Button) findViewById(R.id.send_broadcast_btn);
        sendBroadcast.setOnClickListener(this);
    }

    @Override
    public void onClick(View v) {
        switch (v.getId()) {
        case R.id.send_broadcast_btn:
            Intent intent = new Intent("com.example.broadcasttest.MY_BROADCAST");
            sendBroadcast(intent);
            break;
        default:
            break;
        }
    }
}
```
* 创建`BroadcastTest2`项目，在其中：
创建`AnotherBroadcastReceiver`：
```java
public class AnotherBroadcastReceiver extends BroadcastReceiver {

    @Override
    public void onReceive(Context context, Intent intent) {
        ToastUtil.showShort(context, "在AnotherBroadcastReceiver中接收到了自定义广播！");
    }

}
```
在`AndroidManifest.xml`中注册广播接收器：
```xml
<receiver android:name=".AnotherBroadcastReceiver" >
             <intent-filter>
                 <action android:name="com.example.broadcasttest.MY_BROADCAST" />
             </intent-filter>
</receiver>
```
* 同时运行`BroadcastTest`和`BroadcastTest2`程序，然后在`BroadcastTest`中点击“发送自定义广播”按钮，然后就会发现弹出两次Toast显示接收到了广播。

### 发送有序广播
在1中`BroadcastTest`项目的基础上，做以下修改即可（红色加下划线的代码为新增或修改的代码）：
* `MainActivity`中：
```java
@Override
    public void onClick(View v) {
        switch (v.getId()) {
        case R.id.send_broadcast_btn:
            Intent intent = new Intent("com.example.broadcasttest.MY_BROADCAST");
            sendOrderedBroadcast(intent, null);
            break;
        default:
            break;
        }
    }
```
* `AndroidManifest.xml`中：
```xml
<receiver android:name=".MyBroadcastReceiver" >
             <intent-filter android:priority="100" >
                 <action android:name="com.example.broadcasttest.MY_BROADCAST" />
             </intent-filter>
</receiver>
```
* `MyBroadcastReceiver`类中：
```java
public class MyBroadcastReceiver extends BroadcastReceiver {

    @Override
    public void onReceive(Context context, Intent intent) {
        ToastUtil.showShort(context, "在MyBroadcastReceiver中接收到了自定义广播！");
 abortBroadcast();
    }

}
```
* 再运行两个程序，点击发送广播按钮后，发现只看到了一个Toast提示，因为另一个广播接收被截断了。　

# 使用本地广播
以上的广播都是全局广播，也就是任何应用程序都能接收到。而这会引发安全性问题，如果只希望在当前应用程序内部传递广播，就要使用本地广播了。
本地广播的关键是使用`LocalBroadcastManager`来发送广播。示例程序：
* xml文件：
```xml
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical" >

    <Button
        android:id="@+id/send_broadcast_btn"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="发送自定义广播" />

</LinearLayout>
```
* `MainActivity`：
```java
package com.example.broadcasttest;

import android.app.Activity;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.Bundle;
import android.support.v4.content.LocalBroadcastManager;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;

public class MainActivity extends Activity implements OnClickListener {

    private Button sendBroadcast;

    private IntentFilter intentFilter;

    private LocalReceiver localReceiver;
    private LocalBroadcastManager localBroadcastManager;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // 1.获取localBroadcastManager实例
        localBroadcastManager = LocalBroadcastManager.getInstance(this);

        sendBroadcast = (Button) findViewById(R.id.send_broadcast_btn);

        // 2.在点击事件中用LocalBroadcastManager的sendBroadcast方法发送广播
        sendBroadcast.setOnClickListener(this);

        // 3.注册IntentFilter
        intentFilter = new IntentFilter();
        intentFilter.addAction("com.example.broadcasttest.LOCAL_BROADCAST");
        localReceiver = new LocalReceiver();
        localBroadcastManager.registerReceiver(localReceiver, intentFilter);
    }

    @Override
    public void onClick(View v) {
        switch (v.getId()) {
        case R.id.send_broadcast_btn:
            Intent intent = new Intent(
                    "com.example.broadcasttest.LOCAL_BROADCAST");
            localBroadcastManager.sendBroadcast(intent);
            break;
        default:
            break;
        }
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        localBroadcastManager.unregisterReceiver(localReceiver);
    }
}
```
* 注册广播接收器：
```xml
<receiver android:name=".LocalReceiver" >
             <intent-filter>
                 <action android:name="com.example.broadcasttest.LOCAL_BROADCAST" />
             </intent-filter>
</receiver>
```
* 这时如果也让另一个程序接收`LOCAL_BROADCAST`这个广播，会发现是接收不到的。

* 本地广播的优点：
（1）不用担心机密数据泄露。
（2）其他程序无法将广播发送到我们程序的内容，不用担心安全漏洞的问题。
（3）比全局广播更高效。

# 最佳实践——实现强制下线功能
在登录页面输入账号密码进入主界面后，点击强制下线按钮会弹出强制下线Dialog，并且该Dialog不能被取消，当用户点击确定后会发出强制下线广播，再次跳转到登录界面。
* `login.xml`文件：
```xml
<?xml version="1.0" encoding="utf-8"?>
<TableLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:stretchColumns="1" >

    <TableRow>

        <TextView
            android:layout_height="wrap_content"
            android:text="用户名:" />

        <EditText
            android:id="@+id/user_name_et"
            android:layout_height="wrap_content"
            android:hint="请输入用户名" />
    </TableRow>

    <TableRow>

        <TextView
            android:layout_height="wrap_content"
            android:text="密码:" />

        <EditText
            android:id="@+id/password_et"
            android:layout_height="wrap_content" >
        </EditText>
    </TableRow>

    <TableRow>

        <Button
            android:id="@+id/login_bt"
            android:layout_height="wrap_content"
            android:layout_span="2"
            android:text="登录" />
    </TableRow>

</TableLayout>
```
* `ActivityCollector`类：
```java
public class ActivityCollector {
    public static List<Activity> activities = new ArrayList<Activity>();

    public static void addActivity(Activity activity) {
        activities.add(activity);
    }

    public static void removeActivity(Activity activity) {
        activities.remove(activity);
    }

    public static void finishAll() {
        for (Activity activity : activities) {
            if (!activity.isFinishing()) {
                activity.finish();
            }
        }
    }
}
```
* `BaseActivity`类：
```java
public class BaseActivity extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        ActivityCollector.addActivity(this);
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        ActivityCollector.removeActivity(this);
    }
}
```
* `LoginActivity`类：
```java
public class LoginActivity extends BaseActivity {

    private EditText userNameEt;
    private EditText passwordEt;
    private Button loginBt;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.login);

        userNameEt = (EditText) findViewById(R.id.user_name_et);
        passwordEt = (EditText) findViewById(R.id.password_et);
        loginBt = (Button) findViewById(R.id.login_bt);

        loginBt.setOnClickListener(new OnClickListener() {

            @Override
            public void onClick(View v) {
                String userName = userNameEt.getText().toString();
                String password = passwordEt.getText().toString();

                // 如果用户名是admin且密码是123456,就认为登录成功
                if (userName.equals("110") && password.equals("123456")) {
                    Intent intent = new Intent(LoginActivity.this,
                            MainActivity.class);
                    startActivity(intent);
                    finish();
                } else {
                    Toast.makeText(LoginActivity.this, "用户名或密码错误!",
                            Toast.LENGTH_SHORT).show();
                }
            }
        });
    }
}
```
* `activity_main.xml`：
```xml
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:paddingBottom="@dimen/activity_vertical_margin"
    android:paddingLeft="@dimen/activity_horizontal_margin"
    android:paddingRight="@dimen/activity_horizontal_margin"
    android:paddingTop="@dimen/activity_vertical_margin"
    tools:context="com.example.broadcastbestpractice.MainActivity" >

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="这里是主界面" />

    <Button
        android:id="@+id/force_offline_bt"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_margin="40dp"
        android:text="发送一个强制下线广播" />

</RelativeLayout>
```
* `MainActivity`类：
```java
public class MainActivity extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button forceOfflineBt = (Button) findViewById(R.id.force_offline_bt);
        forceOfflineBt.setOnClickListener(new OnClickListener() {

            @Override
            public void onClick(View v) {
                Intent intent = new Intent(
                        "com.example.broadcastbestpractice.FORCE_OFFLINE");
                sendBroadcast(intent);
            }
        });
    }

}
```
* `ForceOfflineReceiver`：
```java
public class ForceOfflineReceiver extends BroadcastReceiver {

    @Override
    public void onReceive(final Context context, Intent intent) {
        AlertDialog.Builder dialogBuilder = new AlertDialog.Builder(context);
        dialogBuilder.setTitle("警告");
        dialogBuilder.setMessage("你将要被强制下线!请重新登录!");
        dialogBuilder.setCancelable(false);
        dialogBuilder.setPositiveButton("确定",
                new DialogInterface.OnClickListener() {

                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        ActivityCollector.finishAll();
                        Intent intent = new Intent(context, LoginActivity.class);
                        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                        context.startActivity(intent);
                    }
                });

        AlertDialog alertDialog = dialogBuilder.create();
        alertDialog.getWindow().setType(
                WindowManager.LayoutParams.TYPE_SYSTEM_ALERT);
        alertDialog.show();
    }
}
```
* `AndroidManifest.xml`：
```xml
...
　　　　 <activity
            android:name=".LoginActivity"
            android:label="@string/app_name" >
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />

                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
        <activity android:name=".MainActivity" >
        </activity>

        <receiver
            android:name=".ForceOfflineReceiver"
            android:exported="false" >
            <intent-filter>
                <action android:name="com.example.broadcastbestpractice.FORCE_OFFLINE" />
            </intent-filter>
        </receiver>
...
```
