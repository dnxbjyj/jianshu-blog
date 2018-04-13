本文主要讲述python面向对象的一些基础语法。

# 创建对象及对象的属性

创建一个名为Person类，继承自object类（object类是所有类的祖先类），类体为空：


```python
class Person(object):
    pass
```

创建一个Person类的实例：


```python
p1 = Person()
```

为p1动态添加一个'name'属性：


```python
p1.name = 'Tom'
print p1.name
```

    Tom
    

为p1动态添加方法（其实方法也可以看成是对象实例的特殊属性）：


```python
import types
p1.get_name = types.MethodType(lambda self:self.name,p1,Person)
print p1.get_name()
```

    Tom
    

再创建另外一个Person对象：


```python
p2 = Person()
print p2.name
```


    ---------------------------------------------------------------------------

    AttributeError                            Traceback (most recent call last)

    <ipython-input-10-e3abcd8b0fdd> in <module>()
          1 p2 = Person()
    ----> 2 print p2.name
    

    AttributeError: 'Person' object has no attribute 'name'


可以看出为p1对象动态添加的'name'属性并不会影响到Person类的其他对象。

# 带可变参数的构造方法


```python
class Person(object):
    # 这里self为实例方法的第一个必须的参数，必须要有，且要放在第一个；第二个name为自定义必选参数，后面的kwargs是可选参数列表
    def __init__(self,name,**kwargs):
        self.name = name
        for k,v in kwargs.iteritems():
            # 设置实例属性值
            setattr(self,k,v)
```


```python
p = Person('Tom',age = 19,gender = 'male')
print p.name
print p.age
print p.gender
```

    Tom
    19
    male
    

# 实例属性（包括属性和方法）的可见性

python中实例的属性（包括属性和方法）是根据命名来进行可见性约束的，规则如下：

* `attr`  内外部都可见

* `__attr__`  预置属性，内外部都可见，但不建议普通属性这样命名

* `_attr`  内部可见、外部不可见（但只是倡议，并非强制约束）  

* `__attr`  内部可见、外部不可见（强制约束）

举例说明：


```python
class Person(object):
    attr1 = 1
    __attr2__ = 2
    _attr3 = 3
    __attr4 = 4
```


```python
p = Person()
```


```python
print p.attr1
```

    1
    


```python
print p.__attr2__
```

    2
    


```python
print p._attr3
```

    3
    


```python
print p.__attr4
```


    ---------------------------------------------------------------------------

    AttributeError                            Traceback (most recent call last)

    <ipython-input-20-47493f4f761b> in <module>()
    ----> 1 print p.__attr4
    

    AttributeError: 'Person' object has no attribute '__attr4'


# 类属性

写在类中，而非方法中的属性，其可见性规则和实例属性类似。

注：当实例修改了某个类属性之后，其实是创建了一个新的**同名的**实例属性，并不会让类属性值本身真正发生改变。而实例属性的访问优先级是高于类属性的。

# 类方法

类方法就是用`@classmethod`装饰器修饰的方法。`

# 类的继承

### object类

这是所有类的祖先类。一个自定义类如果不指定继承哪个类，那它默认继承object类，如：


```python
class Person:
    pass
p = Person()
print isinstance(p,Person)
print isinstance(p,object)
```

    True
    True
    

### 类的构造方法

```python
def __init__(self,arg1,arg2,...):
    ...
```

在子类的构造方法中要调用父类的构造方法进行初始化，才能获取到父类的实例属性（获取类属性不需要），调用方式：

```python
# SubClass：子类类名
super(SubClass,self).__init__(attr1,attr2,...)  #这里不用再写'self'参数了
```

举例：


```python
class Person(object):
    attr = 1
    def __init__(self,name,age):
        self.name = name
        self.age = age

class Student(Person):
    def __init__(self,name,age,score):
        super(Student,self).__init__(name,age)
        self.score = score
```


```python
s = Student('Tom',18,98)
```


```python
print s
```

    <__main__.Student object at 0x03A31D10>
    


```python
print s.age
print s.name
print s.score
print s.attr
```

    18
    Tom
    98
    1
    

> 小贴士：python作为动态语言，调用实例的方法时，并不会去检查类型的合法性，只要调的方法是实例有的并且参数正确，就可以调用。

> 例如：只要一个对象实例有名为'read'的方法，它就是一个file-like对象，就可以作为参数传入json.load()函数中。

### 类的多重继承


```python
class A:
    pass
class B(A):
    pass
class C(A):
    pass
class D(B,C):
    pass

d = D()
print isinstance(d,D)
print isinstance(d,B)
print isinstance(d,C)
print isinstance(d,A)
```

    True
    True
    True
    True
    

可以看出B、C类都继承了A类，而D类又同时继承了B、C类，所以D类的对象同时也是A、B、C三个类的实例。

# 获取对象的信息


```python
class Person(object):
    name = 'Tom'
p = Person()
```

### 判断对象是否是某个类/类型


```python
print isinstance(p,Person)
```

    True
    


```python
print isinstance([1,2,3],list)
```

    True
    

### 获取对象的类型


```python
print type(p)
```

    <class '__main__.Person'>
    

### 获取对象的所有属性（包括方法）


```python
print dir(p)
```

    ['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'name']
    

### 获取对象某个属性的值


```python
print getattr(p,'name')
```

    Tom
    

### 设置对象的属性值


```python
setattr(p,'age',19)
print p.age
```

    19
    

# 特殊方法（也叫做魔术方法）

* `__str__(self)`和`__repr__(self)`：用于print等显示函数，前者用于给用户看，后者给开发看。

* `__cmp__(self,s)`：用于`cmp()`、`sorted()`等和顺序有关的函数，其中s为另一个同类型的对象。

* `__len__(self)`：用于`len()`函数。

* `__add__(self,s)`、`__sub__(self,s)`、`__mul__(self,s)`、`__div__(self,s)`：用于对象的加减乘除四则运算。

* `__int__(self)`：用于`int()`函数。

* `__float__(self)`：用于`float()`函数。

* `__slots__(self)`：返回一个字符串列表或元组，限制类可以具有的属性。

* `__call__(self)`：让对象变成可调用的（用双括号`()`运算符调用）。

注：实现了`__call__(self)`方法的对象就变成了可以像函数那样调用的了，所以python的对象和函数的区分其实不明显。

举例：


```python
class Say(object):
    def __call__(self,a,b):
        print 'You say:{0} and {1}'.format(a,b)
        
s = Say()
s('hello','world')
```

    You say:hello and world
    

# 装饰器

* `@property`装饰器：装饰属性的getter方法。

* `@attr.setter`装饰器：装饰属性的setter方法。

举例：


```python
class Student(object):
    def __init__(self,name,score):
        self.name = name
        # 这里score定义成一个私有的属性
        self.__score = score
        
    # 相当于getter方法
    @property
    def score(self):
        return self.__score
    
    # 相当于setter方法
    @score.setter
    def score(self,score):
        if score > 100 or score < 0:
            raise ValueError('Invalid score!')
        self.__score = score
        
    # 定义一个新的grade属性
    @property
    def grade(self):
        if self.__score >= 80:
            return 'A'
        elif self.__score < 60:
            return 'C'
        else:
            return 'B'
        
s = Student('Tom',90)
print s.grade
s.score = 59
print s.grade
print s.score
```

    A
    C
    59
    


```python
s.score = -1
```


    ---------------------------------------------------------------------------

    ValueError                                Traceback (most recent call last)

    <ipython-input-10-7a8b6a159a64> in <module>()
    ----> 1 s.score = -1
    

    <ipython-input-9-9b3f1ca25afb> in score(self, score)
         14     def score(self,score):
         15         if score > 100 or score < 0:
    ---> 16             raise ValueError('Invalid score!')
         17         self.__score = score
         18 
    

    ValueError: Invalid score!



```python
s.grade = 'C'
```


    ---------------------------------------------------------------------------

    AttributeError                            Traceback (most recent call last)

    <ipython-input-11-de53788b008a> in <module>()
    ----> 1 s.grade = 'C'
    

    AttributeError: can't set attribute
