> 参考：http://blog.csdn.net/jason0539/article/details/45055233

# （一）观察者模式简介

### 1、定义
对象间一种一对多的依赖关系，一个对象状态发生改变时，所有依赖它的对象都会接到通知并作出相应的响应。

### 2、应用场景
* GUI系统
* 订阅-发布系统
* 事件多级触发场景
* 当一个对象改变时需要通知其他对象，但不知道有其他对象具体有哪些时

### 3、UML类图

![](http://upload-images.jianshu.io/upload_images/8819542-f7ed35a9fdf91f98.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

# （二）观察者模式实例

### 背景介绍
假设有个珠宝公司要运送一批钻石，强盗也盯上这批钻石了，准备在运输途中抢劫，而珠宝公司雇佣的保镖要全程对钻石进行保护，警察也派出警车护航，关系如下图：

![](http://upload-images.jianshu.io/upload_images/8819542-e8da3573c6d5d1ab.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 代码如下：
* 抽象观察者接口：
```java
/**
 * 抽象观察者
 *
 */

public interface Watcher {
    // 对被观察者状态变化做出响应的抽象方法
    public void update(String msg);
}
```

* 抽象被观察者接口：
```java
/**
 * 抽象被观察者
 *
 */

public interface Watched {
    // 添加观察者
    public void addWatcher(Watcher watcher);

    // 移除观察者
    public void removeWatcher(Watcher watcher);

    // 通知观察者
    public void notifyWatchers(String msg);
}
```

* 保镖类：
```java
/**
 * 保镖类，实现Watcher接口
 *
 */

public class Security implements Watcher {

    @Override
    public void update(String msg) {
        System.out.println("保镖收到消息：" + msg + "。保镖开始保护！");
    }

}
```

* 警察类：
```java
/**
 * 警察类，实现Watcher接口
 *
 */

public class Police implements Watcher {

    @Override
    public void update(String msg) {
        System.out.println("警察收到消息：" + msg + "。警察开始派警车护航！");
    }

}
```

* 强盗类：
```java
/**
 * 强盗类，实现Watcher接口
 *
 */

public class Thief implements Watcher {

    @Override
    public void update(String msg) {
        System.out.println("收到消息：" + msg + "。强盗准备动手！");
    }

}
```

* 珠宝运输类：
```java
/**
 * 具体的被观察者
 *
 */

public class Transporter implements Watched {

    List<Watcher> wathcerList = new ArrayList<Watcher>();

    @Override
    public void addWatcher(Watcher watcher) {
        wathcerList.add(watcher);
    }

    @Override
    public void removeWatcher(Watcher watcher) {
        wathcerList.remove(watcher);
    }

    @Override
    public void notifyWatchers(String msg) {
        for (Watcher w : wathcerList) {
            w.update(msg);
        }
    }

}
```

* 测试类：
```java
public class Test {
    public static void main(String[] args) {
        Security s = new Security();
        Thief t = new Thief();
        Police p = new Police();

        Transporter transPorter = new Transporter();
        transPorter.addWatcher(s);
        transPorter.addWatcher(t);
        transPorter.addWatcher(p);

        transPorter.notifyWatchers("运输车队开始出发了");

        transPorter.removeWatcher(t);
        transPorter.notifyWatchers("运输车队摆脱了强盗");
    }
}
```

* 输出结果：
```
保镖收到消息：运输车队开始出发了。保镖开始保护！
收到消息：运输车队开始出发了。强盗准备动手！
警察收到消息：运输车队开始出发了。警察开始派警车护航！
保镖收到消息：运输车队摆脱了强盗。保镖开始保护！
警察收到消息：运输车队摆脱了强盗。警察开始派警车护航！
```

