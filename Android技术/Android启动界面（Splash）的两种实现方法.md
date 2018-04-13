# 用2个Activity实现
用Handler对象的`postDelayed`方法来实现延迟跳转的目的。
补充：Handler的常用方法：
```java
//  立即执行Runnable对象  
public final boolean post(Runnable r);  
//  在指定的时间（uptimeMillis）执行Runnable对象  
public final boolean postAtTime(Runnable r, long uptimeMillis);  
//  在指定的时间间隔（delayMillis）执行Runnable对象  
public final boolean postDelayed(Runnable r, long delayMillis);
```
* `activity_splash.xml`：
```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical" >

    <ImageView
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:src="@drawable/ic_launcher" />

</LinearLayout>
```
* `activity_main.xml`：
```xml
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical" >

    <TextView
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="这里是主界面" />

</LinearLayout>
```
* `SplashActivity`：
```java
package com.example.splashtest;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.view.Window;

public class SplashActivity extends Activity {

    private final int SPLASH_DISPLAY_LENGHT = 3000;
    private Handler handler;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getWindow().requestFeature(Window.FEATURE_NO_TITLE);
        setContentView(R.layout.activity_splash);

        handler = new Handler();
        // 延迟SPLASH_DISPLAY_LENGHT时间然后跳转到MainActivity
        handler.postDelayed(new Runnable() {

            @Override
            public void run() {
                Intent intent = new Intent(SplashActivity.this,
                        MainActivity.class);
                startActivity(intent);
                SplashActivity.this.finish();
            }
        }, SPLASH_DISPLAY_LENGHT);

    }
}
```
* `MainActivity`：
```java
package com.example.splashtest;

import android.app.Activity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;

public class MainActivity extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }
}
```
* 修改`AndroidManifest.xml`文件：
```xml
...
　　　　 <activity
            android:name=".SplashActivity"
            android:label="splash" >
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />

                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
        <activity
            android:name=".MainActivity"
            android:label="@string/app_name" >
        </activity>
　　　　　...
```
* 在`SplashActivity`中禁用返回键：
```java
@Override    
public boolean onKeyDown(int keyCode, KeyEvent event) {  
　　if(keyCode == KeyEvent.KEYCODE_BACK){      
　　　　return  true;
　　}  
　　return  super.onKeyDown(keyCode, event);     

}
```

# 用一个Activity实现
主要利用控件的隐藏来实现。
* xml文件：
```xml
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical" >

    <LinearLayout
        android:id="@+id/splash_lt"
        android:layout_width="match_parent"
        android:layout_height="match_parent" >

        <ImageView
            android:layout_width="match_parent"
            android:layout_height="match_parent"
            android:src="@drawable/ic_launcher" />
    </LinearLayout>

    <TextView
        android:id="@+id/main_tv"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="这是主界面" />

</LinearLayout>
```
* `MainActivity`
```java
package com.example.splashtest2;

import android.app.Activity;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.os.SystemClock;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.Window;
import android.widget.LinearLayout;

public class MainActivity extends Activity {

    private final int STOP_SPLASH = 0;
    private final int SPLASH_TIME = 3000;

    private LinearLayout splashLt;

    private Handler splashHandler = new Handler() {
        public void handleMessage(Message msg) {
            switch (msg.what) {
            case STOP_SPLASH:
                splashLt.setVisibility(View.GONE);
                break;
            default:
                break;
            }

            super.handleMessage(msg);
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getWindow().requestFeature(Window.FEATURE_NO_TITLE);
        setContentView(R.layout.activity_main);

        splashLt = (LinearLayout) findViewById(R.id.splash_lt);

        Message msg = new Message();
        msg.what = STOP_SPLASH;

        // 注：这里必须用延迟发送消息的方法，否则ImageView不会显示出来
        splashHandler.sendMessageDelayed(msg, SPLASH_TIME);
    }

}
```
# 小结
建议使用第一种方法，用两个Activity实现，因为MainActivity中的代码不宜过多。
