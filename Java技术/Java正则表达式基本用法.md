# 两个关键类
* `Pattern`：正则表达式编译后在内存中的表示形式。是不可变类，可供多个线程并发使用；
* `Matcher`：保存执行匹配所涉及的各种状态，多个Matcher对象可以共享一个Pattern对象。

# 简单用法程序示例
```java
System.out.println(Pattern.matches("a\\wb", "a_b")); // 输出：true
Pattern p = Pattern.compile("a*b");
Matcher m = p.matcher("aabzaaadaaafbc");
System.out.println(m.matches()); // 输出：false
```

# Matcher类的常用方法
![](http://upload-images.jianshu.io/upload_images/8819542-b62ad2c9ea8205fe.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

# 程序举例
```java
public static void test1() {
        System.out.println(Pattern.matches("a\\wb", "a_b")); // 输出：true

        Pattern p = Pattern.compile("a*b");
        Matcher m = p.matcher("aabzaaadaaafbc");

        System.out.println(m.matches()); // 输出：false
        System.out.println(m.find()); // 输出：true
        System.out.println(m.group()); // 输出：b
        System.out.println(m.start()); // 输出：2
        System.out.println(m.end()); // 输出：3
        System.out.println(m.lookingAt()); // 输出：true
        m.reset("zab");
        System.out.println(m.lookingAt()); // 输出：false
    }

    public static void test2() {
        Matcher m = Pattern.compile("\\w+").matcher("Java is very easy!");

        while (m.find()) {
            System.out.println(m.group() + "子串的起始位置：" + m.start() + ",结束位置："
                    + m.end());
        }

        int i = 0;
        while (m.find(i)) {
            System.out.print(m.group() + "\t");
            i++;
        }

        // 输出：
        // Java子串的起始位置：0,结束位置：4
        // is子串的起始位置：5,结束位置：7
        // very子串的起始位置：8,结束位置：12
        // easy子串的起始位置：13,结束位置：17
        // Java ava va a is is s very very ery ry y easy easy asy sy y
    }

    public static void test3() {
        String[] mails = { "Jiayongji@163.com", "Jiayongji@gmail.com",
                "jy@hust.org", "wawa@abc.cc" };
        String mailRegEx = "\\w{3,20}@\\w+\\.(com|cn|edu|org|net|gov)";
        Pattern mailPattern = Pattern.compile(mailRegEx);

        Matcher mailMatcher = null;

        for (String mail : mails) {
            if (mailMatcher == null) {
                mailMatcher = mailPattern.matcher(mail);
            } else {
                mailMatcher.reset(mail);
            }

            System.out.println(mail + (mailMatcher.matches() ? "是" : "不是")
                    + "一个合法的邮箱地址");
        }

        // 输出：
        // Jiayongji@163.com是一个合法的邮箱地址
        // Jiayongji@gmail.com是一个合法的邮箱地址
        // jy@hust.org不是一个合法的邮箱地址
        // wawa@abc.cc不是一个合法的邮箱地址

    }

    public static void test4() {
        Matcher m = Pattern.compile("\\bre\\w*").matcher(
                "Java is real good at inrestart and regex.");
        System.out.println(m.replaceAll("哈哈"));

        // 输出：
        // Java is 哈哈 good at inrestart and 哈哈.

    }
```
