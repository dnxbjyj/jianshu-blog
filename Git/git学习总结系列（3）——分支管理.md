本文主要介绍git分支的概念及常用分支操作。

## 分支的概念

所谓分支，可以理解成一个个相互独立的工作空间，在每一个分支上的改动不会影响到其他分支的代码。git默认的分支是master分支。

试想一下这样一个场景：

正在master分支写主干需求的代码，突然来了一个很紧急的临时需求，需要在一周之内完成。如果在master分支直接开发的话，可能会造成主干需求的代码出现问题，这个时候就可以新拉一个分支（比如叫dev），dev分支的初始代码和master分支的完全相同，这个时候就可以放心的在dev分支上开发新需求了，不用担心会影响到master分支。等到在dev分支开发完新需求并充分测试验证没问题之后，就可以合并到master分支了，合并之后就可以删掉dev分支。

## 创建与合并、删除分支

* 查看当前分支：`git branch`

会列出来所有分支，并且会在当前分支前面加上一个`*`

* 创建一个名为"dev"的分支：`git branch dev`

* 切换到名为"dev"的分支：`git checkout dev`

* 创建一个名为"dev"的分支并切换到dev：`git checkout -b dev`

* 假如当前在master分支，合并dev分支到当前分支：`git merge dev`

* 假如当前在master分支上，删除另外一个分支dev：`git branch -d dev`

注：如果当前在dev分支，那么是无法删除dev分支的。如果dev分支并没有和master分支合并，也是无法删除的，除非使用强制删除命令：`git branch -D dev`

## 查看分支合并历史记录

当合并分支出现冲突时，需要先解决冲突，再合并分支。使用`git log --graph`命令可以查看合并分支的历史记录。

注：要注意的是，`git merge <branch-name>`命令默认采用的是fast-forward模式，也就是如果合并某个分支（比如dev）到比如master分支后，把dev删掉，那么在这种模式下的历史记录里是看不到合并记录的。如果想要看到dev分支合并的历史记录，那么在合并时就要采用普通模式：`git merge --no-ff -m "merge with no-ff" <branch-name>`，这里加-m参数是因为本次合并要创一个新的commit.

## 保存与恢复工作现场

* 假如当前在dev分支上，保存工作现场命令：`git stash`，可保存多个工作现场。

* 查看保存的工作现场列表：`git stash list`

* 恢复并删除最后保存的工作现场：`git stash pop`

* 恢复指定的工作现场：`git stash apply stash@{0}`

* 删除指定的工作现场：`git stash drop stash@{0}`

## 操作远程仓库

* 查看远程库信息：`git remote -v`

* 在本地创建和远程分支相关联的分支：`git checkout -b <local-branch-name> origin/<remote-branch-name>`，本地和远程分支的名称最好相同。

* 把本地dev分支推送到远程库：`git push origin dev`

注：如果推送失败，可能本地代码不是最新的，可以先用`git pull`命令先把远程的代码拉到本地，如果有冲突处理一下冲突，然后再推送。不过`git pull`命令也有可能失败，这是因为没有建立本地分支和远程分支的关联，还需要先用这个命令建立关联：`git branch --set-upstream <local-branch-name> origin/<remote-branch-name>`

## 多人协作推荐的分支策略

* master分支放用于发布的代码，平时不要在master分支上进行日常开发。

* 建立dev分支用于平时的开发，在发布版本的时候把代码合并到master分支。

* 团队的每个人从dev分支建立以自己名字命名的分支，如：zhangsan,lisi,wangwu, 每天结束后都把各自代码合到dev分支上。

* 多人开发的新需要，可以从dev分支建立feature分支，在feature分支上进行开发，开发完成后合入dev分支。

* 当master分支出现bug时，可以基于master拉一个bug分支，在bug分支上修改并调试好bug后再合入master分支。

## 多人协作常见的协作模式

* 日常可以通过`git push origin <local-branch-name>`来往远程推送自己的修改。

* 如果推送失败，说明远程的代码比本地的要新，需要使用`git pull`先试图合并。

* 如果合并有冲突，则先解决冲突，然后在本地commit.

* 如果没有冲突，或解决完冲突后，再使用`git push origin <local-branch-name>`即可推送成功。

* 如果`git pull`命令提示`no tracking information`，则说明本地分支没有和远程分支建立关联，用这个命令建立关联：`git branch --set-upstream <local-branch-name> origin/<remote-branch-name>`

* 如果上面一条命令仍然执行不成功，说明本地仓库还没有和远程仓库建立连接，可以用如下命令建立连接：`git remote add origin git@github.com:xxx/xxx.git`
