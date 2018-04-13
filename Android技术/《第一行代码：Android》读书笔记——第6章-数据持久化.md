本文主要讲述了Android数据持久化的三种方式：文件存储、SharedPreference存储、SQLite数据库存储。

# 文件存储
其实Android中文件存储方式和Java的文件操作类似，就是用IO流进行操作。文件存储只能保存简单的字符串或二进制数据，不适合保存结构较为复杂的数据。
### 示例程序（代码中有详细注释）
* xml文件：
其中有一个`EditText`，可以在里面输入字符，还有两个`Button`，一个用于保存输入的内容到一个文件中，另一个用于载入相应的文件内容到`EditText`中。
```xml
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical" >

    <EditText
        android:id="@+id/input_et"
        android:layout_width="match_parent"
        android:layout_height="wrap_content" />

    <Button
        android:id="@+id/save_btn"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="保存" />


    <Button
        android:id="@+id/load_btn"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="载入文件内容" />

</LinearLayout>
```
* `MainActivity`：
```java
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;

import android.app.Activity;
import android.content.Context;
import android.os.Bundle;
import android.text.TextUtils;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

public class MainActivity extends Activity implements OnClickListener {

    private String dataFileName = "MyDataFile";

    private EditText inputEt;
    private Button saveBtn;
    private Button loadBtn;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        inputEt = (EditText) findViewById(R.id.input_et);
        saveBtn = (Button) findViewById(R.id.save_btn);
        loadBtn = (Button) findViewById(R.id.load_btn);

        saveBtn.setOnClickListener(this);
        loadBtn.setOnClickListener(this);
    }

    @Override
    public void onClick(View v) {
        switch (v.getId()) {
        case R.id.save_btn:
            String inputText = inputEt.getText().toString();
            if (inputText.length() == 0) {
                Toast.makeText(MainActivity.this, "未输入任何内容！",
                        Toast.LENGTH_SHORT).show();
            } else {
                save(dataFileName, inputText);
                Toast.makeText(MainActivity.this, "保存成功！", Toast.LENGTH_SHORT)
                        .show();
            }
            break;

        case R.id.load_btn:
            String fileContent = load(dataFileName);

            // 用于判断一个字符串是否是null或者空内容的工具方法
            if (!TextUtils.isEmpty(fileContent)) {
                inputEt.setText(fileContent);
                // 让光标移到文字最后
                inputEt.setSelection(fileContent.length());
                Toast.makeText(this, "载入文件内容成功！", Toast.LENGTH_SHORT).show();
            }
            break;
        default:
            break;
        }
    }

    // 保存输入内容到文件的方法
    public void save(String fileName, String inputText) {
        FileOutputStream out = null;
        BufferedWriter writer = null;

        try {
            // 1.用Context类的openFileOutput方法创建FileOutputStream实例
            // MODE_PRIVATE模式是默认操作模式，表示当指定同样文件名时，所写入的内容将会覆盖原来的内容
            // MODE_APPEND表示如果该文件已经存在就往文件里面追加内容，不存在就创建新文件
            // 注：这里的文件名不可以包含路径，因为所有的文件都是默认存储到/data/data/包名/files目录的
            out = openFileOutput(fileName, Context.MODE_PRIVATE);

            // 2.用FileOutputStream实例创建OutputStreamWriter实例，再用OutputStreamWriter实例创建BufferedWriter实例
            writer = new BufferedWriter(new OutputStreamWriter(out));

            // 3.写入内容到文件
            writer.write(inputText);

            /**
             * 注:查看该文件的方法： DDMS—>File
             * Explorer—>/data/data/com.example.filepersistencetest(包名)/files/
             * 该目录下即可看到刚刚保存的文件，DDMS按钮下方有一个导出文件，即可把文件导出到电脑上用记事本查看
             */

        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            try {
                if (writer != null) {
                    writer.close();
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

    // 载入并读取文件内容的方法
    public String load(String fileName) {
        FileInputStream in = null;
        BufferedReader reader = null;
        StringBuilder content = new StringBuilder();

        try {
            // 1.用Context类的openFileInput方法创建FileInputStream实例
            in = openFileInput(fileName);

            if (in == null) {
                Toast.makeText(MainActivity.this, "数据文件不存在！",
                        Toast.LENGTH_SHORT).show();
                return "";
            }

            // 2.创建BufferedReader实例
            reader = new BufferedReader(new InputStreamReader(in));

            String line = "";

            // 3.读取每一行
            while ((line = reader.readLine()) != null) {
                content.append(line);
            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            if (reader != null) {
                try {
                    reader.close();
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }

        return content.toString();
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        String inputText = inputEt.getText().toString();
        if (inputText.length() != 0) {
            save(dataFileName, inputText);
        }
    }

}
```
* 用`openFileOutput和openFileInput`创建文件时，参数中的文件名不可以包含路径，因为所有的文件都是默认存储到`/data/data/包名/files`目录的。

* 查看该文件的方法： `DDMS—>File Explorer—>/data/data/com.example.filepersistencetest(包名)/files/`，该目录下即可看到刚刚保存的文件，DDMS按钮下方有一个导出文件按钮，即可把文件导出到电脑上用记事本查看。

# SharedPreferences
`SharedPreferences`用键值对形式存储数据，适合保存程序的一些偏好设置等。SharedPreferences文件会自动存放在`/data/data/包名/shared_prefs`目录下，是xml格式的文件。

### 获取SharedPreferences对象的三种方法
* `Activity`类的`getPreferences`方法，只接收一个模式参数，这个方法会自动把当前活动类名作为`SharedPreferences`文件名。
* `PreferencesManager`类中的`getDefaultSharedPreferences`方法，这是一个静态方法，接收一个`Context`参数，并自动使用当前 应用程序的包名作为前缀来命名`SharedPreferences`文件。
* `Context`类的`getSharedPreferences`方法，接受两个参数，第一个为文件名字符串（不要带路径！），第二个是文件操作模式。

### 向SharedPreferences文件写入数据的步骤
* 用`SharedPreferences`对象的`edit`方法获取`SharedPreferences.Editor`实例：
```java
SharedPreferences.Editor editor = getSharedPreferences("dataFile", MODE_PRIVATE).edit();
```
* 写入数据到`SharedPreferences`中：
```java
editor.putString("name", "m2fox");
editor.putInt("age", 23);
editor.putBoolean("married", false);
```
* 用`commit`方法提交：
```java
editor.commit();
```
### 从SharedPreferences文件读数据的步骤
* 创建`SharedPreferences`实例：
```java
SharedPreferences pref = getSharedPreferences("dataFile", MODE_PRIVATE);
```
* 用`getXXX`方法读取数据：
```java
// 第一个参数表示键名，第二个参数表示如果找不到数据时候返回的默认值
        String name = pref.getString("name", "");
        int age = pref.getInt("age", 0);
        boolean married = pref.getBoolean("married", false);

        Log.d("MainActivity", "name is " + name);
        Log.d("MainActivity", "age is " + age);
        Log.d("MainActivity", "married is " + married);
```
### 示例程序
* XML文件：
```xml
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical" >

    <Button
        android:id="@+id/save_data_btn"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="保存数据" />

    <Button
        android:id="@+id/load_data_btn"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="载入数据" />

</LinearLayout>
```
* `MainActivity`：
```java
package com.example.sharedpreferencestest;

import android.app.Activity;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.Toast;

public class MainActivity extends Activity implements OnClickListener {

    private Button saveDataBtn;
    private Button loadDataBtn;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        saveDataBtn = (Button) findViewById(R.id.save_data_btn);
        loadDataBtn = (Button) findViewById(R.id.load_data_btn);

        saveDataBtn.setOnClickListener(this);
        loadDataBtn.setOnClickListener(this);
    }

    @Override
    public void onClick(View v) {
        switch (v.getId()) {
        case R.id.save_data_btn:
            saveData();
            Toast.makeText(MainActivity.this, "保存数据成功", Toast.LENGTH_SHORT)
                    .show();
            break;
        case R.id.load_data_btn:
            loadData();
            break;
        default:
            break;
        }
    }

    // 保存数据到SharedPreferences
    public void saveData() {
        // 1.用SharedPreferences对象的edit方法获取SharedPreferences.Editor实例
        SharedPreferences.Editor editor = getSharedPreferences("dataFile",
                MODE_PRIVATE).edit();

        // 注：获取SharedPreferences对象还有两种方法：
        // （1）Activity类的getPreferences方法，只接收一个模式参数，这个方法会自动把当前活动类名作为SharedPreferences文件名
        // （2）PreferencesManager类中的getDefaultSharedPreferences方法，这是一个静态方法，接收一个Context参数，并自动使用当前
        // 应用程序的包名作为前缀来命名SharedPreferences文件

        // 2.写入数据到SharedPreferences中
        editor.putString("name", "贾永基");
        editor.putInt("age", 23);
        editor.putBoolean("married", false);

        // 3.用commit方法提交
        // 注：SharedPreferences文件会自动存放在/data/data/包名/shared_prefs目录下，是xml格式的文件
        editor.commit();
    }

    // 从SharedPreferences读数据
    public void loadData() {
        SharedPreferences pref = getSharedPreferences("dataFile", MODE_PRIVATE);

        // 第一个参数表示键名，第二个参数表示如果找不到数据时候返回的默认值
        String name = pref.getString("name", "");
        int age = pref.getInt("age", 0);
        boolean married = pref.getBoolean("married", false);

        Log.d("MainActivity", "name is " + name);
        Log.d("MainActivity", "age is " + age);
        Log.d("MainActivity", "married is " + married);
    }

}
```

# SQLite
SQLite是Android内嵌的轻量级关系型数据库，速度很快，支持标准的SQL语法，还支持ACID事务。

### 创建数据库
继承`SQLiteOpenHelper`类创建自己的类`MyDatabaseHelper`，并实现`onCreate`和`onUpgrade`两个抽象方法，在`onCreate`方法中建表，在`onUpgrade`中升级数据库。
```java
import android.content.Context;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteDatabase.CursorFactory;
import android.database.sqlite.SQLiteOpenHelper;
import android.widget.Toast;

public class MyDatabaseHelper extends SQLiteOpenHelper {

    // 1.将建表语句定义成字符串常量
    public static final String CREATE_BOOK = "create table book(" // 注：表名和字段名称不区分大小写
            + "id integer primary key autoincrement,"
            + "author text,"
            + "price real," + "pages integer," + "name text,"+ "category_id integer)";;

    public static final String CREATE_CATEGORY = "create table category("
            + "id integer primary key autoincrement," + "category_name text,"
            + "category_code integer)";

    private Context mContext;

    public MyDatabaseHelper(Context context, String name,
            CursorFactory factory, int version) {
        super(context, name, factory, version);
        mContext = context;
    }

    @Override
    public void onCreate(SQLiteDatabase db) {
        // 2.用SQLiteDatabase的execSQL方法执行建表语句
        db.execSQL(CREATE_BOOK);
        db.execSQL(CREATE_CATEGORY);

        Toast.makeText(mContext, "创建数据库成功！", Toast.LENGTH_SHORT).show();
    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        switch (oldVersion) {
        case 1:
            db.execSQL(CREATE_CATEGORY);
        case 2: // 注意这里case的最后是不写break的，以应对跨版本升级的情况
            db.execSQL("alter table book add column category_id integer");
        default:
            break;
        }
    }

}
```
创建数据库后，在`adb shell`中可以用命令行方式查看数据库的具体数据，方法如下：
* 打开控制台窗口，输入`adb shell`，然后cd到路径：`/data/data/当前包名/databases/`，使用`ls`查看当前目录里的文件。
* 假设提前创建的数据库名叫`BookStore.db`，那么接着就用`sqlite3 BookStore.db`命令打开数据库，然后可以输入各种SQL语句进行操作。
* 输入`.table`命令可以查看当前数据库的表，`.schema`命令可以查看所有表的建表语句。`.exit`或`.quit`命令可以退出数据库编辑，`exit`命令可以退出`adb shell`。
* 在数据库中查询结果出现乱码的情况的解决（Win7环境）：
在控制台里输入命令：`chcp 65001` 确定—>在命令行标题栏上点击右键，选择【属性】 -【字体】，将字体修改为`Lucida Console` 确定
完成后再通过`adb shell`进入sqlite3，乱码解决.

注：恢复cmd的默认设置：`Win+R` -> 输入`regedit` -> 找到`HKEY_CURRENT_USER\Console\%SystemRoot%_system32_cmd.exe `-> 右键删除文件夹`%SystemRoot%_system32_cmd.exe` -> 重启`cmd`即可。

### 示例程序
* xml文件：
```xml
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical" >

    <Button
        android:id="@+id/create_database_btn"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="创建数据库" />

    <Button
        android:id="@+id/add_data_btn"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="添加数据" />

    <Button
        android:id="@+id/update_data_btn"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="更新数据" />

    <Button
        android:id="@+id/delete_data_btn"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="删除数据" />

    <Button
        android:id="@+id/query_data_btn"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="查询数据" />

    <TextView
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="查询结果：" />

    <TextView
        android:id="@+id/query_result_tv"
        android:layout_width="match_parent"
        android:layout_height="wrap_content" />

</LinearLayout>
```
* `MainActivity`：
```java
package com.example.databasetest2;

import java.util.ArrayList;

import android.app.Activity;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

public class MainActivity extends Activity implements OnClickListener {

    private Button createDatabaseBtn;
    private Button addDataBtn;
    private Button updateDataBtn;
    private Button deleteDataBtn;
    private Button queryDataBtn;
    private TextView queryResultTv;

    private MyDatabaseHelper dbHelper;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // 1.创建MyDatabaseHelper实例
        dbHelper = new MyDatabaseHelper(this, "BookStore.db", null, 3); // 这里的3为数据库版本号

        createDatabaseBtn = (Button) findViewById(R.id.create_database_btn);
        addDataBtn = (Button) findViewById(R.id.add_data_btn);
        updateDataBtn = (Button) findViewById(R.id.update_data_btn);
        deleteDataBtn = (Button) findViewById(R.id.delete_data_btn);
        queryDataBtn = (Button) findViewById(R.id.query_data_btn);
        queryResultTv = (TextView) findViewById(R.id.query_result_tv);

        createDatabaseBtn.setOnClickListener(this);
        addDataBtn.setOnClickListener(this);
        updateDataBtn.setOnClickListener(this);
        deleteDataBtn.setOnClickListener(this);
        queryDataBtn.setOnClickListener(this);
    }

    @Override
    public void onClick(View v) {
        SQLiteDatabase db;
        switch (v.getId()) {
        case R.id.create_database_btn:
            // 2.调用MyDatabaseHelper的getWritableDatabase方法打开数据库
            dbHelper.getWritableDatabase();
            break;
        case R.id.add_data_btn:
            // 先获取SQLiteDatabase实例，然后直接用execSQL方法执行SQL语句的方式往表中插入数据
            db = dbHelper.getWritableDatabase();
            db.execSQL(
                    "insert into book (name,author,pages,price,category_id) values (?,?,?,?,?)",
                    new String[] { "三体", "刘慈欣", "567", "49.9", "1" }); // 注：所有类型的占位符数据都要是字符串，若语句中无占位符参数，则第二个函数参数可为null
            db.execSQL(
                    "insert into book (name,author,pages,price,category_id) values (?,?,?,?,?)",
                    new String[] { "第一行代码——Android", "郭霖", "401", "25.9", "3" });
            break;
        case R.id.update_data_btn:
            db = dbHelper.getWritableDatabase();
            // 更新数据
            db.execSQL("update book set price = ? where name = ?",
                    new String[] { "10.99", "三体" });
            break;
        case R.id.delete_data_btn:
            db = dbHelper.getWritableDatabase();
            // 删除数据
            db.execSQL("delete from book where pages > ?", new String[] { "1" });
            break;
        case R.id.query_data_btn:
            db = dbHelper.getWritableDatabase();
            Cursor cursor = db.rawQuery("select * from book where id < ?",
                    new String[] { "100" });
            int idIndex = 0;
            int authorIndex = 0;
            int priceIndex = 0;
            int pagesIndex = 0;
            int nameIndex = 0;
            int categoryIdIndex = 0;

            ArrayList<Book> bookQueryList = new ArrayList<Book>();

            // 获取每个字段的ColumnIndex
            if (cursor.getCount() >= 0) {
                idIndex = cursor.getColumnIndex("id");
                authorIndex = cursor.getColumnIndex("author");
                priceIndex = cursor.getColumnIndex("price");
                pagesIndex = cursor.getColumnIndex("pages");
                nameIndex = cursor.getColumnIndex("name");
                categoryIdIndex = cursor.getColumnIndex("category_id");
            }
            while (cursor.moveToNext()) {
                Book book = new Book();
                book.setId(cursor.getInt(idIndex));
                book.setAuthor(cursor.getString(authorIndex));
                book.setPrice(cursor.getDouble(priceIndex));
                book.setPages(cursor.getInt(pagesIndex));
                book.setName(cursor.getString(nameIndex));
                book.setCategoryId(cursor.getInt(categoryIdIndex));

                bookQueryList.add(book);
            }

            queryResultTv.setText(bookQueryList.toString());
            break;
        default:
            break;
        }
    }
}

// Book类
class Book {
    private int id;
    private String author;
    private double price;
    private int pages;
    private String name;
    private int categoryId;

    public int getCategoryId() {
        return categoryId;
    }

    public void setCategoryId(int categoryId) {
        this.categoryId = categoryId;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getAuthor() {
        return author;
    }

    public void setAuthor(String author) {
        this.author = author;
    }

    public double getPrice() {
        return price;
    }

    public void setPrice(double price) {
        this.price = price;
    }

    public int getPages() {
        return pages;
    }

    public void setPages(int pages) {
        this.pages = pages;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    @Override
    public String toString() {
        return "Book [ id = " + id + ", author = " + author + ", price = "
                + price + ", pages = " + pages + ", name = " + name
                + ", category_id = " + categoryId + " ]";
    }
}
```
* 程序运行效果：
![](http://upload-images.jianshu.io/upload_images/8819542-bbd700f1aef3afcc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

* 使用事务
```java
// 删除旧数据并添加新数据，两个操作为一个原子操作
            SQLiteDatabase db = dbHelper.getWritableDatabase();
            db.beginTransaction(); // 开启事务
            try {
                db.delete("book", null, null);
                // if (true) {
                // // 在这里手动抛出一个异常，让事务失败
                // throw new NullPointerException();
                // }
                ContentValues values = new ContentValues();
                values.put("name", "这是本新书");
                values.put("author", "贾永基");
                values.put("pages", 123);
                values.put("price", 13.4);
                db.insert("book", null, values);
                db.setTransactionSuccessful();// 事务已经执行成功

            } catch (Exception e) {
                e.printStackTrace();
            } finally {
                db.endTransaction(); // 结束事务
            }
```
* 补充：使用`SQLiteDataBase`类自带的方法进行数据库的增、删、改操作（因为使用自带的方法进行查询的操作过于复杂不做介绍，直接使用SQL语句即可）：
比如插入数据：
```java
...
SQLiteDatabase db = dbHelper.getWritableDatabase();

// 使用ContentValues对象组装数据
ContentValues values = new ContentValues();
values.put("name","三体");
values.put("pages",565);
values.put("price",23.99);

// 插入数据到数据库中
// 第一个参数：表名；第二个参数：用于在未指定添加数据的情况下为某些可为空的字段自动赋值为NULL，一般用不到这个功能，把这个参数传入null即可；第三个参数：携带数据的ContentValues对象
db.insert("Book",null,values);
...
```
