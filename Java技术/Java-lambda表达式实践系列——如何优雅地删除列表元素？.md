> 推荐阅读：[Java8 lambda表达式10个示例](http://www.importnew.com/16436.html)

在编程实践中，经常会遇到这样的需求场景：遍历一个列表，把其中不满足某些条件的元素删掉。

下面我们写几个方法来尝试用不同的方式来实现这个需求：
# 先准备两个校验方法
```java
	/**
	 * 校验一个字符串是否合法的方法，字符串的长度大于等于6才是合法的
	 * 
	 * @param str
	 * @return
	 */
	public static boolean isValid(String str) {
		if (null == str || str.length() < 6) {
			return false;
		}
		return true;
	}

	public static boolean isNotValid(String str) {
		return !isValid(str);
	}
```

# 方式1：在for-each循环中删除列表元素
```java
	public static void method1() {
		List<String> list = new ArrayList<String>();
		list.add("1");
		list.add("abc");
		list.add(null);
		list.add("123456");
		list.add("");

		for (String str : list) {
			if (isNotValid(str)) {
				list.remove(str);
			}
		}
		System.out.println(list);
		System.out.println(list.hashCode());
	}
```
运行上面这个方法，报异常：
```
java.util.ConcurrentModificationException
```
可见，并不能在for-each循环遍历一个列表时去删除这个列表的元素，此种方法行不通。

# 方式2：使用迭代器删除列表元素
```java
	public static void method2() {
		List<String> list = new ArrayList<String>();
		list.add("1");
		list.add("abc");
		list.add(null);
		list.add("123456");
		list.add("");
		System.out.println(list);
		System.out.println(list.hashCode());

		Iterator<String> it = list.iterator();
		while (it.hasNext()) {
			String str = it.next();
			if (isNotValid(str)) {
				it.remove();
			}
		}
		System.out.println(list);
		System.out.println(list.hashCode());
	}
```
运行这个方法，输出：
```
[1, abc, null, 123456, ] 
667562667 
[123456] 
1450575490
```
可见使用迭代器可以在遍历列表的同时正常地删除列表的元素，并且删除元素之后列表的内存地址已经发生了变化。

# 方式3：使用lambda表达式删除列表元素
上面使用迭代器的方式虽然能够正常地删除列表中的元素，但还是不够优雅，因为要写好几行的遍历代码，显得略臃肿。能不能只用一行代码完成这个功能呢？答案是可以的——使用lambda表达式：
```java
	public static void method3() {
		List<String> list = new ArrayList<String>();
		list.add("1");
		list.add("abc");
		list.add(null);
		list.add("123456");
		list.add("");
		System.out.println(list);
		System.out.println(list.hashCode());

		list.removeIf(e -> isNotValid(e));
		System.out.println(list);
		System.out.println(list.hashCode());
	}
```
运行上面的方法，输出：
```
[1, abc, null, 123456, ] 
667562667 
[123456] 
1450575490
```
可见使用lambda表达式的方法更为优雅，这里使用了`List`接口所继承的`Collection`接口在JDK 1.8新增的`removeIf`方法，该方法接收一个`Predicate`类型的参数，删除列表中满足`Predicate`条件的元素。在这里使用lambda表达式：`e -> isNotValid(e)`定义了这样一个`Predicate`函数。

# 方式4：使用方法引用删除列表元素
除了lambda表达式，JDK 1.8还可以用一种称为方法引用的方式来删除列表中的元素，使用类似C++的`::`运算符，来引用一个对象的实例方法或一个类的类方法，下面就用方法引用的方式来删除一个列表中的指定元素：
```java
	public static void method4() {
		List<String> list = new ArrayList<String>();
		list.add("1");
		list.add("abc");
		list.add(null);
		list.add("123456");
		list.add("");
		System.out.println(list);
		System.out.println(list.hashCode());

		list.removeIf(RemoveListElement::isNotValid);  // isNotValid为RemoveListElement类的一个静态方法
		System.out.println(list);
		System.out.println(list.hashCode());
	}
```
运行上面的方法，输出：
```java
[1, abc, null, 123456, ] 
667562667 
[123456] 
1450575490
```
可见使用方法引用的方式也可以达到同样的目的，但无疑比lambda表达式更为简洁、优雅。

# 总结
经过上述对比，可以看出：
* 在JDK 1.8之前，要使用迭代器的方式才能在遍历一个列表的时候正确地删除列表中的元素。
* 在JDK 1.8及之后，还可以使用lambda表达式和方法引用的方式正确地删除列表中的元素，这两种方式更为优雅。
