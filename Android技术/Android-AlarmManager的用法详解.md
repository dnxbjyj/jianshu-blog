在Android的Alarm机制中，使用`AlarmManager`可以实现类似闹钟这样的定时任务。在毕业设计项目中要实现定时任务的功能，所以在这里先进行一下梳理。

# AlarmManager与Broadcast结合实现定时任务
`AlarmManager`主要可以发送定时广播，然后在广播接收器中执行任务的具体逻辑；还可以取消已经创建的定时任务、创建可以周期重复执行的定时任务等，将这几个功能进行封装，封装成`AlarmManagerUtil`类如下：
```java
import android.app.AlarmManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.util.Log;

/**
 * AlarmManager工具类
 *
 */

public class AlarmManagerUtil {
    // 获取AlarmManager实例
    public static AlarmManager getAlarmManager(Context context) {
        return (AlarmManager) context.getSystemService(Context.ALARM_SERVICE);
    }

    // 发送定时广播（执行广播中的定时任务）
    // 参数：
    // context:上下文
    // requestCode:请求码，用于区分不同的任务
    // type:alarm启动类型
    // triggerAtTime:定时任务开启的时间，毫秒为单位
    // cls:广播接收器的class
    public static void sendAlarmBroadcast(Context context, int requestCode,
            int type, long triggerAtTime, Class cls) {
        AlarmManager mgr = getAlarmManager(context);

        Intent intent = new Intent(context, cls);
        PendingIntent pi = PendingIntent.getBroadcast(context, requestCode,
                intent, 0);

        mgr.set(type, triggerAtTime, pi);
    }

    // 取消指定requestCode的定时任务
    // 参数：
    // context:上下文
    // requestCode:请求码，用于区分不同的任务
    // cls:广播接收器的class
    public static void cancelAlarmBroadcast(Context context, int requestCode,
            Class cls) {
        AlarmManager mgr = getAlarmManager(context);

        Intent intent = new Intent(context, cls);
        PendingIntent pi = PendingIntent.getBroadcast(context, requestCode,
                intent, 0);

        mgr.cancel(pi);
        ToastUtil
                .showShort(context, "取消定时服务成功" + " @requestCode:" + requestCode);
        Log.d("取消定时服务成功", "@requestCode:" + requestCode);
    }

    // 周期性执行定时任务
    // 参数：
    // context:上下文
    // requestCode:请求码，用于区分不同的任务
    // type:alarm启动类型
    // startTime:开始的时间，毫秒为单位
    // cycleTime:定时任务的重复周期，毫秒为单位
    // cls:广播接收器的class
    public static void sendRepeatAlarmBroadcast(Context context,
            int requestCode, int type, long startTime, long cycleTime, Class cls) {
        AlarmManager mgr = getAlarmManager(context);

        Intent intent = new Intent(context, cls);
        PendingIntent pi = PendingIntent.getBroadcast(context, requestCode,
                intent, 0);

        mgr.setRepeating(type, startTime, cycleTime, pi);
    }
}
```
其中使用到的其他两个工具类都是项目中经常用到的，代码如下：
`ToastUtil`：
```java
/**
 * Toast提示显示工具类
 * 
 */

import android.content.Context;
import android.widget.Toast;

public class ToastUtil {

    // 短时间显示Toast信息
    public static void showShort(Context context, String info) {
        Toast.makeText(context, info, Toast.LENGTH_SHORT).show();
    }

    // 长时间显示Toast信息
    public static void showLong(Context context, String info) {
        Toast.makeText(context, info, Toast.LENGTH_LONG).show();
    }

}
```
`DateTimeUtil`：
```java
import java.text.DateFormat;
import java.text.DecimalFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Arrays;
import java.util.Calendar;
import java.util.Date;
import java.util.GregorianCalendar;

public class DateTimeUtil {
    // 获取当前时间n[]之后的时间的日期时间字符串（N的单位为Calendar的那些表示时间的常量）
    public static String getNLaterDateTimeString(int nType, int n) {
        Date date = new Date();
        Calendar c = new GregorianCalendar();
        c.setTime(date);
        c.add(nType, n);

        return CalendarToString(c);
    }

    // millis to datetime
    public static String getDateTimeStringFromMillis(long millis) {
        Date date = new Date(millis);
        return (DateToString(date));
    }

    // 把日期时间字符串的时间转换成毫秒值（RTC）
    public static long stringToMillis(String dateTime) {
        Calendar c = StringToGregorianCalendar(dateTime);

        return c.getTimeInMillis();
    }

    // 获取两个日期时间字符串表示的时间之间的毫秒差值
    public static long getDifMillis(String dateTime1, String dateTime2) {
        return (stringToMillis(dateTime1) - stringToMillis(dateTime2));
    }

    // 输入一个表示日期或时间的整型数，输出"01"或"23"这样格式的字符串
    public static String getDoubleNumString(int n) {
        int num = n % 60;

        if (num < 10) {
            return "0" + num;
        } else {
            return num + "";
        }
    }

    // 获取标准日期时间字符串的整型的日期值，如："2015-01-21 00:00:00"，返回：21
    public static int getDayOfMonth(String dateTime) {
        Calendar c = StringToGregorianCalendar(dateTime);
        int day = c.get(Calendar.DAY_OF_MONTH);

        return day;
    }

    // 获取当前时间的日期时间字符串，格式："yyyy-MM-dd HH:mm:ss"
    public static String getCurrentDateTimeString() {
        Date date = new Date();
        return DateToString(date);
    }

    // 获取当前的"yyyy-MM-dd"日期格式字符串
    public static String getCurrentDateString() {
        Date date = new Date();
        return DateToString(date).substring(0, 10);
    }

    // 获取当前的"yyyy-MM"日期格式字符串
    public static String getCurrentMonthString() {
        Date date = new Date();
        return DateToString(date).substring(0, 7);
    }

    // 获取当前的"HH:mm"时间格式字符串
    public static String getCurrentTimeString() {
        Date date = new Date();
        return DateToString(date).substring(11, 16);
    }

    // 获取当前的"HH:mm:ss"时间格式字符串
    public static String getCurrentTimeLongString() {
        Date date = new Date();
        return DateToString(date).substring(11, 19);
    }

    // 由日期时间字符串生成“11月1日 星期一”这样格式的字符串
    public static String getShortDateTimeOfWeek(String dateTime) {
        Calendar c = StringToGregorianCalendar(dateTime);

        int month = c.get(Calendar.MONTH) + 1;
        int day = c.get(Calendar.DAY_OF_MONTH);

        String[] weekStr = new String[] { "星期日", "星期一", "星期二", "星期三", "星期四",
                "星期五", "星期六" };
        String week = weekStr[c.get(Calendar.DAY_OF_WEEK) - 1];

        String result = month + "月" + day + "日" + "  " + week;

        return result;
    }

    // 由日期时间字符串生成“2015年11月1日 星期一”这样格式的字符串
    public static String getDateTimeOfWeek(String dateTime) {
        Calendar c = StringToGregorianCalendar(dateTime);

        int year = c.get(Calendar.YEAR);
        int month = c.get(Calendar.MONTH) + 1;
        int day = c.get(Calendar.DAY_OF_MONTH);

        String[] weekStr = new String[] { "星期日", "星期一", "星期二", "星期三", "星期四",
                "星期五", "星期六" };
        String week = weekStr[c.get(Calendar.DAY_OF_WEEK) - 1];

        String result = year + "年" + month + "月" + day + "日" + "  " + week;

        return result;
    }

    // 由日期时间字符串生成“2015年11月1日 05:43”这样格式的字符串
    public static String getDateTimeOfHourMinute(String dateTime) {
        String result = "";
        String date = dateTime.split(" ")[0];
        String time = dateTime.split(" ")[1];
        String[] dateArr = date.split("-");
        String[] timeArr = time.split(":");

        int year = Integer.parseInt(dateArr[0]);
        int month = Integer.parseInt(dateArr[1]);
        int day = Integer.parseInt(dateArr[2]);

        result = year + "年" + month + "月" + day + "日" + "  " + timeArr[0] + ":"
                + timeArr[1];

        return result;
    }

    // 用年月日生成日期字符串，month取值范围：[0,13]
    public static String getDateString(int year, int month, int day) {
        String m;
        String d;

        if (month >= 9) {
            m = (month + 1) + "";
        } else {
            m = "0" + (month + 1);
        }

        if (day >= 10) {
            d = day + "";
        } else {
            d = "0" + day;
        }

        String dateString = year + "-" + m + "-" + d;
        return dateString;
    }

    // 用年月生成年月日期字符串，month取值范围：[0,13]
    public static String getDateString(int year, int month) {
        String m;
        String d;

        if (month >= 9) {
            m = (month + 1) + "";
        } else {
            m = "0" + (month + 1);
        }

        String dateString = year + "-" + m;
        return dateString;
    }

    // 用时、分生成时间字符串
    public static String getTimeString(int hour, int minute) {
        String h;
        String m;

        if (hour >= 10) {
            h = hour + "";
        } else {
            h = "0" + hour;
        }

        if (minute >= 10) {
            m = minute + "";
        } else {
            m = "0" + minute;
        }

        return h + ":" + m;
    }

    // 用时、分、秒生成时间字符串
    public static String getTimeString(int hour, int minute, int second) {
        String h;
        String m;
        String c;

        if (hour >= 10) {
            h = hour + "";
        } else {
            h = "0" + hour;
        }

        if (minute >= 10) {
            m = minute + "";
        } else {
            m = "0" + minute;
        }

        if (second >= 10) {
            c = second + "";
        } else {
            c = "0" + second;
        }

        return h + ":" + m + ":" + c;
    }

    // 该内部类是用于对日期时间字符串数组进行排序的
    public class DateTimeString implements Comparable<DateTimeString> {
        private String mDateTimeStr;

        public DateTimeString(String dateTimeStr) {
            mDateTimeStr = dateTimeStr;
        }

        @Override
        public int compareTo(DateTimeString another) {
            return compareDateTimeString(mDateTimeStr.toString(),
                    another.toString());
        }

        @Override
        public String toString() {
            return mDateTimeStr;
        }

    }

    // 对日期时间字符串数组进行排序,返回排序后的数组（排序后的顺序是从小到大）
    public static String[] sortDateTimeStringArray(String[] dateTimeStringArray) {
        // 将日期时间字符串数组转换成DateTimeString类型数组，DateTimeString实现了Comparable接口，可以进行排序
        DateTimeString[] tmpArray = new DateTimeString[dateTimeStringArray.length];

        // 生成tmpArray数组
        int i = 0;
        DateTimeUtil tmpUtil = new DateTimeUtil();
        for (String str : dateTimeStringArray) {
            tmpArray[i++] = tmpUtil.new DateTimeString(str);
        }

        // 对tmpArray进行排序
        Arrays.sort(tmpArray);

        String[] result = new String[tmpArray.length];
        i = 0;
        for (DateTimeString str : tmpArray) {
            result[i++] = str.toString();
        }
        return result;
    }

    // 比较两个日期时间字符串的大小，如果str1比str2早，则返回-1，如果相等返回0，否则返回1
    public static int compareDateTimeString(String str1, String str2) {
        Date d1 = StringToDate(str1);
        Date d2 = StringToDate(str2);
        if (d1.getTime() - d2.getTime() < 0) {
            return -1;
        } else if (d1.getTime() - d2.getTime() > 0) {
            return 1;
        } else {
            return 0;
        }

    }

    // 时间日期字符串转换成Date对象
    // 注：dateTimeStr带不带前导0都是可以的，比如"2011-01-01 01:02:03"和"2011-1-1 1:2:3"都是合法的
    public static Date StringToDate(String dateTimeStr) {
        Date date = new Date();
        // DateFormat fmt = DateFormat.getDateTimeInstance();
        DateFormat fmt = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        try {
            date = fmt.parse(dateTimeStr);
            return date;
        } catch (ParseException e) {
            e.printStackTrace();
        }
        return date;
    }

    // Date对象转换成日期时间字符串
    public static String DateToString(Date date) {
        String dateTimeStr = null;
        // DateFormat fmt = DateFormat.getDateTimeInstance();
        DateFormat fmt = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        dateTimeStr = fmt.format(date);
        return dateTimeStr;
    }

    // 字符串转换成Calendar
    public static Calendar StringToGregorianCalendar(String dateTimeStr) {
        Date date = StringToDate(dateTimeStr);
        Calendar calendar = new GregorianCalendar();

        calendar.setTime(date);
        return calendar;
    }

    // Calendar转换成String
    public static String CalendarToString(Calendar calendar) {
        Date date = ((GregorianCalendar) calendar).getTime();
        return DateToString(date);
    }

    // 获取日期时间格式字符串表示的两日期时间之间相隔的天数（天数可为浮点型） AC
    public static double getDayNumDif(String str1, String str2) {
        // DateFormat fmt = DateFormat.getDateTimeInstance();
        DateFormat fmt = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        try {
            Date d1 = fmt.parse(str1);
            Date d2 = fmt.parse(str2);
            long dif = Math.abs(d1.getTime() - d2.getTime());
            double dayDif = (double) (dif) / 1000 / (24 * 60 * 60);

            // 保留两位小数
            DecimalFormat df = new DecimalFormat("0.00");
            return Double.parseDouble(df.format(dayDif));
        } catch (ParseException e) {
            e.printStackTrace();
        }
        return -1;
    }

    // 求算术平均值函数，保留2位小数
    public static double getAverage(double[] data) {
        double sum = 0;
        for (int i = 0; i < data.length; i++) {
            sum += data[i];
        }

        DecimalFormat df = new DecimalFormat("0.00");
        return Double.parseDouble(df.format(sum / data.length));
    }

    // 输入一个时间日期字符串（格式：“yyyy-MM-dd HH:mm:ss”），输出num天后的时间日期字符串（num可为浮点数）
    public static String getNDayLatterDateTime(String str, double num) {
        // 创建日期时间格式对象fmt
        // DateFormat fmt = DateFormat.getDateTimeInstance();
        DateFormat fmt = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        try {
            Date curDate = fmt.parse(str);
            GregorianCalendar calendar = new GregorianCalendar();
            calendar.setTime(curDate);

            calendar.add(Calendar.SECOND, (int) (num * (24 * 60 * 60)));

            Date newDate = calendar.getTime();
            String newDateStr = fmt.format(newDate);
            return newDateStr;
        } catch (ParseException e) {
            e.printStackTrace();
        }
        return "";
    }

}
```
# Demo
根据上面`AlarmManagerUtil`中的方法，下面要编写一个Demo，主要的功能就是能创建和取消可以周期执行的定时任务，定时任务的创建是在服务中执行的，而任务的具体内容是在广播接收器中执行的，并且在手机重启后定时任务还能正常运作。
* 布局文件`activity_main.xml`：
```xml
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical" >

    <Button
        android:id="@+id/start_service_btn"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="开启定时服务" />

    <Button
        android:id="@+id/cancel_service_btn"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="取消定时服务" />

</LinearLayout>
```
* `MainActivity`：
```java
import java.util.Calendar;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;

public class MainActivity extends Activity implements OnClickListener {

    // 开启服务按钮
    private Button startServiceBtn;
    // 取消服务按钮
    private Button cancelServiceBtn;

    // 模拟的task id
    private static int mTaskId = 0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        startServiceBtn = (Button) findViewById(R.id.start_service_btn);
        cancelServiceBtn = (Button) findViewById(R.id.cancel_service_btn);

        startServiceBtn.setOnClickListener(this);
        cancelServiceBtn.setOnClickListener(this);
    }

    @Override
    public void onClick(View v) {
        switch (v.getId()) {
        case R.id.start_service_btn:
            Intent i = new Intent(this, AlarmService.class);
            // 获取20秒之后的日期时间字符串
            i.putExtra("alarm_time",
                    DateTimeUtil.getNLaterDateTimeString(Calendar.SECOND, 20));
            i.putExtra("task_id", mTaskId);
            startService(i);
            break;
        case R.id.cancel_service_btn:
            AlarmManagerUtil.cancelAlarmBroadcast(this, mTaskId,
                    AlarmReceiver.class);
            break;
        default:
            break;
        }
    }
}
```
* 创建一个服务`AlarmService`，为了让不同的定时任务运行在不同的线程中，让`AlarmService`继承支持线程的`IntentService`类：
```java
import java.util.Date;

import android.app.AlarmManager;
import android.app.IntentService;
import android.app.PendingIntent;
import android.app.Service;
import android.content.Intent;
import android.os.IBinder;
import android.os.SystemClock;
import android.util.Log;

public class AlarmService extends IntentService {

    // 从其他地方通过Intent传递过来的提醒时间
    private String alarmDateTime;

    public AlarmService() {
        super("AlarmService");
    }

    @Override
    protected void onHandleIntent(Intent intent) {
        alarmDateTime = intent.getStringExtra("alarm_time");
        // taskId用于区分不同的任务
        int taskId = intent.getIntExtra("task_id", 0);

        Log.d("AlarmService", "executed at " + new Date().toString()
                + " @Thread id：" + Thread.currentThread().getId());

        long alarmDateTimeMillis = DateTimeUtil.stringToMillis(alarmDateTime);

        AlarmManagerUtil.sendRepeatAlarmBroadcast(this, taskId,
                AlarmManager.RTC_WAKEUP, alarmDateTimeMillis, 10 * 1000,
                AlarmReceiver.class);

    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        Log.d("Destroy", "Alarm Service Destroy");
    }

}
```
* 创建广播接收器`AlarmReceiver`：
```java
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.text.method.DateTimeKeyListener;
import android.util.Log;
import android.widget.Toast;

public class AlarmReceiver extends BroadcastReceiver {

    @Override
    public void onReceive(Context context, Intent intent) {
        ToastUtil.showShort(context,
                "从服务启动广播：at " + DateTimeUtil.getCurrentDateTimeString());
        Log.d("Alarm", "从服务启动广播：at " + DateTimeUtil.getCurrentDateTimeString());
    }

}
```
* 为了让定时服务在手机重启后也能正常运行，再创建一个系统广播接收器`BootCompleteReceiver`，监听手机一旦开机完成就启动服务`AlarmService`：
```java
/**
 * 开机重新启动服务AlarmService
 *
 */

public class BootCompleteReceiver extends BroadcastReceiver {
    // 模拟的task id
    private static int mTaskId = 0;

    @Override
    public void onReceive(Context context, Intent intent) {
        Log.d("定时服务", "开机启动");
        ToastUtil.showShort(context, "定时服务开机启动");
        Intent i = new Intent(context, AlarmService.class);
        // 获取3分钟之后的日期时间字符串
        i.putExtra("alarm_time",
                DateTimeUtil.getNLaterDateTimeString(Calendar.MINUTE, 3));
        i.putExtra("task_id", mTaskId);
        context.startService(i);
    }
}
```
* 最后是在`AndroidManifest.xml`文件中注册服务、广播接收器，申请相应的权限：
```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.servicebestpractice"
    android:versionCode="1"
    android:versionName="1.0" >

    <uses-sdk
        android:minSdkVersion="14"
        android:targetSdkVersion="14" />

    <uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED" />

    <application
        android:allowBackup="true"
        android:icon="@drawable/ic_launcher"
        android:label="@string/app_name"
        android:theme="@style/AppTheme" >
        <activity
            android:name=".MainActivity"
            android:label="@string/app_name" >
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />

                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

        <service android:name=".AlarmService" >
        </service>

        <receiver android:name=".AlarmReceiver" >
        </receiver>
        <receiver android:name=".BootCompleteReceiver" >
            <intent-filter>
                <action android:name="android.intent.action.BOOT_COMPLETED" />
            </intent-filter>
        </receiver>
    </application>

</manifest>
```
* 点击`开启定时服务`按钮后一段时间，最后点击`取消定时服务`按钮后的运行结果截图：
![](http://upload-images.jianshu.io/upload_images/8819542-452707fc5f74552d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
* 存在的问题：定时任务在手机上测试时，计时不精确，但在模拟器上是精确的。这个问题现在还没有找到很好的解决方案。　　
