有时候工作区中会有我们创建的一些密码配置文件，或者自动生成的一些临时文件，比如python代码编译产生的.pyc文件和java代码编译产生的.class文件等，我们在提交代码的时候没有必要把这些文件也提交。这时就可以用.gitignore文件来指定提交时需要忽略的文件/文件夹列表，那么下次提交时这些文件就不会被提交到本地和远程的代码库中。

## 已有的.gitignore文件大全

链接：https://github.com/github/gitignore

针对各种语言的，可以直接拿来用。在github上创建远程仓库的时候，也可以直接指定选择哪些.gitignore文件。

## 自己创建.gitignore文件

* 在当前本地git仓库根目录下，创建一个名为".gitignore"的文件，并在其中按如下格式写入要忽略的文件/文件夹：

```bash
# i will ignore these files:
*.dll
*.class
*.pyc
debug/*
```

注：第1行"#"后面的是注释，第2~4行分别表示要忽略`*.dll、*.class、*.pyc`文件，最后一行表示忽略掉debug目录及其子目录的所有内容。

* 保存并提交该.gitignore文件。

* 用`git status`命令再查看状态，发现工作区的状态已经是clean了，没有再提示`*.dll、*.class、*.pyc`这些类型的文件和debug目录下的文件未提交了。

## 清除已经提交的文件

比如在配置.gitignore文件之前，就不小心提交了一些dll文件和debug目录下的文件，现在想清除仓库中的这些文件，那么可以这样办：

```bash
git rm *.dll 
git rm -r debug
git rm --cached *.dll
git rm –r --cached debug
git commit -m "清除缓存"
```

执行完之后发现代码库中就没有这些文件/文件夹了。

## 修改git的全局配置

上面添加了.gitignore文件之后，只会对当前仓库产生影响，那么如果想把这个.gitignore文件作为全局配置，该怎么办呢？

* 创建一个.gitignore_global文件，添加要忽略的文件/文件夹清单。

* 执行命令：`git config --global core.excludesfile .gitignore_global`即可。
