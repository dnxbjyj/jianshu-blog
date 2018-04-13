文件读写是每一门编程语言的最基本的核心功能，有了文件读写功能，才能方便地存储和读取数据。
# 文件读写
假如当前工作目录为`/mypy/`，在该目录下有一个文本文件：`test.txt`，其内容为：
```
www.test.com
hello
```
### 打开文件
* 方法1：
```python
f = open('/mypy/test.txt')
print f
# 输出：<open file 'test.txt',mode 'r' at...>
# 注：如果打开文件的时候不指定模式，默认以`r`模式打开，表示只读
```
* 方法2：
```python
f = file('test.txt')
print f
# 输出：同上
```
可见，`file()`函数和`open()`函数有着相似的功能。

### 读取文件内容
```python
f = open('test.txt')
print f.read()
```
输出：
```
www.test.com
hello
```

### 关闭文件
文件使用完了之后，必须关闭：
```python
f.close()
```

### 向文件中写入内容
```python
f = open('test.txt')
f.write('new')
# 报错：IOError: File not open for writing
```
这样写入内容报错的原因是，以只读方式打开的文件不允许写入内容，而要这样：
```python
f = open('test.txt','w+')
f.write('new')
```
执行上面代码，发现这次没有报错，可是去看`test.txt`文件的内容，并没有新写入的`new`，这是为何呢？是因为还没有执行`f.close()`操作，所以文件还并没有被保存，再执行一下`f.close()`操作，现在再去看文件内容，发现为：
```
new.test.com
hello
```
虽然把最新内容`new`写入了文件，但是却是覆盖了文件的前三个字符，这不是我们想要的，我们想把内容写到文件末尾，这里牵扯到文件指针的问题（后面讲），要达到这个目的，需要这样做：
```python
f = open('test.txt')
f.read()
f.write('new')
f.close()
```
再次执行上述操作，发现文件`test.txt`的末尾成功新增一行`new`。

### 文件读写模式
模式|含义
:-:|:-:
r|只读
r+|读写
w|写入，先删除原文件，再重新创建并写入，若文件不存在则创建
w+|读写，先删除原文件，再重新创建并写入，若文件不存在则创建
a|写入，在文件末尾追加新内容，若文件不存在则创建
a+|读写，在文件末尾追加新内容，若文件不存在则创建
b|打开二进制文件，可与r,w,a,+结合使用，如：wb+
U|支持所有换行符：\r, \n, \r\n，可与r,w,a,+结合，但必须以r开头，如'rUa+', 'rUw+'
注：以'w'、'a'模式打开文件，只支持写入，不支持读。

### 用with语句操作文件
打开文件，推荐使用上下文管理器`with `语句，它可以自动管理文件的打开和关闭，用了它以后就不需手工关闭文件，并且支持一次打开多个文件，非常方便，标准用法如下：
```python
with open('test1.txt','w+') as f1, open('test2.txt','w+') as f2:
  f1.write('123')
  f2.write('456')
```

# 文件对象常用函数
### open
打开一个文件，其实`file()`函数也可以打开一个文件，但是推荐首先`open()`函数。`open()`函数返回一个file对象，是一个可迭代对象，例如依次读取并输出一个文件的每一行的内容：
```python
f = open('file.txt')
for line in f:
  print line
```

### read
若不传入参数，表示从当前文件指针所在位置读到文件末尾；若传入一个表示`size`的参数，表示从当前文件指针所在位置往后读`size`个字节，例如：
```python
f = open('file.txt')
# 从开头往后读3个字节
f.read(3)
# 从第3个字节处往后读5个字节
f.read(5)
# 从第8个字节处读到文件末尾
f.read()
```

### close
关闭文件：
```python
f = open('file.txt')
f.close()
```

### readline
每次读文件的一行，如果不传入任何参数，表示每次读一行的所有字符；如果传入一个表示字节的`size`参数，表示读一行的前`size`个字节，如果上一次本行没有读完，则下一次会接着读，直到行尾。

### readlines
返回一个列表，是包含一个文件的每一行内容的字符串列表。

### next
返回文件的下一行。

### write
往文件中从当前文件指针处写入内容。

### writelines
传入一个字符串列表参数，将该字符串列表写入文件。

### flush
修改文件内容后，提交更新。

### seek(偏移量, 选项)
* 选项 = 0：把文件指针从文件头部向后（不能向前）移动偏移量那么多的字节。
* 选项 = 1：把文件指针从当前位置向后（不能向前）移动偏移量那么多的字节。
* 选项 = 2：把文件指针从文件尾部向前移动偏移量那么多的字节。

**一个原则：移动不能越界，否则会出错。**

一个例子：将文件指针移到文件开头：
```python
f = open('file.txt')
f.seek(0,0)
```

# os模块常用函数
os模块有很多实用的文件、目录和路径操作相关的函数，下面介绍几个最经常用到的。

### os.system()
基于当前目录执行shell命令，并返回命令的执行结果。函数原型：
```
Docstring:
system(command) -> exit_status

Execute the command (a string) in a subshell.
Type:      builtin_function_or_method
```

### os.mkdir()
创建目录，函数原型：
```
mkdir(path [, mode=0777])

Create a directory.
Type:      builtin_function_or_method
```
举例：
```python
# 在当前目录下创建名为dir1的目录
os.mkdir('dir1')
# 使用该方法创建嵌套多层目录会报错
os.mkdir('a/b/c')
# 列出path顶层目录下的文件和文件夹（随机顺序）
os.listdir(path)
```

### os.makedirs()
创建多级目录，函数原型：
```
Signature: os.makedirs(name, mode=511)
Docstring:
makedirs(path [, mode=0777])

Super-mkdir; create a leaf directory and all intermediate ones.
Works like mkdir, except that any intermediate path segment (not
just the rightmost) will be created if it does not exist.  This is
recursive.
File:      e:\code\env\.env\lib\os.py
Type:      function
```

### os.rmdir()
删除目录（需要是空目录），函数原型：
```
Docstring:
rmdir(path)

Remove a directory.
Type:      builtin_function_or_method
```
示例：
```python
os.mkdir('dir1')
# 删除目录dir1
os.rmdir('dir1')

os.makedirs('a/b/c')
# c目录被删掉（若path为多级目录，则只有最低一级的目录被删掉）
os.rmdir('a/b/c')

# 删除失败，提示：OSError: Directory not empty:a，目录非空，无法删除
os.rmdir('a')
```

### os.removedirs()
删除空的多级目录（目录中没有文件），函数原型：
```
Signature: os.removedirs(name)
Docstring:
removedirs(path)

Super-rmdir; remove a leaf directory and all empty intermediate
ones.  Works like rmdir except that, if the leaf directory is
successfully removed, directories corresponding to rightmost path
segments will be pruned away until either the whole path is
consumed or an error occurs.  Errors during this latter phase are
ignored -- they generally mean that a directory was not empty.
File:      e:\code\env\.env\lib\os.py
Type:      function
```
示例：
```python
os.makedirs('a/b/c')
# 将'a/b/c'三级目录同时删掉
os.removedirs('a/b/c')

os.makedirs('a/b/c')
# 然后在'a/b'目录下创建一个名为'file.txt'的文件
# 发现这时只有c目录能被删掉，a、b目录及file.txt文件都还在
os.removedirs('a/b/c')

# 报错：OSError: Directory not empty:'a/b'
os.removedirs('a/b')
```

### os.getcwd()
获取当前的工作目录，函数原型：
```
Docstring:
getcwd() -> path

Return a string representing the current working directory.
Type:      builtin_function_or_method
```

### os.chdir()
修改当前的工作目录，影响`os.getcwd()`函数的返回值，函数原型：
```
Docstring:
chdir(path)

Change the current working directory to the specified path.
Type:      builtin_function_or_method
```

### os.path的几个实用函数
* os.path.isabs()
判断某个路径是否是一个绝对路径。

* os.path.isdir()
判断某个路径是否是一个存在的路径。

* os.path.isfile()
判断某个路径是否是一个文件。

* os.path.islink()
判断某个路径是否是一个超链接。但注意到函数说明中有这么一句话：
```
Signature: os.path.islink(path)
Docstring:
Test for symbolic link.
On WindowsNT/95 and OS/2 always returns false
```
在`WindowsNT/95`和`OS/2`系统，`os.path.islink()`函数总是返回`false`

* os.path.ismount()
判断某个路径是否是一个挂载点：
```
Test whether a path is a mount point (defined as root of drive)
```

* os.path.abspath()
以当前工作目录为前缀，把一个相对路径转为绝对路径。

* os.path.basename()
获取一个路径代表的文件名（包括后缀名）。

* os.path.exists()
判断某个路径是否存在（可以为目录路径也可以为文件路径）。

* os.path.join(path1,*path)
拼接2个或多个路径，若其中一个为绝对路径，那它之前的路径都会被忽略。

### os.walk(top, topdown = True, onerror = None)
遍历根目录`top`，递归地返回一个三元组：
```
(root, dirs, files)
```
其中，`root`为根目录路径，`dirs`为`root`路径下的目录列表，`files`为`root`路径下的文件列表。

`topdown`参数表示是否从顶层目录开始遍历，`onerror`是发生错误时候的回调函数。

函数原型：
```
Directory tree generator.

For each directory in the directory tree rooted at top (including top
itself, but excluding '.' and '..'), yields a 3-tuple

    dirpath, dirnames, filenames

dirpath is a string, the path to the directory.  dirnames is a list of
the names of the subdirectories in dirpath (excluding '.' and '..').
filenames is a list of the names of the non-directory files in dirpath.
Note that the names in the lists are just names, with no path components.
To get a full path (which begins with top) to a file or directory in
dirpath, do os.path.join(dirpath, name).

If optional arg 'topdown' is true or not specified, the triple for a
directory is generated before the triples for any of its subdirectories
(directories are generated top down).  If topdown is false, the triple
for a directory is generated after the triples for all of its
subdirectories (directories are generated bottom up).

When topdown is true, the caller can modify the dirnames list in-place
(e.g., via del or slice assignment), and walk will only recurse into the
subdirectories whose names remain in dirnames; this can be used to prune the
search, or to impose a specific order of visiting.  Modifying dirnames when
topdown is false is ineffective, since the directories in dirnames have
already been generated by the time dirnames itself is generated. No matter
the value of topdown, the list of subdirectories is retrieved before the
tuples for the directory and its subdirectories are generated.

By default errors from the os.listdir() call are ignored.  If
optional arg 'onerror' is specified, it should be a function; it
will be called with one argument, an os.error instance.  It can
report the error to continue with the walk, or raise the exception
to abort the walk.  Note that the filename is available as the
filename attribute of the exception object.

By default, os.walk does not follow symbolic links to subdirectories on
systems that support them.  In order to get this functionality, set the
optional argument 'followlinks' to true.

Caution:  if you pass a relative pathname for top, don't change the
current working directory between resumptions of walk.  walk never
changes the current directory, and assumes that the client doesn't
either.

Example:

import os
from os.path import join, getsize
for root, dirs, files in os.walk('python/Lib/email'):
    print root, "consumes",
    print sum([getsize(join(root, name)) for name in files]),
    print "bytes in", len(files), "non-directory files"
    if 'CVS' in dirs:
        dirs.remove('CVS')  # don't visit CVS directories
File:      e:\code\env\.env\lib\os.py
Type:      function
```
