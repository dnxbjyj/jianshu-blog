# （一）创建活动

* 创建活动类
创建没有Activity的项目，发现src文件夹是空的，手动创建一个包`com.jyj.demo1`，在包中添加一个名为`MainActivity`的class，该MainActivity类要继承Activity类，并重写`onCreate()`方法.
ps:重写`onCreate`方法时候要先写：`super.onCreate(...)`

* 创建布局
没有布局的活动是不可见的，在`res->layout`目录中添加一个`Android XML file`，比如文件名为`mylayout.xml`,可以在该文件中创建布局，添加`TextView、Button`等控件.

* 加载布局
需要将第（2）步的`layout`文件加载到`MainActivity`中，在第（1）步创建的`MainActivity`的`onCreate()`方法中，使用`setContentView(R.layout.mylayout)`将布局加载进来.
ps:这里的R文件是`com.jyj.demo1`包下的R文件，**而不是`android.R`！！**

* 注册活动
四大组件都要先注册才能使用，在`AndroidManifest.xml`文件中，在`<application>`中添加`<activity>`标签，将需要注册的activity使用下面代码注册：
```xml
android:name=".MainActivity"
```
如果该活动是主活动，即打开程序时候看到的活动，则需要添加：
```xml
<action android:name="android.intent.action.MAIN" />
<category android:name="android.intent.category.LAUNCHER" />
```
总体注册代码如下：
```xml
<activity
    android:name=".MainActivity"
    android:label="MyAPP" >
    
    <intent-filter>
        <action android:name="android.intent.action.MAIN" />
        <category android:name="android.intent.category.LAUNCHER" />
    </intent-filter>
</activity
```

# （二）活动的使用
* 隐藏标题栏
在活动的`onCreate()`方法中，在`setContentView(...)`之前，添加如下一行即可：
```java
requestWindowFeature(Window.FEATURE_NO_TITLE);
```
* 使用Toast
```java
Toast.makeText(MainActivity.this,"Hello",Toast.LENGTH_SHORT).show();
```
* 使用Menu
（1）在res目录新建一个`menu`文件夹，在`menu`中新建一个名为`main.xml`的`Android XML File`，`main.xml`的内容如下.
```xml
<menu xmlns:android="http://schemas.android.com/apk/res/android">
    <item
        android:id="@+id/ add_item"
        android:title="Add" />
    <item
        android:id="@+id/ remove_item"
        android:title="Remove" />
        
</menu>
```
（2）在MainActivity中重写`onCreateOptionsMenu( )`方法，代码如下.
```java
public boolean onCreateOptionsMenu(Menu menu){
    getMenuInflater().inflate(R.menu.main,menu);
    return true;
}
```
（3）为菜单项定义响应事件，在`MainActivity`中重写`onOptionsItemSelected( )`方法，代码如下.
```java
public boolean onOptionsItemSelected(MenuItem item){
    switch(item.getItemId()){
    case R.id.add_item:
        Toast...;
        break;
    case R.id.remove_item:
        Toast...;
        break;
    default:
    }
    return true;
}
```
* 销毁活动
假设有一个按钮button,要为它添加点击事件，当点击它的时候退出程序，那么代码如下：
```java
button.setOnClickListener(new OnClickListener(){
     @Override
     public void onClick(View v){
         finish();
     }
 });
```
# （三）采用Intent切换活动

* 显式Intent
（1）先新建另外一个活动`SecondActivity`,现在就有两个活动了：`MainActivity`和`SecondActivity`.
（2）假设要从`MainActivity`跳转到`SecondActivity`，那么在`MainActivity`中需要跳转的地方（如点击事件中）加入如下代码即可：
```java
Intent intent = new Intent(MainActivity.this,SecondActivity.class);
startActivity(intent);
```
* 隐式Intent
（1）新建活动`SecondActivity`,现在就有两个活动了：`MainActivity`和`SecondActivity`.假设要从`MainActivity`跳转到`SecondActivity`.
（2）注册`SecondActivity`时这样写：
```xml
<activity android:name=".SecondActivity"
     <intent-filter>
         <action android:name="com.jyj.demo1.SECOND_START" />
         <category android:name="android.intent.category.DEFAULT" />
     </intent-filter>
</activity>
```
（3）在`MainActivity`需要跳转到`SecondActivity`的地方添加如下代码：
```java
Intent intent = new Intent("com.jyj.demo1.SECOND_START");
startActivity(intent);
```
ps:某活动注册时`intent-filter`中只能有一个action,但可以有多个category（可以自定义category），其他活动在要跳转到该活动创建intent时，只需满足其中一个category即可跳转到该活动. Intent添加category的方法：
```java
intent.addCategory(com.example.activitytest.MY_CATEGORY
//注：要跳转到的活动在注册时要添加MY_CATEGORY这样一个category，否则会出错
```
* 隐式Intent的其他用法
（1）打开系统的活动
如打开浏览器：
```java
Intent intetn = new Intent(Intent.ACTION_VIEW);
intent.setData(Uri.parse("http://www.baidu.com"));
startActivity(intent);
```
（2）精确指定当前的活动能响应的数据类型
在活动的`intent-filter`中，添加`<data>`标签，用于精确指定该活动能响应的数据类型，包括`android :scheme`用于指定数据的协议部分，如：
```xml
<data android:scheme="http" />
```
data标签可以配置以下内容：
`android: scheme`  用于指定数据的协议部分，如http.
`android: host`  用于指定数据的主机名部分，如www. baidu.com
`android: port`  用于指定数据的端口部分，一般紧随主机名之后.
`android: path`  用于指定主机名和端口之后的部分.
`android: mimeType`  用于指定可以处理的数据类型，运行使用通配符的方式进行指定.

注：假如活动1要跳转到活动2，只有活动1的Intent中携带的Data和活动2的data标签中指定的内容完全一致时，才能跳转成功.

# （四）Intent传递数据

* 向下一个活动传递数据
（1）在第一个活动中，使用`putExtra()`将数据传入intent,如： 
```java
 String data = "FirstActivity's data";
Intent intent = new Intent(FirstActivity.this,SecondActivity.class);
intent.putExtra("extra_data",data);
startActivity(intent);
```
（2）在第二个活动中，这样接收数据：
```java
Intent intent = getIntent();
String data = intent.getStringExtra("extra_data");
Log.d("data from FirstActivity",data);
```
* 返回数据给上一个活动
假设活动2在finish时要返回数据给活动1,步骤如下：
（1）在活动1中button1的点击事件中加入如下代码：
```java
Intent intent = new Intent(FirstActivity.this,SecondActivity.class);
startActivityForResult(intent,1);
```
说明：这里的1为`requestCode`，用于之后判断是不是自己发出去的intent.

（2）在活动2中button2的点击事件中加入如下代码：
```java
Intent intent = new Intent();
String data = "SecondActivity's data for return";
intent.putExtra("data_return",data);
setResult(RESULT_OK,intent);
finish();
```
说明：`RESULT_OK`为`resultCode`,用于在活动1中分辨是哪一个活动返回的数据.

（3）重写活动1的`onActivityResult`方法：
```java
@Override
protected void onActivityResult(int requestCode,int resultCode,Intent data){
    switch(requestCode){
    case 1:
        if(resultCode == RESULT_OK){
            String returnData = data.getStringExtra("data_return");
            Log.d("returnData from SecondActivity",returnData);
        }
        break;
    default:
    }
}
```
（4）如果活动2是按返回键返回的，可以在活动2中重写onBackPressed方法返回数据，方法同第（2）步.

# （五）活动的生命周期
### 活动的状态
* 运行状态：在返回栈栈顶时
* 暂停状态：不可操作，但可见
* 停止状态：完全不可见
* 销毁状态：从栈中移除

### 活动生存周期图
![image.png](http://upload-images.jianshu.io/upload_images/8819542-a9a16af4e34e8305.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 活动的生存周期
* 完整生存期：`onCreate()—>onDestroy()`
* 可见生存期：`onStart()—>onStop()`
* 前台生存期：`onResume()—>onPause()`

### 活动被回收后的数据保存
* 重写`Activity`的`onSaveInstanceState()`方法，该方法携带一个`bundle`参数，`bundle`可以保存各种信息，代码如下：
```java
@Override
protected void onSaveInstanceState(Bundle outState) {
     super.onSaveInstanceState(outState);
     String tempData = "Something you just typed";
     outState.putString("data_key", tempData);
}
```
* 如何恢复呢？在`onCreate()`方法，传入的参数为`Bundle savedInstanceState`,利用这个参数恢复数据：
```java
if(savedInstanceState != null){
     String tempData = savedInstanceState.getString("data_key");
}
```

#（六）活动的启动模式

### standard
在启动活动时，不管它在返回栈中是不是已经存在，都会创建一个新的活动放到返回栈栈顶.这是活动的默认启动模式.
示意图：
![image.png](http://upload-images.jianshu.io/upload_images/8819542-074ecec9117f5681.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### singleTop
在启动活动时，如果发现返回栈的栈顶已经是该活动了，那么就直接使用它，不会再创建新的活动实例；其他情况会创建新的活动实例.
示意图：
![image.png](http://upload-images.jianshu.io/upload_images/8819542-b72a4476f28a8b1a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### singleTask
启动活动前，先检查整改返回栈，如果栈中存在该活动的实例，则不会重新创建，否则重新创建.
示意图：
![image.png](http://upload-images.jianshu.io/upload_images/8819542-f4bc221caa37d30b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### singleInstance
若某活动A被指定为singleInstance的启动模式，那么在A启动时会重新在一个新的返回栈中创建它，A与其他活动不在同一个Task中，其他程序也可以调用活动A的这个实例.
示意图：
![image.png](http://upload-images.jianshu.io/upload_images/8819542-e76b64987a599045.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 指定活动的启动模式的方法：
在`AndroidManifest.xml`文件的`Activity`标签中：
```xml
<activity

　　　　android:launchMode="singleTask"

　　　　... >

　　　　...

</activity>
```
　
# （七）活动的最佳实践

### 知道当前页面是哪个活动
（1）新建一个类：`BaseActivity`，继承`Activity`类.
（2）在`BaseActivity`中打印活动信息：
```java
Log.i("BaseActivity",getClass().getSimpleName());  //获得类名
```
（3）以后编写的所有活动都继承`BaseActivity`即可.

### 随时随地退出程序
写代码时候会遇到这样一个问题：当打开很多活动之后，退出程序需要一直按好多次Back，很麻烦.解决方法如下：
（1）新建一个活动管理类，实现所有活动的添加、删除和finish:
```java
public class ActivityCollector{
    public static List<Activity> activities = new ArrayList<Activity>();
    
    public static void addActivity(Activity activity){
        activities.add(activity);
    }
    
    public static void removeActivity(Activity activity){
        activities.remove(activity);
    }
    
    public static void finishAll(){
        for(Activity activity:activities){
            if(!activity.isFinishing()){
                activity.finish();
            }
        }
    }
}
```
（2）然后修改BaseActivity，在`onCreate`方法中：
```java
ActivityCollector.addActivity(this);
```
在`onDestroy`方法中：
```java
ActivityCollector.removeActivity(this);
```
（3）如果想完全退出程序，只需调用ActivityCollector.finishAll方法即可.

### 给每个活动添加一个合适的启动方法
有时也会遇到这个问题：需要启动一个`SecondActivity`，可是不知道该Activity需要哪些参数，怎么办？
办法：
（1）在`SecondActivity`中添加一个启动自己的方法：
```java
public class SecondActivity extends Activity{
    ...
    public static void startActivity(Context context,String data1,String data2){
        Intent intent = new Intent(context,SecondActivity.class);
        intent.putExtra("param1",data1);
        intent.putExtra("param2",data2);
        startActivity(intent);
    }
}
```
（2）在`FirstActivity`中启动`SecondActivity`的方法为：
```java
SecondActivity.startActivity(FirstActivity.this,"data1","data2");
```












