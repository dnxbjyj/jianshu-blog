因为一些历史原因，Windows系统下文本文件是以`\r\n`作为换行符的，其十六进制就是：`0D 0A`，把这种文本格式称为dos格式；而在Linux系统下文本文件是以`\n`作为换行符的，其十六进制就是：`0A`，把这种文本格式称为unix格式。如果在Windows系统下去读取unix格式的文本文件，或者在Linux系统下去读取dos格式的文件，或多或少都会出现一些问题。

在Linux系统下有2个命令：`dos2unix`和`unix2dos`，可以将两种格式的文本文件互相转换。那么接下来我们用Python实现一个`dos2unix`工具，实现完了之后`unix2dos`就非常简单了，不再单独再说。

# 用Python判断一个文件是否是dos格式的
### 准备一个文本文件
首先准备一个文本文件：`file.txt`，其格式为dos格式，我们在notepad++中把它打开，并点击菜单栏"视图"—>"显示符号"—>"显示行尾符"，看到的效果是这样的：
![](http://upload-images.jianshu.io/upload_images/8819542-df2b72b0cd539e77.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

可以看到每行的结尾的换行符都是`CR LF`，这其实就是`\r\n`。在notepad++右下角状态栏也可以看到这个文件是dos格式的：
![](http://upload-images.jianshu.io/upload_images/8819542-d589a8002e5e3051.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 判断一个文件是否是dos格式
我们知道dos文件是以`\r\n`作为换行符的，那么判断一个文件是否是dos格式的就比较简单了，直接上代码：
```python
# coding:utf-8
import re

file_name = 'file.txt'
content = ''
with open(file_name,'r') as fin:
    content = fin.read()
print re.findall(r'\r\n',content)
```
运行上面脚本，结果如下：
![](http://upload-images.jianshu.io/upload_images/8819542-ca73c8503cc143d0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
可以看到匹配结果为空，但是file.txt中明明有那么多`\r\n`换行符，为什么没有匹配到呢？

经过分析发现，这是因为Python在以`r`模式读取文本文件的时候，会自动将其转为unix格式，因此只能读取到`\n`换行符：

```python
# coding:utf-8
import re

file_name = 'file.txt'
content = ''
with open(file_name,'r') as fin:
    content = fin.read()
print re.findall(r'\n',content)
```

运行上面的代码，结果如下：
![](http://upload-images.jianshu.io/upload_images/8819542-a843330b31cd4c19.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

那么问题就来了，我们怎么匹配到`\r\n`呢？经过了一番研究发现，用'rb'模式读取文本文件就可以了，代码如下：

```python
# coding:utf-8
import re

file_name = 'file.txt'
content = ''
# 这里需要用'rb'模式读取文本文件，否则，如果file.txt是dos格式文件，是读取不到'\r\n'换行符的
with open(file_name,'rb') as fin:
    content = fin.read()
print re.findall(r'\r\n',content)
```

上面代码运行结果如下：
![](http://upload-images.jianshu.io/upload_images/8819542-e27faaf62ef1abaf.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

可以看出成功匹配出了文本文件中的`\r\n`。这里要注意的是，对于`rb`模式读取的文本文件内容，正则的`re.M`多行模式是失效的，比如我们下面只匹配行尾的`\r\n`：
```python
# coding:utf-8
import re

file_name = 'file.txt'
content = ''
# 这里需要用'rb'模式读取文本文件，否则，如果file.txt是dos格式文件，是读取不到'\r\n'换行符的
with open(file_name,'rb') as fin:
    content = fin.read()
print re.findall(r'\r\n$',content,re.M)
```
运行结果：
![](http://upload-images.jianshu.io/upload_images/8819542-e243689c5d36e8f9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
可以看到只匹配到了文件的最后一个`\r\n`，这一点疑问还需要继续研究。

# 将dos格式文本文件转为unix格式
经过上述一番探讨，怎么把dos文件转为unix格式就比较简单了，简单来说就是把文件中的所有`\r\n`换行符替换为`\n`，上代码：

```python
# coding:utf-8
import re

file_name = 'file.txt'
content = ''
# 这里需要用'rb'模式读取文本文件，否则，如果file.txt是dos格式文件，是读取不到'\r\n'换行符的
with open(file_name,'rb') as fin:
    content = fin.read()

# 这里要注意的是，re.M模式同样是失效的
content = re.sub(r'\r\n',r'\n',content)
with open(file_name,'wb') as fout:
    fout.write(content)
```
运行上面脚本之后，去查看file.txt文件，发现其换行符已经变成了`\n`：
![](http://upload-images.jianshu.io/upload_images/8819542-f1e17490e2f7e780.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### tips
其实notepad++本身也带有将一个文本文件转为unix格式的功能，方法是：打开一个文本文件—>"编辑"菜单—>"文档格式转换"—>"转换为UNIX格式"即可。当然也可以转换为dos格式或mac格式（mac格式是以`\r`作为换行符的）。
