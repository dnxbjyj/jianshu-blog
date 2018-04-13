创建日期或时间选择窗口需要弹出Dialog的时候，Activity类的showDialog方法已经弃用了，而推荐使用的是DialogFragment，本文总结一下其具体用法。

# 日期选择器
* 创建`MyDatePickerDialog`类，继承自`DatePickerDialog`类，实现构造方法，重写`onDateChanged`方法：
```java
import android.app.DatePickerDialog;
import android.content.Context;
import android.widget.DatePicker;

public class MyDatePickerDialog extends DatePickerDialog {

    public MyDatePickerDialog (Context context, OnDateSetListener callBack,
            int year, int monthOfYear, int dayOfMonth) {
        super(context, callBack, year, monthOfYear, dayOfMonth);
        
        this.setTitle("选择任务的日期");        
        this.setButton2("取消", (OnClickListener)null);
        this.setButton("确定", this);  //setButton和this参数组合表示这个按钮是确定按钮
        
    }

    @Override
    public void onDateChanged(DatePicker view, int year, int month, int day) {
        super.onDateChanged(view, year, month, day);
        this.setTitle("选择任务的日期");
    }

}
```
注：隐藏日期选择器的`日`选择项的方法：在`MyDatePickerDialog`的构造方法中添加一个参数：代表日期选择器类型的整型参数，比如0代表年月日都显示，1表示只显示年和月等，然后用如下代码来隐藏`日`选择项（隐藏年月的方法同理，时间选择器也同理）：
```java
// 获取当前系统的语言
        Locale locale = context.getResources().getConfiguration().locale;
        String language = locale.getLanguage();
　　　　　　  // 隐藏日选择栏
            if (language.endsWith("zh")) {
                ((ViewGroup) ((ViewGroup) this.getDatePicker().getChildAt(0))
                        .getChildAt(0)).getChildAt(2).setVisibility(View.GONE);
            } else {
                ((ViewGroup) ((ViewGroup) this.getDatePicker().getChildAt(0))
                        .getChildAt(0)).getChildAt(1).setVisibility(View.GONE);
            }
```
* 创建`DatePickerFragment`类，继承自`DialogFragment`类并实现`DatePickerDialog.OnDateSetListener`接口，重写其`onCreateDialog`和`onDateSet`方法：
```java
import java.util.Calendar;

import android.app.Dialog;
import android.app.DialogFragment;
import android.os.Bundle;
import android.widget.DatePicker;
import android.app.DatePickerDialog;

public class DatePickerFragment extends DialogFragment implements
        DatePickerDialog.OnDateSetListener {
    @Override
    public Dialog onCreateDialog(Bundle savedInstanceState) {
        final Calendar c = Calendar.getInstance();
        int year = c.get(Calendar.YEAR);
        int month = c.get(Calendar.MONTH);
        int day = c.get(Calendar.DAY_OF_MONTH);
        return new MyDatePickerDialog(getActivity(), this, year, month, day);
    }

    @Override
    public void onDateSet(DatePicker view, int year, int month, int day) {

    }

}
```
* 在活动中显示日期选择器：
```java
DatePickerFragment datePickerFrg = new DatePickerFragment() {
                @Override
                public void onDateSet(DatePicker view, int year, int month,
                        int day) {
                    Log.d("DateSet","选择的日期是：" + year +"-" + (month + 1) + "-" + day);                }
            };
            datePickerFrg.show(getFragmentManager(), "datePickerFrg");
```
* 效果：
![](http://upload-images.jianshu.io/upload_images/8819542-a1dac034e8d56fe0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

# 时间选择器
时间选择器的使用其实和日期选择器差不多。
* 创建`MyTimePickerDialog`类，继承自`TimePickerDialog`，实现构造方法，重写`onTimeChanged`方法：
```java
import android.app.TimePickerDialog;
import android.content.Context;
import android.content.DialogInterface.OnClickListener;
import android.widget.TimePicker;

public class MyTimePickerDialog extends TimePickerDialog {

    public MyTimePickerDialog (Context context, OnTimeSetListener callBack,
            int hourOfDay, int minute, boolean is24HourView) {
        super(context, callBack, hourOfDay, minute, is24HourView);
        
        this.setTitle("选择任务的时间");        
        this.setButton2("取消", (OnClickListener)null);
        this.setButton("确定", this);  //setButton和this参数组合表示这个按钮是确定按钮
    }
    
    @Override
    public void onTimeChanged(TimePicker view, int hourOfDay, int minute) {
        super.onTimeChanged(view, hourOfDay, minute);
        this.setTitle("选择任务的时间");    
    }

}
```
* 创建`TimePickerFragment`类，继承自`DialogFragment`类并实现`TimePickerDialog.OnTimeSetListener`接口，重写其`onCreateDialog`和`onTimeSet`方法：
```java
public class TimePickerFragment extends DialogFragment implements
        TimePickerDialog.OnTimeSetListener {

    @Override
    public Dialog onCreateDialog(Bundle savedInstanceState) {
        final Calendar calendar = Calendar.getInstance();
        int hour = calendar.get(Calendar.HOUR_OF_DAY);
        int minute = calendar.get(Calendar.MINUTE);

        return new MyTimePickerDialog(getActivity(), this, hour, minute,
                DateFormat.is24HourFormat(getActivity()));
    }

    @Override
    public void onTimeSet(TimePicker view, int hourOfDay, int minute) {

    }
}
```
* 在活动中显示时间选择器：
```java
TimePickerFragment timePickerFrg = new TimePickerFragment() {
                @Override
                public void onTimeSet(android.widget.TimePicker view,
                        int hourOfDay, int minute) {
                    Log.d("TimeSet", "选择的时间是：" + hourOfDay + ":" + minute);
                };
            };
            timePickerFrg.show(getFragmentManager(), "timePickerFrg");
```
* 效果：
![](http://upload-images.jianshu.io/upload_images/8819542-ba1c180a11d2d095.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
