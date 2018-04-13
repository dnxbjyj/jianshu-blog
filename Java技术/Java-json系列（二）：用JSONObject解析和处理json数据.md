本文中主要介绍JSONObject处理json数据时候的一些常用场景和方法。

# （一）jar包下载

所需jar包打包下载百度网盘地址：[JSONObject所必须的6个包.rar](https://pan.baidu.com/s/1c27Uyre)

#（二）常见场景及处理方法

### 1、解析简单的json字符串：
```java
// 简单的json测试字符串
public static final String JSON_SIMPLE = "{'name':'tom','age':16}";

JSONObject obj = JSONObject.fromObject(JSON_SIMPLE);
System.out.println("name is : " + obj.get("name"));
System.out.println("age is : " + obj.get("age"));
```
输出：
```
name is : tom
age is : 16
```

###  2、解析嵌套的json字符串：
```java
        // 嵌套的json字符串
        public static final String JSON_MULTI = "{'name':'tom','score':{'Math':98,'English':90}}";
        JSONObject obj = JSONObject.fromObject(JSON_MULTI);
        System.out.println("name is : " + obj.get("name"));
        System.out.println("score is : " + obj.get("score"));

        JSONObject scoreObj = (JSONObject) obj.get("score");
        System.out.println("Math score is : " + scoreObj.get("Math"));
        System.out.println("English score is : " + scoreObj.get("English"));
```
输出：
```
name is : tom
score is : {"English":90,"Math":98}
Math score is : 98
English score is : 90
```

### 3、把bean对象转化成JSONObject对象：

Person、Info、Score类分别如下：（注：要定义成独立的三个public类，不能定义成内部类或非public类，否则会转换异常）
```java
public class Person {
    private String name;

    private Info info;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Info getInfo() {
        return info;
    }

    public void setInfo(Info info) {
        this.info = info;
    }

    @Override
    public String toString() {
        return "Person [name=" + name + ", info=" + info + "]";
    }

}
```
```java
public class Info {
    private int age;
    private Score score;

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }

    public Score getScore() {
        return score;
    }

    public void setScore(Score score) {
        this.score = score;
    }

    @Override
    public String toString() {
        return "Info [age=" + age + ", score=" + score + "]";
    }

}
```
```java
public class Score {
    private String math;
    private String english;

    public String getMath() {
        return math;
    }

    public void setMath(String math) {
        this.math = math;
    }

    public String getEnglish() {
        return english;
    }

    public void setEnglish(String english) {
        this.english = english;
    }

    @Override
    public String toString() {
        return "Score [math=" + math + ", english=" + english + "]";
    }

}
```
转换方法：
```java
Score score = new Score();
        score.setEnglish("A");
        score.setMath("B");

        Info info = new Info();
        info.setAge(20);
        info.setScore(score);

        Person person = new Person();
        person.setInfo(info);
        person.setName("Tim");

        JSONObject obj = JSONObject.fromObject(person);
        System.out.println(obj.toString());
```

输出：
```json
 {
    "name": "Tim",
    "info": {
        "score": {
            "english": "A",
            "math": "B"
        },
        "age": 20
    }
}
```

### 4、把json数组转换成JsonObject数组：
```java
// 数组形式的json
        public static final String JSON_ARRAY = "[{'name':'tom'},{'name':'john','age':20},{}]";

        JSONArray arr = JSONArray.fromObject(JSON_ARRAY);
        System.out.println(arr);

        for (int i = 0; i < arr.size(); i++) {
            JSONObject obj = arr.getJSONObject(i);
            System.out.println(obj.toString());
        }
```
输出：
```json
[{"name":"tom"},{"name":"john","age":20},{}]
{"name":"tom"}
{"name":"john","age":20}
{}
```

5、构造一个json字符串：
```java
JSONObject obj = new JSONObject();
        obj.put("name", "tom");
        obj.put("age", 19);

        // 子对象
        JSONObject objContact = new JSONObject();
        objContact.put("tel", "123456");
        objContact.put("email", "tom@test.com");
        obj.put("contact", objContact);

        // 子数组对象
        JSONArray scoreArr = new JSONArray();
        JSONObject objEnglish = new JSONObject();
        objEnglish.put("course", "english");
        objEnglish.put("result", 100);
        objEnglish.put("level", "A");

        JSONObject objMath = new JSONObject();
        objMath.put("course", "math");
        objMath.put("result", 50);
        objMath.put("level", "D");

        scoreArr.add(objEnglish);
        scoreArr.add(objMath);

        obj.put("score", scoreArr);

        System.out.println(obj.toString());
```

输出：
```json
{
    "score": [
        {
            "result": 100,
            "level": "A",
            "course": "english"
        },
        {
            "result": 50,
            "level": "D",
            "course": "math"
        }
    ],
    "contact": {
        "tel": "123456",
        "email": "[tom@test.com](mailto:tom@test.com)"
    },
    "name": "tom",
    "age": 19
}
```
思考：输出的json中的字段的顺序有没有办法设置？
