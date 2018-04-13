> 以下用法是在ubuntu系统下的用法，主要内容整理自[廖雪峰的官方网站](https://www.liaoxuefeng.com/)

# 安装git
`sudo apt-get install git`

# 声明git账号
`git config --global user.name "Your Name"`
`git config --global user.email "email@example.com"`

# 创建版本库（假设库名为learngit）
`mkdir learngit`
`cd learngit`
`git init`
接着创建一个文本文件readme.txt,并写入内容＂hello＂
`git add readme.txt`
`git commit -m "wrote a readme file"`

# 查看git状态
`git status`
`git diff`  #查看修改内容

# 查看提交版本号：
`git log`
`git reflog`  #未来的版本
`git reset --hard commit_id`  # 强制回退到某个版本

# 撤消修改
`git checkout -- readme.txt`　　＃丢弃工作区的修改
`git reset HEAD readme.txt`  #丢弃暂存区的修改＇

# 删除文件
`git rm test.txt`
`git commit -m "remove test.txt"`

# 创建SSH Key(在用户主目录下)
`ssh-keygen -t rsa -C "dnxbjyj@126.com"`
在刚刚提示的目录下找到id_rsa.pub文件，用文本编辑器打开，复制里面的一长串字符；登录github,在账号设置里面找到SSH Keys页面，填入任意title,在Key文本框里复制进去刚刚复制的字符，然后点击Add Key,之后就能从本地push了。

# 添加远程库
(在github建立远程库，假设建立的库名为learngit)
`git remote add origin git@github.com:dnxbjyj/learngit.git`  #关联远程库
`git push -u origin master`  #第一次推送master分支的所有内容
`git push origin master`  #后面推送master的所有内容
`git remote rm origin`  #断开和远程库的关联

# 创建与合并分支
`git branch`  #查看分支
`git branch <name>`  #创建分支
`git checkout <name>`  #切换到某分支
`git branch -b <name>`  #创建并跳转到某分支
`git merge <name>`  #合并某分支到当前分支
`git branch -d <name>` 　#删除某分支
`git branch -D <name>`    #强制删除没有合并完全的分支

# 推送分支
`git remote`  #查看远程库的信息
`git remote -v`  #查看远程库的详细信息，显示可以抓取和推送的origin的地址
`git push origin master`  #向远程的origin推送本地的master分支

# 抓取分支
`git checkout -b dev origin/dev`  #创建远程origin的dev分支到本地
`git branch --set-upstream-to = origin/dev`  #指定本地dev分支与远程origin/dev分支的链接
`git pull`  #把最新提交从origin/dev上抓取下来
(再合并分支，若出现冲突，则解决冲突,再add,commit)
`git push origin dev`  #push dev分支

# 把最新的分支从origin/goods上抓取下来到当前本地分支：
`git pull origin goods`

# git clone远程仓库的某个分支到本地：
`git clone -b goods git@github.com:senguo2014/senguo.cc.git`　　＃clone远程的goods分支

# 完整流程
### 拉远程库最新的代码到本地分支：
`git fetch origin test:tmp` #将远程库上origin目录下的test分支拉到本地库并在本地库创建tmp分支
或：
`git pull origin test`　　＃将远程库上origin下的test分支拉到本地当前分支上（会自动merge）
### 切换到本地的working分支：
`git checkout working`
`git branch`  #查看当前分支
### 写代码，修改代码．然后提交所有修改：
`gti status`  #查看当前分支状态
`git add .`　＃注：最后是一个点
`git commit -a -m "hello"`
### 将本地的tmp分支合并到当前的working分支：
`git merge tmp`
### 根据提示，打开代码文件逐一修改冲突
`HEAD<<<<<<<<<<<内容１=======内容２>>>>>>>working`
### 冲突修改完以后，再merge一遍，然后将当前分支的内容提交到远程库的test分支上：
`git push origin test`

### 总结：可以简略地归结为三步曲：
`git fetch origin master:tmp`  #将远程的master分支fetch到本地的tmp分支上,若tmp分支不存在,则自动新建.
`git diff tmp`
`git merge tmp`  #将当前分支和tmp分支merge
`git push origin master:newbranch`  #其中master表示本地master,newbranch表示在远程创建的新分支或远程已经有的分支.

# 删除远程test分支：
`git push origin --delete test`

# 推送分支
`git push <远程主机名(origin)> <本地分支名>:<远程分支名>`
 注意，分支推送顺序的写法是`<来源地>:<目的地>`，所以git pull是`<远程分支>:<本地分支>`，而git push是`<本地分支>:<远程分支>`。
如果省略远程分支名，则表示将本地分支推送与之存在”追踪关系”的远程分支(通常两者同名)，如果该远程分支不存在，则会被新建。

# git的.gitignore不起作用的原因
可能为：先添加到本地分支其他文件再添加的.gitignore文件
解决方法：先清空本地分支，然后先添加和提交.gitignore文件到本地分支，然后再添加提交其他文件到本地分支，然后再往远程分支推．

# 文件权限问题
git上fetch下来的文件的默认权限是100644，在这种权限下在本地是无法对代码进行修改的，需要`chmod -R 777 workgit`，然后对代码进行修改．在向远程push代码的时候，还要先把权限改回100644，这样才不会起冲突(这种修改权限的方法可能会失效,所以最好的解决方法就是不要修改权限,而用sudo权限打开sublime然后再编辑代码)．

# 在新建库后pull或clone的时候出现错误：
```
Permission denied (publickey).
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
```

可能的解决的方法：
１．`ssh-keygen...`命令前加sudo，然后再按原来的步骤来做．

# 公钥只与电脑有关,与是否新建仓库无关

# 查看历史版本
`git log`
