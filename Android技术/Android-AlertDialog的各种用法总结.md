> 参考：[Android的AlertDialog详解](http://www.2cto.com/kf/201205/131876.html "http://www.2cto.com/kf/201205/131876.html")

# 最简单的用法（详见注释）
```java
            // 1、创建简单的AlertDialog // AlertDialog的构造方法全部是Protected的，
            // 所以不能直接通过new一个AlertDialog来创建出一个AlertDialog; //
            // (1)要创建一个AlertDialog，就要用到AlertDialog.Builder
            AlertDialog.Builder dialog = new AlertDialog.Builder(this);

            // (2)设置各种属性 // 注：不设置哪项属性，这个属性就默认不会显示出来
            dialog.setTitle("这是一个简单的对话框");
            dialog.setIcon(R.drawable.dictation2_64);
            dialog.setMessage("欢迎使用！");

            // (3)设置dialog可否被取消 
            dialog.setCancelable(true);

            // (4)显示出来 
            dialog.show();
```
效果如下：
![](http://upload-images.jianshu.io/upload_images/8819542-ced4939c135d44bc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

# 带按钮的AlertDialog
```java
// 2、带按钮的AlertDialog
            AlertDialog.Builder dialog = new AlertDialog.Builder(this);
            dialog.setTitle("确认");
            dialog.setIcon(R.drawable.dictation2_64);
            dialog.setMessage("确定要删除此项吗？");

            // 设置“确定”按钮,使用DialogInterface.OnClickListener接口参数
            dialog.setPositiveButton("确定",
                    new DialogInterface.OnClickListener() {

                        @Override
                        public void onClick(DialogInterface dialog, int which) {
                            Log.d("Dialog", "点击了“确认”按钮");
                        }
                    });

            // 设置“查看详情”按钮,使用DialogInterface.OnClickListener接口参数
            dialog.setNeutralButton("查看详情",
                    new DialogInterface.OnClickListener() {

                        @Override
                        public void onClick(DialogInterface dialog, int which) {
                            Log.d("Dialog", "点击了“查看详情”按钮");
                        }
                    });

            // 设置“取消”按钮,使用DialogInterface.OnClickListener接口参数
            dialog.setNegativeButton("取消",
                    new DialogInterface.OnClickListener() {

                        @Override
                        public void onClick(DialogInterface dialog, int which) {
                            Log.d("Dialog", "点击了“取消”按钮");
                        }
                    });

            dialog.show();
```
效果如下：
![](http://upload-images.jianshu.io/upload_images/8819542-b3c035da4f9e5385.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

# 类似于ListView的AlertDialog
用`setItems(CharSequence[] items, final OnClickListener listener)`方法来实现类似ListView的AlertDialog：
```java
// 3、类似ListView的AlertDialog
            AlertDialog.Builder dialog = new AlertDialog.Builder(this);
            dialog.setTitle("请选择一项运动");
            dialog.setIcon(R.drawable.dictation2_64);
            // 设置为false说明当前dialog是不能用返回键取消的
            dialog.setCancelable(false);
            
            // 列表字符串数组
            final String[] sportsArray = new String[] { "跑步", "篮球", "游泳",
                    "自行车", "羽毛球" };
            // 用于在item的点击事件中，记录选择的是哪一项，初始值设为0.这里用final数组只是因为匿名内部类中只能使用外部终态的变量
            final int selectedIndex[] = { 0 };

            // 用setItems方法来实现
            dialog.setItems(sportsArray, new DialogInterface.OnClickListener() {

                @Override
                public void onClick(DialogInterface dialog, int which) {
                    selectedIndex[0] = which;
                    Log.d("Dialog", "选择了：" + sportsArray[selectedIndex[0]]);
                }
            });

            dialog.setNegativeButton("取消",
                    new DialogInterface.OnClickListener() {

                        @Override
                        public void onClick(DialogInterface dialog, int which) {
                            Log.d("Dialog", "点击了“取消”按钮");
                        }
                    });

            dialog.show();
```
效果如下：
![](http://upload-images.jianshu.io/upload_images/8819542-78e6889439e5329c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

# 类似RadioButton的AlertDialog
用`setSingleChoiceItems(CharSequence[] items, int checkedItem, final OnClickListener listener)`方法来实现类似RadioButton的AlertDialog。

第一个参数是要显示的数据的数组，第二个参数是初始值（初始被选中的item），第三个参数是点击某个item的触发事件。
```java
// 4、类似RadioButton的AlertDialog
            AlertDialog.Builder dialog = new AlertDialog.Builder(this);
            dialog.setTitle("请选择一项运动");
            dialog.setIcon(R.drawable.dictation2_64);

            // 列表字符串数组
            final String[] sportsArray = new String[] { "跑步", "篮球", "游泳",
                    "自行车", "羽毛球" };
            // 用于在item的点击事件中，记录选择的是哪一项，初始值设为0.这里用final数组只是因为匿名内部类中只能使用外部终态的变量
            final int selectedIndex[] = { 0 };

            // 用setSingleChoiceItems方法来实现
            dialog.setSingleChoiceItems(sportsArray, 0,
                    new DialogInterface.OnClickListener() {

                        @Override
                        public void onClick(DialogInterface dialog, int which) {
                            selectedIndex[0] = which;

                        }
                    });

            dialog.setPositiveButton("确定",
                    new DialogInterface.OnClickListener() {

                        @Override
                        public void onClick(DialogInterface dialog, int which) {
                            Log.d("Dialog", "选择了："
                                    + sportsArray[selectedIndex[0]]);
                        }
                    });

            dialog.setNegativeButton("取消",
                    new DialogInterface.OnClickListener() {

                        @Override
                        public void onClick(DialogInterface dialog, int which) {
                            Log.d("Dialog", "点击了“取消”按钮");
                        }
                    });

            dialog.show();
```
效果如下：
![](http://upload-images.jianshu.io/upload_images/8819542-3bbf96afef1bf555.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

# 类似CheckBox的AlertDialog
用`setMultiChoiceItems(CharSequence[] items, boolean[] checkedItems, final OnMultiChoiceClickListener listener)`方法来实现类似CheckBox的AlertDialog，第一个参数是要显示的数据的数组，第二个参数是选中状态的数组，第三个参数是点击某个item的触发事件。
```java
// 5、类似CheckBox的AlertDialog
            AlertDialog.Builder dialog = new AlertDialog.Builder(this);
            dialog.setTitle("请选择喜欢的运动（可多选）");
            dialog.setIcon(R.drawable.dictation2_64);

            // 列表字符串数组
            final String[] sportsArray = new String[] { "跑步", "篮球", "游泳",
                    "自行车", "羽毛球" };
            // 用于在item的点击事件中，记录选择了哪些项.
            final boolean[] selectedIndex = { true, true, false, false, false };

            // 用setMultiChoiceItems方法来实现
            dialog.setMultiChoiceItems(sportsArray, selectedIndex,
                    new DialogInterface.OnMultiChoiceClickListener() {

                        @Override
                        public void onClick(DialogInterface dialog, int which,
                                boolean isChecked) {
                            selectedIndex[which] = isChecked;
                        }
                    });

            dialog.setPositiveButton("确定",
                    new DialogInterface.OnClickListener() {

                        @Override
                        public void onClick(DialogInterface dialog, int which) {
                            for (int i = 0; i < selectedIndex.length; i++) {
                                if (selectedIndex[i]) {
                                    Log.d("Dialog", "选择了：" + sportsArray[i]);
                                }
                            }
                        }
                    });

            dialog.setNegativeButton("取消",
                    new DialogInterface.OnClickListener() {

                        @Override
                        public void onClick(DialogInterface dialog, int which) {
                            Log.d("Dialog", "点击了“取消”按钮");
                        }
                    });

            dialog.show();
```
效果如下：
![](http://upload-images.jianshu.io/upload_images/8819542-4ee98395d2b58431.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

# 自定义View的AlertDialog
有时候系统自带的AlertDialog风格不能满足我们的需求，就比如说我们要实现一个Login画面，有用户名和密码，这时我们就要用到自定义View的AlertDialog，步骤如下：
* 先创建自定义登录框的布局文件`my_login_view.xml`：
```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical" >

    <LinearLayout
        android:layout_width="fill_parent"
        android:layout_height="wrap_content"
        android:gravity="center"
        android:padding="5dp" >

        <TextView
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="账号：" />

        <EditText
            android:id="@+id/my_login_account_et"
            android:layout_width="0dip"
            android:layout_height="wrap_content"
            android:layout_weight="1" />
    </LinearLayout>

    <LinearLayout
        android:layout_width="fill_parent"
        android:layout_height="wrap_content"
        android:gravity="center"
        android:padding="5dp" >

        <TextView
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="密码：" />

        <EditText
            android:id="@+id/my_login_password_et"
            android:layout_width="0dip"
            android:layout_height="wrap_content"
            android:layout_weight="1"
            android:inputType="numberPassword" />
    </LinearLayout>

</LinearLayout>
```
* 在Activity的合适地方创建自定义的AlertDialog（比如按钮的点击事件中）：
```java
// 6、自定义View的AlertDialog
            AlertDialog.Builder dialog = new AlertDialog.Builder(this);
            dialog.setTitle("用户登录");

            // 取得自定义View
            LayoutInflater layoutInflater = LayoutInflater.from(this);
            final View myLoginView = layoutInflater.inflate(
                    R.layout.my_login_view, null);
            dialog.setView(myLoginView);

            dialog.setPositiveButton("确定",
                    new DialogInterface.OnClickListener() {

                        @Override
                        public void onClick(DialogInterface dialog, int which) {
                            EditText loginAccountEt = (EditText) myLoginView
                                    .findViewById(R.id.my_login_account_et);
                            EditText loginPasswordEt = (EditText) myLoginView
                                    .findViewById(R.id.my_login_password_et);
                            Log.d("MyLogin Dialog", "输入的用户名是："
                                    + loginAccountEt.getText().toString());
                            Log.d("MyLogin Dialog", "输入的密码是："
                                    + loginPasswordEt.getText().toString());
                        }
                    });

            dialog.setNegativeButton("取消",
                    new DialogInterface.OnClickListener() {

                        @Override
                        public void onClick(DialogInterface dialog, int which) {

                        }
                    });

            dialog.show();
```
效果如下：
![](http://upload-images.jianshu.io/upload_images/8819542-67c6b1db5720aaf2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
点击“确定”按钮后LogCat中的内容：
![](http://upload-images.jianshu.io/upload_images/8819542-739d76d5ec541eef.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

