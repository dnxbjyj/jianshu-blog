本文主要总结了python正则零宽断言（zero-length-assertion）的一些常用用法。

# 1. 什么是零宽断言

有时候在使用正则表达式做匹配的时候，我们希望匹配一个字符串，这个字符串的前面或后面需要是特定的内容，但我们又不想要前面或后面的这个特定的内容，这时候就需要零宽断言的帮助了。所谓零宽断言，简单来说就是匹配一个位置，这个位置满足某个正则，但是不纳入匹配结果的，所以叫“零宽”，而且这个位置的前面或后面需要满足某种正则。

比如对于一个字符串：`finished going done doing`，我们希望匹配出其中的以`ing`结尾的单词，就可以使用零宽断言：


```python
import re
s = 'finished going done doing'
p = re.compile(r'\b\w+(?=ing\b)')

print '【Output】'
print [x + 'ing' for x in re.findall(p,s)]
```

    【Output】
    ['going', 'doing']


可以看出从中匹配出了`going`和`doing`两个单词，达到目的。

这里正则中使用的`(?=ing\b)`就是一种零宽断言，它匹配这样一个位置：这个位置有一个`ing`字符串，后面跟着一个`\b`符号，并且这个位置前面的字符串满足正则：`\b\w+`，于是匹配结果就是：`['go','do']`

# 2. 不同的零宽断言

零宽断言分为四种：正预测先行断言、正回顾后发断言、负预测先行断言、负回顾后发断言，不同的断言匹配的位置不同。

总结一下，这几个仿佛说的不是"人话"的令人费解的名词可以这样理解：其中的“正”指的是肯定预测，即某个位置满足某个正则，而与之对应的“负”则指的是否定预测，即某个位置不要满足某个正则；其中的“预测先行”则指的是“往后看”，“先往后走”的意思，即这个位置是出现在某一个字符串后面的，而与之相反的“回顾后发”则指的是相反的意思：“往前看”，即匹配的这个位置是出现在某个字符串的前面的。

不理解没关系，我们用实例说话，下面对每种零宽断言进行详细介绍。

## 1. 正预测先行断言：`(?=exp)`

匹配一个位置（但结果不包含此位置）之前的文本内容，这个位置满足正则exp，举例：匹配出字符串s中以ing结尾的单词的前半部分：


```python
s = "I'm singing while you're dancing."
p = re.compile(r'\b\w+(?=ing\b)')

print '【Output】'
print re.findall(p,s)
```

    【Output】
    ['sing', 'danc']


## 2. 正回顾后发断言：`(?<=exp)`

匹配一个位置（但结果不包含此位置）之后的文本，这个位置满足正则exp，举例：匹配出字符串s中以do开头的单词的后半部分：


```python
s = "doing done do todo"
p = re.compile(r'(?<=\bdo)\w+\b')

print '【Output】'
print re.findall(p,s)
```

    【Output】
    ['ing', 'ne']


## 3. 负预测先行断言：`(?!exp)`

匹配一个位置（但结果不包含此位置）之前的文本，此位置不能满足正则exp，举例：匹配出字符串s中不以ing结尾的单词的前半部分：


```python
s = 'done run going'
p = re.compile(r'\b\w+(?!ing\b)')

print '【Output】'
print re.findall(p,s)
```

    【Output】
    ['done', 'run', 'going']


可见，出问题了，这不是我们预期的结果（预期的结果是：done和run），这是因为负向断言不支持匹配不定长的表达式，将p改一下再匹配：


```python
s = 'done run going'
p = re.compile(r'\b\w{2}(?!ing\b)')

print '【Output】'
print re.findall(p,s)
```

    【Output】
    ['do', 'ru']


可见一次只能匹配出固定长度的不以ing结尾的单词，没有完全达到预期。这个问题还有待解决。

## 4. 负回顾后发断言：`(?<!exp)`

匹配一个位置（但结果不包含此位置）之后的文本，这个位置不能满足正则exp，举例：匹配字符串s中不以do开头的单词：


```python
s = 'done run going'
p = re.compile(r'(?<!\bdo)\w+\b')

print '【Output】'
print re.findall(p,s)
```

    【Output】
    ['done', 'run', 'going']


可见也存在与负预测先行断言相同的问题，改一下：


```python
s = 'done run going'
p = re.compile(r'(?<!\bdo)\w{2}\b')

print '【Output】'
print re.findall(p,s)
```

    【Output】
    ['un', 'ng']


## 5. 正向零宽断言的结合使用

举例：字符串ip是一个ip地址，现在要匹配出其中的四个整数：


```python
ip = '160.158.0.77'
p = re.compile(r'(?<=\.)?\d+(?=\.)?')

print '【Output】'
print re.findall(p,ip)
```

    【Output】
    ['160', '158', '0', '77']


## 6. 负向零宽断言的结合使用

举例：匹配字符串s中的一些单词，这些单词不以`x`开头且不以`y`结尾：


```python
s = 'xaay xbbc accd'
p = re.compile(r'(?<!\bx)\w+(?!y\b)')

print '【Output】'
print re.findall(p,s)
```

    【Output】
    ['xaay', 'xbbc', 'accd']


可见这里因为负向断言不支持不定长表达式，所以也存在和前面相同的问题。

# 3. 零宽断言的应用

## 1. 匹配html标签之间的内容


```python
s = '<span>Hello world!</span>'
p = re.compile(r'(?<=<(?:\w+)>(.*)(?=</\1>))')

print '【Output】'
print re.findall(p,s)
# 报错：error: look-behind requires fixed-width pattern
```

上面的报错是因为零宽断言的正则中不能含有不定长的表达式，改一下：


```python
s = '<span>Hello world!</span>'
p = re.compile(r'(?<=<(\w{4})>)(.*)(?=</\1>)')

print '【Output】'
print re.findall(p,s)
```

    【Output】
    [('span', 'Hello world!')]


## 2. 匹配存在多种规则约束（含否定规则）的字符串

匹配一个长度为4个字符的字符串，该字符串只能由数字、字母或下划线3种字符组成，且必须包含其中的至少两种字符，且不能以下划线或数字开头：


```python
# 测试数据
strs = ['_aaa','1aaa','aaaa','a_12','a1','a_123','1234','____']
p = re.compile(r'^(?!_)(?!\d)(?!\d+$)(?![a-zA-Z]+$)\w{4}$')

print '【Output】'
for s in strs:
    print re.findall(p,s)
```

    【Output】
    []
    []
    []
    ['a_12']
    []
    []
    []
    []

## 3. 注意点

零宽断言虽然也是用小括号括起来的，但不占用分组的默认命名空间。举例如下：

```python
s = 'goingxxx'
# 在紧跟'ing'后面的字符串前加上'AAA'
print re.sub(r'(?<=ing)(\w+)\b',r'AAA\1',s)
# 输出： goingAAAxxx
```
