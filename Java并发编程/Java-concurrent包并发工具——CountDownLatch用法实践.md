> 参考：http://blog.csdn.net/qq_30739519/article/details/51350527

很多系统在启动运行之前都会有一个称为"健康检查"的阶段，比如会去检查数据库、网络、虚拟机等基础组件服务的状态是否正常，当确认这些服务都正常之后，才会继续做其他的启动工作（否则地基不牢，后面的事情做了也是白搭）。这种场景简而言之就是，后面的任务对于前面的一个或多个任务有前后依赖关系，只有当前面的任务完成了，后面的任务才能开始，而这样的场景正好可以由`CountDownLatch`这样一个并发辅助工具来完成。

`CountDownLatch`，按字面意思理解，就是：`计数闩（shuan）`，这个`闩`就是`门闩`的意思，可以理解为一个开关，通过一个计数开关来控制并发任务的执行。该类位于`java.util.concurrent.CountDownLatch`，从JDK 1.5版本引入。

本文就以一个简单的健康检查场景为例子，来理一理`CountDownLatch`这样一个并发工具的用法。

# 场景简要描述
假设有一个系统，在系统启动之前需要先检查数据库、网络、虚拟机三个组件服务是否正常，如果都正常，才继续启动；否则启动失败。

可以用一个图示来表示：
![](https://upload-images.jianshu.io/upload_images/8819542-a989cfa29d25a8a8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


# 创建一个健康检查任务基类
每个健康检查任务都是跑在子线程中的，所以要实现Runnable接口：
```java
package com.countdownlatch;

import java.util.concurrent.CountDownLatch;

/**
 * 系统健康检查任务基类
 * 
 * @author Administrator
 *
 */
public abstract class BaseHealthCheckTask implements Runnable {

	// 同步计数闩对象
	private CountDownLatch latch;

	// 要进行健康检查的服务名称
	protected String serviceName;

	// 健康检查是否完成
	protected boolean checkOk;

	public BaseHealthCheckTask(CountDownLatch latch, String serviceName) {
		this.latch = latch;
		this.serviceName = serviceName;
		// checkOk初始化为false，等正常完成健康检查操作之后赋值true
		this.checkOk = false;
	}

	public String getServiceName() {
		return serviceName;
	}

	public boolean isCheckOk() {
		return checkOk;
	}

	@Override
	public void run() {
		try {
			// 执行具体的健康检查工作
			doCheck();
			// 检查成功，给检查成功标志对象赋值true
			this.checkOk = true;
		} catch (Exception e) {
			// 如果执行健康检查任务过程中发生异常，不再给checkOk赋值true，表示健康检查失败
			e.printStackTrace();
		}

		// 健康检查完成之后（不管成功还是失败），将同步计数闩的计数值减1
		this.latch.countDown();
	}

	/**
	 * 需要由子类实现的抽象方法，用于做具体的健康检查工作
	 */
	protected abstract void doCheck() throws Exception;
}

```

# 创建不同服务的健康检查任务子类
* DBHealthCheckTask
假设数据库健康检查任务需要耗时3秒完成：
```java
package com.countdownlatch;

import java.util.concurrent.CountDownLatch;

/**
 * 数据库服务健康检查任务类
 * 
 * @author Administrator
 *
 */
public class DBHealthCheckTask extends BaseHealthCheckTask {

	public DBHealthCheckTask(CountDownLatch latch) {
		super(latch, "DBService");
	}

	@Override
	public void doCheck() throws InterruptedException {
		System.out
				.println("start to check: " + this.serviceName + " health...");
		// sleep 3秒，模拟执行数据库健康检查任务
		Thread.sleep(3000);
		System.out.println("finish to check: " + this.serviceName + " health!");
	}

}

```

* NetworkHealthCheckTask
假设网络健康检查任务需要耗时5秒完成：
```java
package com.countdownlatch;

import java.util.concurrent.CountDownLatch;

/**
 * 网络服务健康检查任务类
 * 
 * @author Administrator
 *
 */
public class NetworkHealthCheckTask extends BaseHealthCheckTask {

	public NetworkHealthCheckTask(CountDownLatch latch) {
		super(latch, "NetworkService");
	}

	@Override
	public void doCheck() throws InterruptedException {
		System.out
				.println("start to check: " + this.serviceName + " health...");
		// sleep 5秒，模拟执行网络健康检查任务
		Thread.sleep(5000);
		System.out.println("finish to check: " + this.serviceName + " health!");
	}

}

```

* VmHealthCheckTask
假设虚拟机健康检查任务需要耗时4秒完成：
```java
package com.countdownlatch;

import java.util.concurrent.CountDownLatch;

/**
 * 虚拟机服务健康检查任务类
 * 
 * @author Administrator
 *
 */
public class VmHealthCheckTask extends BaseHealthCheckTask {

	public VmHealthCheckTask(CountDownLatch latch) {
		super(latch, "VmService");
	}

	@Override
	public void doCheck() throws InterruptedException {
		System.out
				.println("start to check: " + this.serviceName + " health...");
		// sleep 4秒，模拟执行虚拟机健康检查任务
		Thread.sleep(4000);
		System.out.println("finish to check: " + this.serviceName + " health!");
	}

}

```

# 创建一个系统启动器类
用单例模式创建一个系统启动器，在启动器主线程中，先启动并等待3个健康检查任务的完成，才能接着进行其他启动工作。如果有健康检查任务的检查结果是失败的，那么终止启动主线程。
```java
package com.countdownlatch;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.Executor;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

/**
 * 系统启动器
 * 
 * @author Administrator
 *
 */
public class SystemStarter {
	// 单例化，因为系统启动器对象全局只能有一个
	private static SystemStarter INSTANCE = new SystemStarter();

	// 同步计数闩对象
	private CountDownLatch latch;

	// 设置默认的同步计数闩所允许的线程数为3
	private static final int LATCH_COUNT = 3;

	// 默认的超时等待描述
	private static final int DEFAULT_LATCH_TIMEOUT_SECOND = 60;

	private SystemStarter() {
		// 初始化启动器的同步闩对象
		this.latch = new CountDownLatch(LATCH_COUNT);
	}

	public static SystemStarter getInstance() {
		return INSTANCE;
	}

	public void startUp() throws InterruptedException {
		// 用于函数计时
		long start = System.currentTimeMillis();

		// 执行器对象，用于执行3个健康检查线程任务
		Executor executor = Executors.newFixedThreadPool(LATCH_COUNT);
		List<BaseHealthCheckTask> tasks = new ArrayList<BaseHealthCheckTask>();
		// 使用同步计数闩对象初始化3个健康检查任务对象：数据库、网络和虚拟机健康检查
		tasks.add(new DBHealthCheckTask(this.latch));
		tasks.add(new NetworkHealthCheckTask(this.latch));
		tasks.add(new VmHealthCheckTask(this.latch));

		// 并发执行健康检查任务
		for (BaseHealthCheckTask task : tasks) {
			executor.execute(task);
		}

		// 同步计数闩阻塞主线程进行等待，直到上面的3个健康检查任务全部执行完成，或超过默认超时时间才继续往下执行主线程
		this.latch.await(DEFAULT_LATCH_TIMEOUT_SECOND, TimeUnit.SECONDS);

		System.out.println("check system health FINISH!");

		// 输出每个健康检查任务的检查结果（是否检查通过）
		for (BaseHealthCheckTask task : tasks) {
			System.out.println("health check result (is passed): "
					+ task.getServiceName() + " - " + task.isCheckOk());
			// 一旦有一个任务失败，显示系统启动失败，退出启动器
			if (!task.isCheckOk()) {
				System.out.println("start up the system FAILED! "
						+ task.getServiceName() + " is NOT OK!");
				return;
			}
		}

		System.out.println("-----");

		// 在全部健康检查完成后，才开始执行启动过程中的其他任务
		doOtherStartupWork();

		System.out.println("-----");

		long end = System.currentTimeMillis();
		System.out.println("start up the system FINISH! totally spent "
				+ (end - start) + "ms.");
	}

	/**
	 * 其他任务，依赖于所有健康检查完成之后，才能执行这些任务
	 * 
	 * @throws InterruptedException
	 */
	private void doOtherStartupWork() throws InterruptedException {
		System.out.println("do some other works...");
		Thread.sleep(1500);
	}
}

```

# 在main方法中调用启动器启动系统
```java
package com.countdownlatch;

public class Main {
	public static void main(String[] args) throws InterruptedException {
		SystemStarter startup = SystemStarter.getInstance();
		startup.startUp();
	}
}

```
执行结果：
```
start to check: DBService health...
start to check: VmService health...
start to check: NetworkService health...
finish to check: DBService health!
finish to check: VmService health!
finish to check: NetworkService health!
check system health FINISH!
health check result (is passed): DBService - true
health check result (is passed): NetworkService - true
health check result (is passed): VmService - true
-----
do some other works...
-----
start up the system FINISH! totally spent 6520ms.
```
可见启动器最终耗时为3个健康检查任务中最长耗时的任务的耗时（网络健康检查的5秒）+做其他启动工作的耗时（1.5秒），即6.5秒。

# 附：CountDownLatch类方法梳理
`CountDownLatch`类位于`java.util.concurrent.CountDownLatch`，是JDK并发工具包`concurrent`中的一个辅助工具类。

* 查看`CountDownLatch`类的源码，可以看到有1个成员变量`sync`、1个带参构造方法和5个方法。
![](https://upload-images.jianshu.io/upload_images/8819542-d550233572cf5493.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

* 该类的核心功能由一个`Sync`类型的成员变量`sync`实现，`Sync`是一个静态内部类，继承自`AbstractQueuedSynchronizer`类。

* `await()`方法会让调用该方法的当前线程阻塞等待，直到latch的计数值变为0，或者有线程抛出中断异常。下面是方法的文档说明：
```
Causes the current thread to wait until the latch has counted down to zero, unless the thread is {@linkplain Thread#interrupt interrupted}.
```

* `await(long timeout, TimeUnit unit)`方法是和`await()`方法类似的一个方法，只不过可以设置一个阻塞等待的超时时间，当超过该超时时间后，会结束阻塞等待（不管子线程有没有执行完），接着往下执行。下面是方法的文档说明：
```
Causes the current thread to wait until the latch has counted down to zero, unless the thread is {@linkplain Thread#interrupt interrupted}, or the specified waiting time elapses.
```

* `countDown()`方法由子线程调用，会对latch的计数值减1，直到减到0为止。下面是方法的文档说明：
```
Decrements the count of the latch, releasing all waiting threads if the count reaches zero.
```

* `getCount()`方法用于获取当前latch的计数值，下面是方法的文档说明：
```
Returns the current count.
This method is typically used for debugging and testing purposes.
```

* `toString()`方法会打印出当前latch的计数值：
```
Returns a string identifying this latch, as well as its state.
The state, in brackets, includes the String {@code "Count ="}
followed by the current count.
```

* 最后看一看该类的作者：
![](https://upload-images.jianshu.io/upload_images/8819542-b55fb0492e761ba5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

Doug Lea正是`java.util.concurrent`包的作者，是一位对Java影响力深远的人，可以看一看百度百科的介绍：[Doug Lea](https://baike.baidu.com/item/Doug%20Lea/6319404?fr=aladdin)

# 本文源码地址
[我的GitHub](https://github.com/dnxbjyj/java-projects/tree/master/concurrent/com.concurrent.test/src/com/countdownlatch)
