在项目开发的时候，复杂业务场景中经常用到并发编程。有时候需要获取并发执行结果，或者捕获多线程中的异常，这个时候用Runnable任务就不行了，而需要用到Callable。本文通过一个简单的实例来探讨一下Callable结合Executor框架的用法。

# 需求
假设系统中有一个模块，需要从另一个模块调用REST API接口查询用户（Person）的信息（通过用户ID查询），根据业务需要，会遇到一次性查询成千上万个用户信息的场景，需要进行并发查询，并获取查询结果。

# 准备工作
* Person model数据类结构
为了简单起见，假设用户信息类只有两个字段：`id`和`name`，都为String类型。
```java
package com.executor.model;

/**
 * 用户信息数据类
 * @author Administrator
 *
 */
public class Person {
	private String id;
	private String name;
	
	public Person(){
		
	}
	
	public Person(String id, String name) {
		this.id = id;
		this.name = name;
	}
	public String getId() {
		return id;
	}
	public void setId(String id) {
		this.id = id;
	}
	public String getName() {
		return name;
	}
	public void setName(String name) {
		this.name = name;
	}

	@Override
	public String toString() {
		return "Person [id=" + id + ", name=" + name + "]";
	}
}

```

* 查询用户信息的REST API接口封装的工具类PersonRestAPIUtil
queryPersonFromAPI方法模拟调用REST接口查询用户信息，每次查询需要耗时300毫秒。
```java
package com.executor.util;

import com.executor.model.Person;

/**
 * RestAPI工具类
 * 
 * @author Administrator
 *
 */
public class PersonRestAPIUtil {
	/**
	 * 模拟调Rest API查询用户信息
	 * 
	 * @param id
	 * @return
	 */
	public static Person queryPersonFromAPI(String id) {
		Person p = new Person();
		
		// 模拟调接口耗时，300毫秒
		try {
			Thread.sleep(300);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		
		// 模拟查询到的用户信息，并返回
		p.setId(id);
		p.setName("person#" + id);
		return p;
	}
}

```

# 总体步骤梳理
主要是四步曲：
* 创建Callable任务类
* 构建Callable任务列表
* 用Executor线程池并发执行多个任务
* 获取任务执行结果

# 创建Callable任务类
在执行并发任务之前，需要通过创建一个实现Callable接口的任务类来定义每个任务具体的执行业务逻辑。对于本文的需求，名为`QueryPersonTask`的任务类来查询单个用户的信息，`QueryPersonTask`类继承自`Callable<Person>`。
```java
package com.executor.task;

import java.util.concurrent.Callable;

import com.executor.model.Person;
import com.executor.util.PersonRestAPIUtil;

/**
 * 查询单个用户信息任务类
 * 
 * @author Administrator
 *
 */
public class QueryPersonTask implements Callable<Person> {

	private String id;

	public QueryPersonTask(String id) {
		this.id = id;
	}

	/**
	 * call方法是任务执行的主体，
	 */
	@Override
	public Person call() throws Exception {
		return PersonRestAPIUtil.queryPersonFromAPI(this.id);
	}

}

```

# 构建Callable任务列表
假设有一批用户的ID是知道的，存在一个名为`ids`的`List<String>`列表中，下面构建查询这多个用户信息的Callable任务列表：
```java
// 构建查询多个用户信息的Callable任务列表
		List<Callable<Person>> tasks = new ArrayList<Callable<Person>>();
		for (String id : ids) {
			QueryPersonTask task = new QueryPersonTask(id);
			tasks.add(task);
		}
```


# 用Executor线程池并发执行多个任务
上一步已经构建好了任务列表，下面在线程池中并发执行这些任务。
* 创建线程池
```java
ThreadPoolExecutor executor = (ThreadPoolExecutor) Executors
				.newFixedThreadPool(100);
```

* 执行任务
```java
		List<Future<Person>> futureResults = new ArrayList<Future<Person>>();
		try {
			futureResults = executor.invokeAll(tasks);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
```
可以看到任务执行结果存储在了一个`List<Future<Person>>`类型的`futureResults`对象中。

# 获取任务执行结果
```java
		// 从futureResults中获取并解析出Person列表
		List<Person> persons = new ArrayList<Person>();
		for (Future<Person> ret : futureResults) {
			Person p;
			try {
				p = ret.get(); // get()方法会阻塞等到，直到获取到结果为止
				if (null != p) {
					persons.add(p);
				}
			} catch (InterruptedException e) {
				e.printStackTrace();
				throw new Exception("InterruptedException occurs.");
			} catch (ExecutionException e) {
				e.printStackTrace();
				throw new Exception("ExecutionException occurs.");
			}
		}
```
最终任务执行结果被解析为了`List<Person>`，这也就是我们最终想要的数据。

# 性能对比：并发与单线程
下面写一个`PersonBusiness`业务类，来测试一下单线程与并发的性能对比：
```java
package com.executor.business;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.ThreadPoolExecutor;

import com.executor.model.Person;
import com.executor.task.QueryPersonTask;
import com.executor.util.PersonRestAPIUtil;

public class PersonBusiness {
	public static void main(String[] args) throws Exception {
		// 构建20个用户的ID列表
		List<String> ids = new ArrayList<String>();
		for (int i = 1; i <= 20; i++) {
			ids.add(String.valueOf(i));
		}
		
		// 单线程查询
		singleThreadQueryPersons(ids);
		// 并发查询
		concurrentQueryPersons(ids);
	}

	/**
	 * 单线程查询多个用户信息
	 * 
	 * @param ids
	 * @return
	 */
	private static List<Person> singleThreadQueryPersons(List<String> ids) {
		// 计时开始
		long start = System.currentTimeMillis();

		List<Person> persons = new ArrayList<Person>();

		// 遍历每个用户ID，依次查询用户信息
		for (String id : ids) {
			Person p = PersonRestAPIUtil.queryPersonFromAPI(id);
			persons.add(p);
		}

		// 计时结束
		long end = System.currentTimeMillis();
		System.out.println("查询" + ids.size()
				+ "个用户，singleThreadQueryPersons方法共耗时：" + (end - start) + "毫秒");

		return persons;
	}

	private static List<Person> concurrentQueryPersons(List<String> ids)
			throws Exception {
		// 计时开始
		long start = System.currentTimeMillis();

		// 1. 构建查询多个用户信息的Callable任务列表
		List<Callable<Person>> tasks = new ArrayList<Callable<Person>>();
		for (String id : ids) {
			QueryPersonTask task = new QueryPersonTask(id);
			tasks.add(task);
		}

		// 2. 并发执行多个任务，并获取并发执行结果
		// 2.1 获取线程池
		ThreadPoolExecutor executor = (ThreadPoolExecutor) Executors
				.newFixedThreadPool(100);

		// 2.2 执行任务，并获取任务执行结果
		List<Future<Person>> futureResults = new ArrayList<Future<Person>>();
		try {
			futureResults = executor.invokeAll(tasks);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}

		// 2.3 从futureResults中获取并解析出Person列表
		List<Person> persons = new ArrayList<Person>();
		for (Future<Person> ret : futureResults) {
			Person p;
			try {
				p = ret.get(); // get()方法会阻塞等到，直到获取到结果为止
				if (null != p) {
					persons.add(p);
				}
			} catch (InterruptedException e) {
				e.printStackTrace();
				throw new Exception("InterruptedException occurs.");
			} catch (ExecutionException e) {
				e.printStackTrace();
				throw new Exception("ExecutionException occurs.");
			}
		}

		// 计时结束
		long end = System.currentTimeMillis();
		System.out.println("查询" + persons.size()
				+ "个用户，concurrentQueryPersons方法共耗时：" + (end - start) + "毫秒");
		return persons;
	}
}

```
运行上面代码，输出结果为：
```
查询20个用户，singleThreadQueryPersons方法共耗时：6011毫秒
查询20个用户，concurrentQueryPersons方法共耗时：301毫秒
```
可见并发执行效果明显，最终总耗时约等于查询单个用户的耗时。

# 优化
### 封装并发执行泛型工具类
可以看到在`PersonBusiness.concurrentQueryPersons`方法中，先构建了Callable任务列表，然后创建了线程池，然后执行任务，最后获取任务执行结果。这里是查询Person信息，那如果后面再遇到需求变动了，需要查询Dog、Cat等信息，难道再重复写一遍这些代码吗？

为了代码重用，把上述的执行并发任务和获取执行结果两步骤的代码封装成工具类，便于以后重用：
```java
package com.executor.util;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.ThreadPoolExecutor;

import com.executor.model.Person;

/**
 * Executor Framework并发任务处理类
 * 
 * @author Administrator
 *
 */
public class ExecutorUtil {

	/**
	 * 并发执行Callable任务方法，支持泛型参数
	 * 
	 * @param tasks
	 * @return
	 * @throws Exception
	 */
	public static <T> List<T> concurrentExecute(List<Callable<T>> tasks)
			throws Exception {
		// 1. 获取线程池
		ThreadPoolExecutor executor = (ThreadPoolExecutor) Executors
				.newFixedThreadPool(100);

		// 2. 并发执行任务，并获取返回结果
		List<Future<T>> futureResults = new ArrayList<Future<T>>();
		try {
			futureResults = executor.invokeAll(tasks);
		} catch (InterruptedException e) {
			e.printStackTrace();
			throw new Exception("InterruptedException occurs.");
		}

		// 3. 取回并解析返回结果
		List<T> results = getFromFutureResults(futureResults);

		return results;
	}

	/**
	 * 从并发Future结果中取回并解析结果，支持泛型参数
	 * 
	 * @param futureResults
	 * @return
	 * @throws Exception
	 */
	private static <T> List<T> getFromFutureResults(
			List<Future<T>> futureResults) throws Exception {

		List<T> results = new ArrayList<T>();
		for (Future<T> ret : futureResults) {
			try {
				T r = ret.get(); // get()方法会阻塞等到，直到获取到结果为止
				if (null != r) {
					results.add(r);
				}
			} catch (InterruptedException e) {
				e.printStackTrace();
				throw new Exception("InterruptedException occurs.");
			} catch (ExecutionException e) {
				e.printStackTrace();
				throw new Exception("ExecutionException occurs.");
			}
		}

		return results;
	}

}

```

### 线程池对象单例化
如果每次执行并发任务都创建一个线程池，将会造成资源浪费，那么可以考虑进一步优化，对`ExecutorUtil.concurrentExecute`方法中创建线程池封装成一个单例模式的类，比如叫`MyThreadPool`，不用每次调用都创建新的线程池。

# 总结
最终的代码结构：
![](https://upload-images.jianshu.io/upload_images/8819542-f222d0b2b954cad0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

可以看到Callable任务加上Executor线程池的调度，可以让我们轻松写出可以获取执行结果的并发代码，而且执行效率很高。此外，如果想要获取并发执行过程中的异常，可以通过改造Callable任务类的泛型为`Exception`，并在`call`方法中捕获并返回异常即可，这里不再赘述。

代码已经push到：[我的GitHub](https://github.com/dnxbjyj/java-projects/tree/master/concurrent/com.concurrent.test/src/com/executor)
