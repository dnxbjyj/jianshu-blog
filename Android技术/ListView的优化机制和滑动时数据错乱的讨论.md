> 参考：[http://www.myexception.cn/mobile/1612364.html](http://www.myexception.cn/mobile/1612364.html)

# Android ListView的基本用法
* 创建一个实体类`Person`，为其添加`Getter`和`Setter`方法，作为ListView适配器的类型：
```java
public class Person {
    private int imageId;
    private String name;
    private int age;

    public Person(int imageId, String name, int age) {
        this.imageId = imageId;
        this.name = name;
        this.age = age;
    }

    public int getImageId() {
        return imageId;
    }

    public String getName() {
        return name;
    }

    public int getAge() {
        return age;
    }

    public void setImageId(int imageId) {
        this.imageId = imageId;
    }

    public void setName(String name) {
        this.name = name;
    }

    public void setAge(int age) {
        this.age = age;
    }
}
```
* 创建`person_item.xml`文件，其中包含一个`ImageView`和两个`TextView`：
```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:id="@+id/person_item_ll"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:orientation="horizontal" >

    <ImageView
        android:id="@+id/image_iv"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:src="@drawable/img" />

    <LinearLayout
        android:layout_width="0dp"
        android:layout_height="match_parent"
        android:layout_weight="1"
        android:orientation="vertical"
        android:gravity="center" >

        <TextView
            android:id="@+id/name_tv"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:gravity="center"
            android:text="Tom" />

        <TextView
            android:id="@+id/age_tv"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:gravity="center"
            android:text="20" />
    </LinearLayout>

</LinearLayout>
```
* 创建自定义适配器类`PersonAdapter`，以`Person`类为泛型，继承自`ArrayAdapter<Person>`，重写父类的构造方法和`getView`方法，`getView`方法会在每个子项被滚动到屏幕内的时候调用：
```java
public class PersonAdapter extends ArrayAdapter<Person> {
    private int mResourceId;

    public PersonAdapter(Context context, int textViewResourceId,
            List<Person> objects) {
        super(context, textViewResourceId, objects);
        // textViewResourceId：ListView子项布局的id;objects：数据
        mResourceId = textViewResourceId;
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        // 1.获取当前项的Person实例
        Person person = getItem(position);
        
        // 2.为这个子项加载传入的布局
        View view = LayoutInflater.from(getContext()).inflate(mResourceId, null);
        
        // 3.用view的findViewById方法获取到子项布局控件的实例
        ImageView imgIv = (ImageView) view.findViewById(R.id.image_iv);
        TextView nameTv = (TextView) view.findViewById(R.id.name_tv);
        TextView ageTv = (TextView) view.findViewById(R.id.age_tv);
        
        // 4.设置相应控件的内容
        imgIv.setImageResource(person.getImageId());
        nameTv.setText(person.getName());
        ageTv.setText(person.getAge() + "");
        
        // 5.为imgIv设置点击事件，点击它的时候换图片
        final ImageView finalImgIv = imgIv;
        imgIv.setOnClickListener(new OnClickListener() {
            
            @Override
            public void onClick(View v) {
                finalImgIv.setImageResource(R.drawable.another_img);
            }
        });
        
        // 6.返回view
        return view;
    }

}
```
* `activity_main.xml`：
```xml
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical" >

    <ListView
        android:id="@+id/person_info_lv"
        android:layout_width="match_parent"
        android:layout_height="match_parent" >
    </ListView>

</LinearLayout>
```
* `MainActivity`：
```java
public class MainActivity extends Activity {

    private ListView personInfoLv;

    private String[] names;
    private int[] ages;
    private List<Person> persons;
    private int imageId;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        personInfoLv = (ListView) findViewById(R.id.person_info_lv);

        names = new String[] { "AAA", "BBB", "CCC", "DDD", "EEE", "FFF", "GGG",
                "HHH", "III", "JJJ", "KKK", "LLL", "MMM", "NNN", "OOO" };
        ages = new int[names.length];
        persons = new ArrayList<Person>();
        imageId = R.drawable.img;

        for (int i = 0; i < names.length; i++) {
            ages[i] = i + 1;
        }
        // 创建Person信息列表
        for (int i = 0; i < names.length; i++) {
            Person person = new Person(imageId, names[i], ages[i]);
            persons.add(person);
        }
        // 创建adapter
        PersonAdapter adapter = new PersonAdapter(MainActivity.this,
                R.layout.person_item, persons);
        
        // 设置adapter
        personInfoLv.setAdapter(adapter);

    }
}
```
* 运行效果：
![](http://upload-images.jianshu.io/upload_images/8819542-35c181728ad24745.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

# ListView的性能优化及滑动时数据显示错乱问题解决

* 在`adapter`的`getView`方法中，每次都将布局重新加载一遍，当快速滚动屏幕时候就会带来性能问题；此外，`View`的`findViewById`方法对性能的影响也比较大。为此要做一些优化，主要使用缓存和`ViewHolder`两种策略。缓存机制如下图，可以实现item的复用（假设一屏可以容纳7个item）
* 假设现在有两个新需求：一个是把列表的前三项的背景颜色设置成蓝色的，另一个是在每次点击每一item的图片时，不仅要修改图片，还要把修改后的图片id存到列表对象中去，这个可以用控件的`setTag`方法来实现。加上实现优化策略，最终修改原`adapter`如下：
```java
public class PersonAdapter extends ArrayAdapter<Person> {
    private int mResourceId;

    public PersonAdapter(Context context, int textViewResourceId,
            List<Person> objects) {
        super(context, textViewResourceId, objects);
        mResourceId = textViewResourceId;
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        Person person = getItem(position);

        View view;
        ViewHolder viewHolder;

        if (null == convertView) {
            view = LayoutInflater.from(getContext()).inflate(
                    R.layout.person_item, null);

            viewHolder = new ViewHolder();
            viewHolder.imageIv = (ImageView) view.findViewById(R.id.image_iv);
            viewHolder.nameTv = (TextView) view.findViewById(R.id.name_tv);
            viewHolder.ageTv = (TextView) view.findViewById(R.id.age_tv);

            // 点击图片的时候更换图片，并更改列表对象中的imageId的值
            final ViewHolder finalViewHolder = viewHolder;
            viewHolder.imageIv.setOnClickListener(new OnClickListener() {

                @Override
                public void onClick(View v) {
                    Person p = (Person) finalViewHolder.imageIv.getTag();

                    int currentImageId;
                    if (p.getImageId() == R.drawable.img) {
                        finalViewHolder.imageIv
                                .setImageResource(R.drawable.another_img);
                        currentImageId = R.drawable.another_img;
                    } else {
                        finalViewHolder.imageIv
                                .setImageResource(R.drawable.img);
                        currentImageId = R.drawable.img;
                    }

                    p.setImageId(currentImageId);
                }
            });

            view.setTag(viewHolder);
            viewHolder.imageIv.setTag(person);
        } else {
            view = convertView;
            viewHolder = (ViewHolder) view.getTag();
            viewHolder.imageIv.setTag(person);
        }

        viewHolder.imageIv.setImageResource(person.getImageId());
        viewHolder.nameTv.setText(person.getName());
        viewHolder.ageTv.setText(person.getAge() + "");

        // 为前三个item设置背景颜色为蓝色
        if (position < 3) {
            view.setBackgroundColor(0xFF0000FF);
        } 

        return view;
    }

    class ViewHolder {
        ImageView imageIv;
        TextView nameTv;
        TextView ageTv;
    }

}
```
* 这时发现在滑动`ListView`后，不仅是前三个item的背景颜色是蓝色的，而且后面有些项的背景颜色也变成了蓝色的，而且毫无规律可循。滑动几次后的效果如下图所示：
![](http://upload-images.jianshu.io/upload_images/8819542-b5a898dc294e97ef.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
* 这主要是因为缓存复用引起的问题，只需要在原来代码的64行后面添加else判断即可，将不是前三行的item的背景颜色设置成默认的白色的。最终代码如下：
```java
public class PersonAdapter extends ArrayAdapter<Person> {
    private int mResourceId;

    public PersonAdapter(Context context, int textViewResourceId,
            List<Person> objects) {
        super(context, textViewResourceId, objects);
        mResourceId = textViewResourceId;
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        Person person = getItem(position);

        View view;
        ViewHolder viewHolder;

        if (null == convertView) {
            view = LayoutInflater.from(getContext()).inflate(
                    R.layout.person_item, null);

            viewHolder = new ViewHolder();
            viewHolder.imageIv = (ImageView) view.findViewById(R.id.image_iv);
            viewHolder.nameTv = (TextView) view.findViewById(R.id.name_tv);
            viewHolder.ageTv = (TextView) view.findViewById(R.id.age_tv);

            // 点击图片的时候更换图片，并更改列表对象中的imageId的值
            final ViewHolder finalViewHolder = viewHolder;
            viewHolder.imageIv.setOnClickListener(new OnClickListener() {

                @Override
                public void onClick(View v) {
                    Person p = (Person) finalViewHolder.imageIv.getTag();

                    int currentImageId;
                    if (p.getImageId() == R.drawable.img) {
                        finalViewHolder.imageIv
                                .setImageResource(R.drawable.another_img);
                        currentImageId = R.drawable.another_img;
                    } else {
                        finalViewHolder.imageIv
                                .setImageResource(R.drawable.img);
                        currentImageId = R.drawable.img;
                    }

                    p.setImageId(currentImageId);
                }
            });

            view.setTag(viewHolder);
            viewHolder.imageIv.setTag(person);
        } else {
            view = convertView;
            viewHolder = (ViewHolder) view.getTag();
            viewHolder.imageIv.setTag(person);
        }

        viewHolder.imageIv.setImageResource(person.getImageId());
        viewHolder.nameTv.setText(person.getName());
        viewHolder.ageTv.setText(person.getAge() + "");

        // 为前三个item设置背景颜色为蓝色
        if (position < 3) {
            view.setBackgroundColor(0xFF0000FF);
        } else {
            view.setBackgroundColor(0xFFFFFFFF);
        }

        return view;
    }

    class ViewHolder {
        ImageView imageIv;
        TextView nameTv;
        TextView ageTv;
    }

}
```
* 总结：总之防止错乱关键就是一句话：哪里对控件有修改，另外的地方就要把它改回来。
