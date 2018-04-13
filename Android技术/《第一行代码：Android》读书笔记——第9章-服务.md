# Service简介
服务适合执行那种不需要和用户交互而且还要长期运行的任务。所有的服务代码都是默认运行在主线程中，需要在服务内部手动添加子线程，在子线程中执行耗时任务。

# 线程
### 线程的3种用法：
* 继承Thread：
```java
class MyThread extends Thread{
        public void run( ){
                //执行耗时操作
        }
}
new MyThread( ).start( );
```
* 实现Runnable接口：
```java
class MyRunnable implements Runnable{   
       public void run( ){
                //执行耗时操作
        }
}
new Thread(new MyRunnable).start( );
```
* 使用匿名类：
```java
new Thread(new Runnable( ){
        public void run( ){
                //执行耗时操作
        }
}).start( );
```
注：Android不允许在子线程中更新UI，只能在主线程中更新。

# 异步消息处理
不直接在子线程中进行UI操作，而是在子线程中通过`Handler`将`Message`传送给主线程，主线程中的`Handler`接收这个`message`，然后进行UI操作，这叫异步消息处理。

异步消息处理四步曲：
* 在主线程中创建一个`Handler`类型的类成员变量对象，并重写`handleMessage`方法，用于处理相应事件：
```java
private Handler handler = new Handler( ){
        public void handleMessage(Message msg){
                switch(msg.what){        //msg的what字段是一个标志字段，整型
                        case xxx:
                                //在这里可以进行UI操作
                                textView.setText("Change text succeed!")        //改变textView的字符
                                break;
                        default:
                                break;
                }
        }
}
```
* 在子线程中需要进行UI操作时（如按钮点击事件中），创建一个`Message`对象，并通过`Handler`对象的`sendMessage`方法将该消息发送出去，比如：
```java
public static final int UPDATE_TEXT = 1;        //修改UI的标志值
......
@Override
public void onClick(View v){
        switch(v.getId( )){
                case R.id.chage_text_btn:
                        new Thread(new Runnable( ){
                                @Override
                                public void run( ){
                                        Message msg = new Message( );
                                        msg.what = UPDATE_TEXT ;
                                        handler.sendMessage(msg);
                                }
                        }).start( );
                        break;
                
                default:
                        break;
        }
}
```
* 发出的`Message`进入`MessageQueue`队列等待处理。
* `Looper`一直尝试从`MessageQueue`中取出等待处理的消息，最后分发回`handleMessage`方法。
注：Message有一个what字段，可以携带标志识别信息（整型），还有arg1和arg2字段，可以携带整型数据，还有一个obj字段可以带一个Object对象。
* 异步消息处理机制示意图：
![](http://upload-images.jianshu.io/upload_images/8819542-6564f8c479e7570d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

# AsyncTask
`AsyncTask`类是Android对异步消息处理的封装。使用`AsyncTask`需要自定义一个类去继承它：
```java
class MyAsyncTask extends AsyncTask<Params, Progress, Result>
```
三个泛型的含义：
* `Params`：如果在执行AsyncTask时需要传递信息给后台，则传入此参数，如果不需要则为Void。
* `Progress`：如果在后台执行任务过程中，需要在界面上显示进程，则使用这个参数作为进程的单位，一般为Integer。
* `Result`：后台任务执行完后，如果需要对结果进行返回，则使用这个参数作为返回值的类型，如Boolean。

继承时需要实现的几个方法：
* `void onPreExecute( );`
该方法运行在UI线程中，可以进行UI的初始化等操作。
* `boolean doInBackground(Void... params);`
该方法的所有代码都在子线程中运行，在该方法中处理耗时任务，需要调用`publicProgress(Progress)`方法传递进度。
* `void onProgressUpdate(Integer... values);`
当在`doInBackground`中调用`publicProgress`方法时，会自动调用此方法，在这里进行UI操作。
* `void onPostExecute(Boolean result);`
执行收尾工作。

要启用`MyAsyncTask`，在主线程中这样用：`new MyAsyncTask.execute( );`

# Service
### service基本用法
* 定义`Service`：
```java
public class MyService extends Service {
    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    @Override
    public void onCreate() {
        super.onCreate();
        Log.d("MyService", "onCreate executed");
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        Log.d("MyService", "onStartCommand executed");
        return super.onStartCommand(intent, flags, startId);
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        Log.d("MyService", "onDestroy executed");
    }
}
```
* Service类中有一个抽象方法`onBind`，还有三个常用方法：
`onCreate( )`：会在Service创建时调用。
`onStartCommand( )`：会在Service启动时调用。
`onDestory( )`：在Service销毁时调用。
* Service需要在`AndroidManifest.xml`中注册。
```xml
<application
        ... >
        <service android:name=".MyService" >
        </service>
        ...
</application>
```
* 启动和停止Service：
```java
// 启动：
Intent startIntent = new Intent(this, MyService.class);
startService(startIntent);

//停止：
Intent stopIntent = new Intent(this, MyService.class);
stopService(stopIntent);
```
### Activity和Service通信
* 在Service中安插内线Binder，并在`onBind`方法中发送这个内线：
```java
public class MyService extends Service {

    private DownloadBinder mBinder = new DownloadBinder();

    class DownloadBinder extends Binder {    //自定义Binder，模拟下载功能
        public void startDownload() {
            Log.d("MyService", "startDownload executed");
        }

        public int getProgress() {
            Log.d("MyService", "getProgress executed");
            return 0;
        }
    }
    
    @Override
    public IBinder onBind(Intent intent) {
        return mBinder;
    }
    ...    //其他方法
}
```
* 在Activity中创建内线及`ServiceConnection`，其中的`onServiceConnected`方法即可接收内线`IBinder`并通过向下转型获取`Binder`：
```java
...
    private MyService.DownloadBinder downloadBinder;
    private ServiceConnection connection = new ServiceConnection() {
        @Override
        public void onServiceConnected(ComponentName name, IBinder service) {
            downloadBinder = (MyService.DownloadBinder) service;
            downloadBinder.startDownload();
            downloadBinder.getProgress();
        }

        @Override
        public void onServiceDisconnected(ComponentName name) {

        };
    };
    ...
```
* 在合适的时候（如按钮的点击事件等）绑定Activity与Service：
```java
Intent bindIntent = new Intent(this, MyService.class);
bindService(bindIntent, connection, BIND_AUTO_CREATE);    //BIND_AUTO_CREATE指当绑定后，自动创建Service
```
* 解除绑定：
```java
if(connection != null){
    unbindService(connection);
}
```

### Service的生命周期：
* 每个Service都只会存在一个实例。
* 方法：
```java
startService( )
onCreate( )
onStartCommand( )
onDestory( )
bindService( )
unbindService( )
stopService( )
stopSelf( )    //在Service中任何地方都可以用这个方法结束服务本身
onBind( )
```
* 如果`startService( )`和`bindService( )`都调用了，那么必须同时满足`unbindService( )`和`stopService( )`都被调用才会执行`onDestory( )`方法。
### 前台Service
在系统状态栏中一直显示的可见Service，只需在Service的`onCreate`方法中添加如下代码即可（其实是通知的用法）：
```java
@Override
    public void onCreate() {
        super.onCreate();
        ...
        Notification notification = new Notification(R.drawable.ic_launcher,
                "Notification comes", System.currentTimeMillis());
        Intent notificationIntent = new Intent(this, MainActivity.class);
        PendingIntent pendingIntent = PendingIntent.getActivity(this, 0,
                notificationIntent, 0);
        notification.setLatestEventInfo(this, "This is title",
                "This is content", pendingIntent);
        startForeground(1, notification);
    }
```
### IntentService
服务的代码默认都是在主线程中的，如果直接在服务里去处理一些耗时逻辑，就很容易出现`ANR(Application Not Responding)`的情况。这时就可以方便的使用已经把多线程封装好的`IntentService`类：
```java
public class MyIntentService extends IntentService {

    public MyIntentService() {        //需要一个无参的构造方法，调用父类的有参构造方法
        super("MyIntentService");
    }

    @Override
    protected void onHandleIntent(Intent intent) {    //这个方法默认在子线程中运行
        // 打印当前线程ID
        Log.d("MyIntentService", "Thread id is "
                + Thread.currentThread().getId());

        // 在这里已经是在子线程中运行了，可以执行一些耗时操作，但不能执行UI操作
        try {
            Thread.sleep(1000);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        Log.d("MyIntentService", "onDestroy executed");
    }
}
```
IntentService在任务处理完后，会自动调用`onDestory`方法，不用再去人工调用`unbindService`或`stopService`方法。其他用法和普通Service一样。

# Service最佳实践：后台定时任务
* Android中的定时任务实现方式有两种：Java API的Timer类和Android的Alarm机制。前者会受CPU休眠的影响，后者会唤醒CPU。
* 首先创建一个`LongRunningService`服务，重写其`onStartCommand`方法，在这里面执行定时任务：
```java
import java.util.Date;

import android.app.AlarmManager;
import android.app.PendingIntent;
import android.app.Service;
import android.content.Intent;
import android.os.IBinder;
import android.os.SystemClock;
import android.util.Log;

public class LongRunningService extends Service {

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        //创建子线程打印当前时间，模拟定时任务
        new Thread(new Runnable() {
            @Override
            public void run() {
                Log.d("LongRunningService",
                        "executed at " + new Date().toString());
            }
        }).start();
        //1.创建AlarmManager 
        AlarmManager manager = (AlarmManager) getSystemService(ALARM_SERVICE);
        int aMinute = 60 * 1000; // 一分钟的毫秒数
        long triggerAtTime = SystemClock.elapsedRealtime() + aMinute;
        //2.创建跳到广播接收器的Intent
        Intent i = new Intent(this, AlarmReceiver.class);
        //3.创建PendingIntent 
        PendingIntent pi = PendingIntent.getBroadcast(this, 0, i, 0);
        //4.使用AlarmManager的set方法
        //第一个参数：指定工作类型，有四种：ELAPSED_REALTIME_WAKEUP表示定时任务触发时间从
        //系统开机算起，会唤醒CPU；ELAPSED_REALTIME，同ELAPSED_REALTIME_WAKEUP，但不会唤醒CPU；
        //RTC表示从1970-1-1 00:00算起，不会唤醒CPU，RTC_WAKEUP同RTC，但会唤醒CPU。
        //注：唤醒CPU和唤醒屏幕是不同的概念。
        manager.set(AlarmManager.ELAPSED_REALTIME_WAKEUP, triggerAtTime, pi);
        
        return super.onStartCommand(intent, flags, startId);
    }
}
```
* 创建`AlarmReceiver`类：
```java
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;

public class AlarmReceiver extends BroadcastReceiver {

    @Override
    public void onReceive(Context context, Intent intent) {
        Intent i = new Intent(context, LongRunningService.class);
        context.startService(i);    //反过来再启动服务，交替循环进行下去
    }
}
```
* 在活动中启动服务：
```java
import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
 
public class MainActivity extends Activity {
 
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
 
        Intent i = new Intent(this, LongRunningService.class);
        startService(i);
    }
}
```
* 在`AndroidManifest.xml`中注册服务和广播接收器。
* 分析：刚刚创建的这个定时任务，会每隔一分钟执行一次。
