　　GSON是谷歌提供的开源库，用来解析Json格式的数据，非常好用。如果要使用GSON的话，则要先下载`gson-2.2.4.jar`这个文件，如果是在Android项目中使用，则在Android项目的libs目录下添加这个文件即可；如果是在Java项目中，则把gson-2.2.4.jar先添加到当前项目的任意一个包中，然后右键点击这个jar包 -> 构建路径 -> 添加至构建路径。这样准备工作就做好了。

# （一）单条无嵌套Json数据的解析

比如有如下Json数据：`{"name":"John", "age":20}`
注：也可以用单引号，写成：`{'name':'John', 'age':20}`

解析该数据步骤如下：

* 1、定义Person类：
```java
public class Person{

　　　　private String name;  //属性都定义成String类型，并且属性名要和Json数据中的键值对的键名完全一样

　　　　private String age;

　　　　...//提供所有属性的getter和setter方法

}
```
* 2、创建GSON对象并解析：
```java
String jsonData = "{\"name\":\"John\", \"age\":20}";　　//注：这里也可以不使用转义字符，而用单引号：String jsonData = "{'name':'John', 'age':20}";
Gson gson = new Gson();
Person person = gson.fromJson(jsonData,Person.class);
```
* 3、然后使用Person对象的getter方法就可以获取到数据了。 

* 4、扩展：考虑到Json数据的不同，那么解析Json的时候所用的类也可能不同，比如这里用的是Person，如果解析其他数据可能用的又是Dog、Cat...所以考虑将用GSON解析的步骤封装，并提供泛型参数，示例程序如下：
```java
import com.google.gson.Gson;

/**
 * 用GSON解析单条Json数据
 *
 */
public class GsonTest1 {
    public static void main(String[] args) {
        String jsonData = "{'name':'John', 'age':20}";
        Person person = GsonUtil.parseJsonWithGson(jsonData, Person.class);
        System.out.println(person.getName() + "," + person.getAge());
    }
}

/*
 * 封装的GSON解析工具类，提供泛型参数
 */
class GsonUtil {
    //将Json数据解析成相应的映射对象
    public static <T> T parseJsonWithGson(String jsonData, Class<T> type) {
        Gson gson = new Gson();
        T result = gson.fromJson(jsonData, type);
        return result;
    }

}

class Person {
    private String name;
    private String age;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getAge() {
        return age;
    }

    public void setAge(String age) {
        this.age = age;
    }

}
```
以上代码输出结果：
```
John,20
```

# （二）单条有嵌套的Json数据解析

比如有如下Json数据：`{"name":"John", "age":20,"grade":{"course":"English","score":100,"level":"A"}}`

对这样的数据就要用内部类的来解决了。解析步骤如下：

* 1、定义Student类：
```java
class Student {
    private String name;
    private String age;

    private Grade grade;

    public class Grade { // 内部类要定义成public的
        private String course;
        private String score;
        private String level;

        public String getCourse() {
            return course;
        }

        public void setCourse(String course) {
            this.course = course;
        }

        public String getScore() {
            return score;
        }

        public void setScore(String score) {
            this.score = score;
        }

        public String getLevel() {
            return level;
        }

        public void setLevel(String level) {
            this.level = level;
        }

        // 重写toString方法
        @Override
        public String toString() {
            return "Grade:[course = " + course + ", score = " + score
                    + ", level = " + level + "]";
        }
    }

    // 重写toString方法
    @Override
    public String toString() {
        return "Student:[name = " + name + ", age = " + age + ", grade = "
                + grade + "]";
    }
}
```
* 2、使用（一）中封装的GsonUtil工具类进行解析：
```java
public class GsonTest1 {
    public static void main(String[] args) {
        String jsonData = "{'name':'John', 'age':20,'grade':{'course':'English','score':100,'level':'A'}}";
        Student student = GsonUtil.parseJsonWithGson(jsonData, Student.class);
        System.out.println(student);
    }
}

/*
 * 封装的GSON解析工具类，提供泛型参数
 */
class GsonUtil {
    // 将Json数据解析成相应的映射对象
    public static <T> T parseJsonWithGson(String jsonData, Class<T> type) {
        Gson gson = new Gson();
        T result = gson.fromJson(jsonData, type);
        return result;
    }

}
```
以上代码输出结果：
```
Student:[name = John, age = 20, grade = Grade:[course = English, score = 100, level = A]]
```

# （三）解析Json数组（多条Json数据）

比如有如下Json数据：
```
[{'name':'John', 'grade':[{'course':'English','score':100},{'course':'Math','score':78}]}, {'name':'Tom', 'grade':[{'course':'English','score':86},{'course':'Math','score':90}]}] 
```  
注：Json数组最外层一定要加`[]`

如何处理这样的数据呢？就要用到List。步骤如下：

示例程序如下：
```java
import java.lang.reflect.Type;
import java.util.List;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

/**
 * 用GSON解析Json数组
 */
public class GsonTest {
    public static void main(String[] args) {
        // Json数组最外层要加"[]"
        String jsonData = "[{'name':'John', 'grade':[{'course':'English','score':100},{'course':'Math','score':78}]},{'name':'Tom', 'grade':[{'course':'English','score':86},{'course':'Math','score':90}]}]";

        List<Student> students = GsonUtil.parseJsonArrayWithGson(jsonData,
                Student.class);
        System.out.println(students);
    }
}

/*
 * 封装的GSON解析工具类，提供泛型参数
 */
class GsonUtil {
    // 将Json数据解析成相应的映射对象
    public static <T> T parseJsonWithGson(String jsonData, Class<T> type) {
        Gson gson = new Gson();
        T result = gson.fromJson(jsonData, type);
        return result;
    }

    // 将Json数组解析成相应的映射对象列表
    public static <T> List<T> parseJsonArrayWithGson(String jsonData,
            Class<T> type) {
        Gson gson = new Gson();
        List<T> result = gson.fromJson(jsonData, new TypeToken<List<T>>() {
        }.getType());
        return result;
    }
}

class Student {
    private String name;
    private List<Grade> grade; // 因为grade是个数组，所以要定义成List

    public class Grade {
        private String course;
        private String score;

        public String getCourse() {
            return course;
        }

        public void setCourse(String course) {
            this.course = course;
        }

        public String getScore() {
            return score;
        }

        public void setScore(String score) {
            this.score = score;
        }

    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public List<Grade> getGrade() {
        return grade;
    }

    public void setGrade(List<Grade> grade) {
        this.grade = grade;
    }
}
```
以上代码输出结果：
```
[{name=John, grade=[{course=English, score=100.0}, {course=Math, score=78.0}]}, {name=Tom, grade=[{course=English, score=86.0}, {course=Math, score=90.0}]}]
```
 
