> 参考：[http://blog.csdn.net/guolin_blog/article/details/17357967](http://blog.csdn.net/guolin_blog/article/details/17357967)

在毕设项目中多处用到自定义控件，一直打算总结一下自定义控件的实现方式，今天就来总结一下吧。在此之前学习了郭霖大神博客上面关于自定义View的几篇博文，感觉受益良多，本文中就参考了其中的一些内容。

总结来说，自定义控件的实现有三种方式，分别是：组合控件、自绘控件和继承控件。下面将分别对这三种方式进行介绍。

# （一）组合控件

组合控件，顾名思义就是将一些小的控件组合起来形成一个新的控件，这些小的控件多是系统自带的控件。比如很多应用中普遍使用的标题栏控件，其实用的就是组合控件，那么下面将通过实现一个简单的标题栏自定义控件来说说组合控件的用法。

* 新建一个Android项目，创建自定义标题栏的布局文件`title_bar.xml`：
```xml
<?xml version="1.0" encoding="utf-8"?>
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:background="#0000ff" >

    <Button
        android:id="@+id/left_btn"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_centerVertical="true"
        android:layout_margin="5dp"
        android:background="@drawable/back1_64" />

    <TextView
        android:id="@+id/title_tv"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_centerInParent="true"
        android:text="这是标题"
        android:textColor="#ffffff"
        android:textSize="20sp" />

</RelativeLayout>
```
可见这个标题栏控件还是比较简单的，其中在左边有一个返回按钮，背景是一张事先准备好的图片`back1_64.png`，标题栏中间是标题文字。

* 创建一个类TitleView，继承自RelativeLayout：
```java
public class TitleView extends RelativeLayout {

    // 返回按钮控件
    private Button mLeftBtn;
    // 标题Tv
    private TextView mTitleTv;

    public TitleView(Context context, AttributeSet attrs) {
        super(context, attrs);

        // 加载布局
        LayoutInflater.from(context).inflate(R.layout.title_bar, this);

        // 获取控件
        mLeftBtn = (Button) findViewById(R.id.left_btn);
        mTitleTv = (TextView) findViewById(R.id.title_tv);

    }

    // 为左侧返回按钮添加自定义点击事件
    public void setLeftButtonListener(OnClickListener listener) {
        mLeftBtn.setOnClickListener(listener);
    }

    // 设置标题的方法
    public void setTitleText(String title) {
        mTitleTv.setText(title);
    }
}
```
在TitleView中主要是为自定义的标题栏加载了布局，为返回按钮添加事件监听方法，并提供了设置标题文本的方法。

* 在`activity_main.xml`中引入自定义的标题栏：
```xml
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:id="@+id/main_layout"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical" >

    <com.example.test.TitleView
        android:id="@+id/title_bar"
        android:layout_width="match_parent"
        android:layout_height="wrap_content" >
    </com.example.test.TitleView>

</LinearLayout>
```

* 在MainActivity中获取自定义的标题栏，并且为返回按钮添加自定义点击事件：
```java
private TitleView mTitleBar;
　　　　 mTitleBar = (TitleView) findViewById(R.id.title_bar);

        mTitleBar.setLeftButtonListener(new OnClickListener() {

            @Override
            public void onClick(View v) {
                Toast.makeText(MainActivity.this, "点击了返回按钮", Toast.LENGTH_SHORT)
                        .show();
                finish();
            }
        });
```

* 运行效果如下：
![](http://upload-images.jianshu.io/upload_images/8819542-894e9ad90ade4f7a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

这样就用组合的方式实现了自定义标题栏，其实经过更多的组合还可以创建出功能更为复杂的自定义控件，比如自定义搜索栏等。

# （二）自绘控件
自绘控件的内容都是自己绘制出来的，在View的onDraw方法中完成绘制。下面就实现一个简单的计数器，每点击它一次，计数值就加1并显示出来。

* 创建CounterView类，继承自View，实现OnClickListener接口：
```java
public class CounterView extends View implements OnClickListener {

    // 定义画笔
    private Paint mPaint;
    // 用于获取文字的宽和高
    private Rect mBounds;
    // 计数值，每点击一次本控件，其值增加1
    private int mCount;

    public CounterView(Context context, AttributeSet attrs) {
        super(context, attrs);

        // 初始化画笔、Rect
        mPaint = new Paint(Paint.ANTI_ALIAS_FLAG);
        mBounds = new Rect();
        // 本控件的点击事件
        setOnClickListener(this);
    }

    @Override
    protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);

        mPaint.setColor(Color.BLUE);
        // 绘制一个填充色为蓝色的矩形
        canvas.drawRect(0, 0, getWidth(), getHeight(), mPaint);

        mPaint.setColor(Color.YELLOW);
        mPaint.setTextSize(50);
        String text = String.valueOf(mCount);
        // 获取文字的宽和高
        mPaint.getTextBounds(text, 0, text.length(), mBounds);
        float textWidth = mBounds.width();
        float textHeight = mBounds.height();

        // 绘制字符串
        canvas.drawText(text, getWidth() / 2 - textWidth / 2, getHeight() / 2
                + textHeight / 2, mPaint);
    }

    @Override
    public void onClick(View v) {
        mCount ++;
        
        // 重绘
        invalidate();
    }

}
```
* 在`activity_main.xml`中引入该自定义布局：
```xml
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:id="@+id/main_layout"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical" >

    <com.example.test.CounterView
        android:id="@+id/counter_view"
        android:layout_width="100dp"
        android:layout_height="100dp"
        android:layout_gravity="center_horizontal|top"
        android:layout_margin="20dp" />

</LinearLayout>
```
* 运行效果如下：
![image.png](http://upload-images.jianshu.io/upload_images/8819542-3ad6e8631d40a561.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


# （三）继承控件
就是继承已有的控件，创建新控件，保留继承的父控件的特性，并且还可以引入新特性。下面就以支持横向滑动删除列表项的自定义ListView的实现来介绍。

* 创建删除按钮布局`delete_btn.xml`，这个布局是在横向滑动列表项后显示的：
```xml
<?xml version="1.0" encoding="utf-8"?>
<Button xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:background="#FF0000"
    android:padding="5dp"
    android:text="删除"
    android:textColor="#FFFFFF"
    android:textSize="16sp" >

</Button>
```
* 创建CustomListView类，继承自ListView，并实现了OnTouchListener和OnGestureListener接口：
```java
public class CustomListView extends ListView implements OnTouchListener,
        OnGestureListener {

    // 手势动作探测器
    private GestureDetector mGestureDetector;

    // 删除事件监听器
    public interface OnDeleteListener {
        void onDelete(int index);
    }

    private OnDeleteListener mOnDeleteListener;

    // 删除按钮
    private View mDeleteBtn;

    // 列表项布局
    private ViewGroup mItemLayout;

    // 选择的列表项
    private int mSelectedItem;

    // 当前删除按钮是否显示出来了
    private boolean isDeleteShown;

    public CustomListView(Context context, AttributeSet attrs) {
        super(context, attrs);

        // 创建手势监听器对象
        mGestureDetector = new GestureDetector(getContext(), this);

        // 监听onTouch事件
        setOnTouchListener(this);
    }

    // 设置删除监听事件
    public void setOnDeleteListener(OnDeleteListener listener) {
        mOnDeleteListener = listener;
    }

    // 触摸监听事件
    @Override
    public boolean onTouch(View v, MotionEvent event) {
        if (isDeleteShown) {
            hideDelete();
            return false;
        } else {
            return mGestureDetector.onTouchEvent(event);
        }
    }

    @Override
    public boolean onDown(MotionEvent e) {
        if (!isDeleteShown) {
            mSelectedItem = pointToPosition((int) e.getX(), (int) e.getY());
        }
        return false;
    }

    @Override
    public boolean onFling(MotionEvent e1, MotionEvent e2, float velocityX,
            float velocityY) {
        // 如果当前删除按钮没有显示出来，并且x方向滑动的速度大于y方向的滑动速度
        if (!isDeleteShown && Math.abs(velocityX) > Math.abs(velocityY)) {
            mDeleteBtn = LayoutInflater.from(getContext()).inflate(
                    R.layout.delete_btn, null);

            mDeleteBtn.setOnClickListener(new OnClickListener() {

                @Override
                public void onClick(View v) {
                    mItemLayout.removeView(mDeleteBtn);
                    mDeleteBtn = null;
                    isDeleteShown = false;
                    mOnDeleteListener.onDelete(mSelectedItem);
                }
            });

            mItemLayout = (ViewGroup) getChildAt(mSelectedItem
                    - getFirstVisiblePosition());

            RelativeLayout.LayoutParams params = new RelativeLayout.LayoutParams(
                    LayoutParams.WRAP_CONTENT, LayoutParams.WRAP_CONTENT);
            params.addRule(RelativeLayout.ALIGN_PARENT_RIGHT);
            params.addRule(RelativeLayout.CENTER_VERTICAL);

            mItemLayout.addView(mDeleteBtn, params);
            isDeleteShown = true;
        }

        return false;
    }

    // 隐藏删除按钮
    public void hideDelete() {
        mItemLayout.removeView(mDeleteBtn);
        mDeleteBtn = null;
        isDeleteShown = false;
    }

    public boolean isDeleteShown() {
        return isDeleteShown;
    }
    
    /**
     * 后面几个方法本例中没有用到
     */
    @Override
    public void onShowPress(MotionEvent e) {

    }

    @Override
    public boolean onSingleTapUp(MotionEvent e) {
        return false;
    }

    @Override
    public boolean onScroll(MotionEvent e1, MotionEvent e2, float distanceX,
            float distanceY) {
        return false;
    }

    @Override
    public void onLongPress(MotionEvent e) {

    }

}
```
* 定义列表项布局`custom_listview_item.xml`，它的结构很简单，只包含了一个TextView：
```xml
<?xml version="1.0" encoding="utf-8"?>
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:descendantFocusability="blocksDescendants" >

    <TextView
        android:id="@+id/content_tv"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_centerVertical="true"
        android:layout_margin="30dp"
        android:gravity="center_vertical|left" />

</RelativeLayout>
```
* 定义适配器类CustomListViewAdapter，继承自ArrayAdapter<String>：
```java
public class CustomListViewAdapter extends ArrayAdapter<String> {

    public CustomListViewAdapter(Context context, int textViewResourceId,
            List<String> objects) {
        super(context, textViewResourceId, objects);
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        View view;

        if (convertView == null) {
            view = LayoutInflater.from(getContext()).inflate(
                    R.layout.custom_listview_item, null);
        } else {
            view = convertView;
        }

        TextView contentTv = (TextView) view.findViewById(R.id.content_tv);
        contentTv.setText(getItem(position));

        return view;
    }

}
```
* 在`activity_main.xml`中引入自定义的ListView：
```xml
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:id="@+id/main_layout"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical" >

    <com.example.test.CustomListView
        android:id="@+id/custom_lv"
        android:layout_width="match_parent"
        android:layout_height="wrap_content" />

</LinearLayout>
```
* 在MainActivity中对列表做初始化、设置列表项删除按钮点击事件等处理：
```java
public class MainActivity extends Activity {

    // 自定义Lv
    private CustomListView mCustomLv;
    // 自定义适配器
    private CustomListViewAdapter mAdapter;
    // 内容列表
    private List<String> contentList = new ArrayList<String>();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        setContentView(R.layout.activity_main);

        initContentList();

        mCustomLv = (CustomListView) findViewById(R.id.custom_lv);
        mCustomLv.setOnDeleteListener(new OnDeleteListener() {

            @Override
            public void onDelete(int index) {
                contentList.remove(index);
                mAdapter.notifyDataSetChanged();
            }
        });

        mAdapter = new CustomListViewAdapter(this, 0, contentList);
        mCustomLv.setAdapter(mAdapter);
    }

    // 初始化内容列表
    private void initContentList() {
        for (int i = 0; i < 20; i++) {
            contentList.add("内容项" + i);
        }
    }

    @Override
    public void onBackPressed() {
        if (mCustomLv.isDeleteShown()) {
            mCustomLv.hideDelete();
            return;
        }
        super.onBackPressed();
    }

}
```
* 运行效果如下：
![image.png](http://upload-images.jianshu.io/upload_images/8819542-66b42093c813ec2e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
