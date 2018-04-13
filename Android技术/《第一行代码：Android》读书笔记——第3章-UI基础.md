# （一）Android常用控件及简单用法
### 用法总结如下图：
![image.png](http://upload-images.jianshu.io/upload_images/8819542-636ec8a27ed89c56.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 补充：
* `margin`：外边距；`padding`：内边距。
* `gravity`：子元素的位置；`layout_gravity`：子元素在父元素中的位置。
* 当布局方向为横向时，不能指定子元素在横向上的对齐方式；竖向同理。

# （二）四种布局
### 布局与控件的嵌套关系：
![image.png](http://upload-images.jianshu.io/upload_images/8819542-d9160c51086d0b5d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 四种基本布局
![image.png](http://upload-images.jianshu.io/upload_images/8819542-ea9a49fa257b547e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

# （三）自定义控件的使用　　
### Android中控件和布局的继承结构图：
![image.png](http://upload-images.jianshu.io/upload_images/8819542-ef34dafcddb2320b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 在xml文件中引入布局
假如新建了一个名为`title.xml`的布局文件，作为标题栏，然后在`activity_main.xml`中可以用`<include layout="@layout/title" />`这样的方法引入`title.xml`的布局。

### 创建自定义控件并为控件中的元素添加点击事件：
* `title_base.xml`和`color.xml`（用于保存常用颜色）
`title_base.xml`：
```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:background="@drawable/TitleBaseBg"
    android:orientation="horizontal" >

    <LinearLayout
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:layout_gravity="center"
        android:layout_weight="1"
        android:gravity="left"
        android:orientation="vertical" >

        <ImageButton
            android:id="@+id/title_base_left_ib"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:background="@drawable/Transparent"
            android:padding="5dp"
            android:src="@drawable/back1_64" />
    </LinearLayout>

    <LinearLayout
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:layout_gravity="center_vertical"
        android:layout_weight="1"
        android:gravity="center"
        android:orientation="vertical" >

        <TextView
            android:id="@+id/title_base_middle_tv"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="我的App"
            android:textColor="@drawable/White"
            android:textSize="20sp" />
    </LinearLayout>

    <LinearLayout
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:layout_gravity="center"
        android:layout_weight="1"
        android:gravity="right"
        android:orientation="vertical" >

        <ImageButton
            android:id="@+id/title_base_right_ib"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:background="@drawable/Transparent"
            android:padding="5dp"
            android:src="@drawable/add4_64" />
    </LinearLayout>

</LinearLayout>
```
`color.xml`：
```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>

    <drawable name="TitleBaseBg">#ff272636</drawable>
    <drawable name="Transparent">#00ffffff</drawable>
    <drawable name="White">#ffffffff</drawable>

</resources>
```
* `BaseTitleLayout.java`，是个抽象类，继承自`LinearLayout`类：
```java
public abstract class BaseTitleLayout extends LinearLayout {
    protected ImageButton titleBaseLeftIb;
    protected TextView titleBaseMiddleTv;
    protected ImageButton titleBaseRightIb;

    public BaseTitleLayout(Context context, AttributeSet attrs) {
        super(context, attrs);
        LayoutInflater.from(context).inflate(R.layout.title_base, this);

        titleBaseLeftIb = (ImageButton) findViewById(R.id.title_base_left_ib);
        titleBaseMiddleTv = (TextView) findViewById(R.id.title_base_middle_tv);
        titleBaseRightIb = (ImageButton) findViewById(R.id.title_base_right_ib);

        changeUI();
        onLeftClick();
        onRightClick();
    }

    // 改变标题栏按钮、文字、背景等
    protected abstract void changeUI();

    // 标题栏左边按钮的点击事件
    protected abstract void onLeftClick();

    // 标题栏右边按钮的点击事件
    protected abstract void onRightClick();

}
```
* `MainActivityTitleLayout.java`，继承自`BaseTitleLayout`类：
```java
public class MainActivityTitleLayout extends BaseTitleLayout {

    public MainActivityTitleLayout(Context context, AttributeSet attrs) {
        super(context, attrs);

    }

    @Override
    protected void changeUI() {
        titleBaseLeftIb.setVisibility(View.INVISIBLE);
    }

    @Override
    protected void onLeftClick() {

    }

    @Override
    protected void onRightClick() {
        titleBaseRightIb.setOnClickListener(new OnClickListener() {

            @Override
            public void onClick(View v) {
                Toast.makeText(getContext(), "点击了添加按钮", Toast.LENGTH_SHORT)
                        .show();
            }
        });
    }

}
```
* `activity_main.xml`：
```xml
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical" >

    <com.easydo.layout.MainActivityTitleLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content" >
    </com.easydo.layout.MainActivityTitleLayout>

</LinearLayout>
```
* `MainActivity`：
```java
public class MainActivity extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        setContentView(R.layout.activity_main);
    }
}
```
* 运行效果：
![image.png](http://upload-images.jianshu.io/upload_images/8819542-d38fd3fb301e9249.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

# （四）ListView的用法
### 最简单的用法
* xml文件：
```xml
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical" >

    <ListView
        android:id="@+id/content_lv"
        android:layout_width="match_parent"
        android:layout_height="match_parent" >
    </ListView>

</LinearLayout>
```
* `MainActivity`（详细步骤见注释）
```java
public class MainActivity extends Activity {
    // 1.创建数据数组
    private String[] animalList = { "猫", "狗", "狐狸", "小熊", "鱼", "老虎",
            "长颈鹿", "象", "龙猫" };

    ListView listView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // 2.创建以数据列表元素类型为泛型的适配器
        // 构造函数：第一个参数为上下文；第二个参数为列表项的布局，这里用Android自带的布局；第三个参数为第1步中准备好的数据数组.
        // simple_list_item_1:单行显示，其中只有一个TextView
        // simple_list_item_2:双行显示，有两个TextView，两行字大小不一样
        // two_line_list_item:双行显示，有两个TextView，两行字大小一样
        ArrayAdapter<String> adapter = new ArrayAdapter<String>(
                MainActivity.this, android.R.layout.simple_list_item_1,
                animalList);
        // 3.获取xml中的ListView实例
        listView = (ListView) findViewById(R.id.content_lv);

        // 4.用第2步创建好的适配器来设置ListView实例的内容
        listView.setAdapter(adapter);
    }
}
```
* 运行结果：
![image.png](http://upload-images.jianshu.io/upload_images/8819542-a962af46181fe641.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 定制的ListView界面
上面的ListView每个项只能显示一个文本，太单调了，下面通过定制的方式让它丰富起来。实现左边显示一个图片，右边显示动物名字的效果。
步骤如下：
* 创建一个实体类`Animal`，作为`ListView`适配器的类型：
```java
public class Animal {
    private String name;
    private int imageId;

    public Animal(String name, int imageId) {
        this.name = name;
        // 对应的图片ID
        this.imageId = imageId;
    }

    public String getName() {
        return name;
    }

    public int getImageId() {
        return imageId;
    }

}
```
* 创建`animal_item.xml`文件，其中包含一个`ImageView`和一个`TextView`：
```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical" >

    <ImageView
        android:id="@+id/animal_img_iv"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content" />

    <TextView
        android:id="@+id/animal_name_tv"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_gravity="center"
        android:layout_marginLeft="10dp" />

</LinearLayout>
```
* 创建自定义适配器类`AnimalAdapter`，以`Animal`类为泛型，继承自`ArrayAdapter<Animal>`，重写父类的构造方法和`getView`方法，`getView`方法会在每个子项被滚动到屏幕内的时候调用：
```java
public class AnimalAdapter extends ArrayAdapter<Animal> {

    private int resourceId;

    public AnimalAdapter(Context context, int textViewResourceId,
            List<Animal> objects) {
        super(context, textViewResourceId, objects);
        // textViewResourceId：ListView子项布局的id;objects：数据
        resourceId = textViewResourceId;
    }

    // getView方法会在每个子项被滚动到屏幕内的时候调用
    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        // 1.获取当前项的Animal实例
        Animal animal = getItem(position);

        // 2.为这个子项加载传入的布局
        View view = LayoutInflater.from(getContext()).inflate(resourceId, null);

        // 3.用view的findViewById方法获取到子项布局控件的实例
        ImageView animalImage = (ImageView) view
                .findViewById(R.id.animal_img_iv);
        TextView animalName = (TextView) view.findViewById(R.id.animal_name_tv);

        // 4.设置相应控件的内容
        animalImage.setImageResource(animal.getImageId());
        animalName.setText(animal.getName());

        // 5.返回view
        return view;
    }
}
```
注：在`getView`方法里还可以为`item`的子控件添加点击事件。

* `MainActivity`：
```java
public class MainActivity extends Activity {
    // 1.创建动物名字数组和动物数据列表
    private String[] animalNameList = { "猫", "狗", "狐狸", "小熊", "鱼", "老虎", "长颈鹿",
            "象", "龙猫" };
    private List<Animal> animalList = new ArrayList<Animal>();
    // 为简单起见，把所有动物的图片都设置为ic_launcher
    private int animalImageResourceId = R.drawable.ic_launcher;

    ListView listView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // 2.初始化动物数据
        initAnimals();

        // 3.创建自定义的适配器实例
        // 构造函数：第一个参数：当前上下文；第二个参数：子项布局xml文件；第三个参数：动物数据List
        AnimalAdapter adapter = new AnimalAdapter(MainActivity.this,
                R.layout.animal_item, animalList);

        // 4.获取ListView实例
        listView = (ListView) findViewById(R.id.content_lv);

        // 5.设置适配器
        listView.setAdapter(adapter);

    }

    private void initAnimals() {
        for (int i = 0; i < animalNameList.length; i++) {
            Animal animal = new Animal(animalNameList[i], animalImageResourceId);
            animalList.add(animal);
        }
    }
}
```
* 运行效果：
![image.png](http://upload-images.jianshu.io/upload_images/8819542-8ef3aa3b4bbbb865.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 提升`ListView`的效率
在`AnimalAdapter`的`getView`方法中，每次都将布局重新加载一遍，当快速滚动屏幕时候就会带来性能问题，为此要做一些优化。修改如下：
```java
public class AnimalAdapter extends ArrayAdapter<Animal> {

    private int resourceId;

    public AnimalAdapter(Context context, int textViewResourceId,
            List<Animal> objects) {
        super(context, textViewResourceId, objects);
        // textViewResourceId：ListView子项布局的id;objects：数据
        resourceId = textViewResourceId;
    }

    // getView方法会在每个子项被滚动到屏幕内的时候调用
    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        Animal animal = getItem(position);

        // 用于提升性能
        View view;
        ViewHolder viewHolder;
        if (convertView == null) {
            view = LayoutInflater.from(getContext()).inflate(resourceId, null);
            viewHolder = new ViewHolder();
            viewHolder.animalImage = (ImageView) view
                    .findViewById(R.id.animal_img_iv);
            viewHolder.animalName = (TextView) view
                    .findViewById(R.id.animal_name_tv);

            // 将viewHolder存储在View中
            view.setTag(viewHolder);
        } else {
            view = convertView;

            // 重新获取viewHolder
            viewHolder = (ViewHolder) view.getTag();
        }

        viewHolder.animalImage.setImageResource(animal.getImageId());
        viewHolder.animalName.setText(animal.getName());

        return view;
    }

    // 创建内部类用于缓存，优化性能
    class ViewHolder {
        ImageView animalImage;
        TextView animalName;
    }
}
```
### 为`ListView`的子项添加点击事件
使用`ListView`对象的`setOnItemClickListener`方法，如：
```java
...
        listView.setAdapter(adapter);

        listView.setOnItemClickListener(new OnItemClickListener() {

            @Override
            public void onItemClick(AdapterView<?> parent, View view,
                    int position, long id) {
                Animal animal = animalList.get(position);
                Toast.makeText(MainActivity.this, animal.getName(),
                        Toast.LENGTH_SHORT).show();
            }

        });
```
### 补充：
* xml中设置ListView的分割线颜色：`android:divider="#000"`
* 将ListView定位到最后一行：`listView.setSelection(dataList.size());`

#（五）单位和尺寸

* 像素密度：每英寸所包含的像素数，单位为`dpi`.
x方向像素密度值的获取方法：`float xdpi = getResources().getDisplayMetrics().xdpi;`
y方向像素密度值的获取方法：`float ydpi = getResources().getDisplayMetrics().ydpi;`

* 使用dp为单位来设置控件的宽和高，就可以保证控件在不同像素密度的屏幕上显示的比例是一致的。使用sp来设置字体大小同理。

# （六）制作Nine-Patch图片
详见另一篇博文：[Android制作和使用Nine-Patch图片]()



