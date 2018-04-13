如果你是一个程序员，并且使用过Eclipse这样一个IDE开发过程序，那你对Eclipse插件一定不会陌生。因为在Eclipse中，几乎一切功能皆是插件。在Eclipse插件市场、GitHub等各种地方也有着多如牛毛的插件，不过如果你曾思考过这样一个问题：**我能不能自己开发一些插件来灵活地实现自己独特的需求？**那么本文我们就可以一起来探讨下如何开始开发属于自己的Eclipse插件。

本文将从Eclipse插件是什么、为什么要开发插件、怎样开发一个Hello Word插件以及下一步该怎么做四件事来探讨。

# Eclipse插件是什么
说起"插件"，我们很容易联想到一个东西，那就是电源插座和插头，像这样的：
![](https://upload-images.jianshu.io/upload_images/8819542-9813475faa757cb1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

一个插座上可以有很多个插孔，每个插孔都可以插入不同的插头，比如可以插我的电脑的充电插头，插手机的充电插头，插台灯的插头...概括来说，插座上的插孔提供了一种基础能力，那就是——提供电力，使用插孔提供的电力我们可以让形形色色的电器运转起来，从而让我们的生活变得多姿多彩。

Eclipse插件其实也就像插孔和插头，Eclipse核心层代码提供了基于操作系统的核心基础能力，将这些能力进行封装，并将封装后的能力根据一定的规范、以插孔的形式对外开放出来，千千万万的开发者可以基于这些插孔提供的各种能力，专注于开发自己需要的各种各样的插头（即各种插件）实现自己的需求，而不用陷入诸如"插孔的能力究竟是怎样实现的"这样的复杂的底层细节中去。

所以说Eclipse插件就是类似于插座插孔和插头这样一种东西，具有非常高的可扩展性。

# 为什么要开发Eclipse插件
如果我们日常使用Eclipse作为自己工作或学习的IDE，可能在有些时候希望有这样或那样一个插件，来帮助我们完成一些事情，比如对自己的代码做一些统计，或者想定时自动提交自己的代码到GitHub，或者想在Eclipse中就可以翻译英文单词而不用再打开浏览器使用谷歌翻译，或者想在Eclipse中就能看到今天的天气是怎样的（这种需求也是挺清奇的，但真的可能有这种需求）等等。

目前已经有千千万万的开发者开发的成千上万、数不胜数的插件，那么为什么我们还要自己开发插件？这是因为现实需求无限而插件有限，以有限满足无限，殆矣。

你总会遇到千奇百怪的实际需求，而不可能任何需求都恰好有对应的插件可以完美满足，这个时候就要我们自己动手开发满足自己特定需求的插件，且自己开发的插件可高度定制化，想怎么玩就怎么玩，具有充分的自由度。

从另一个方面来讲，Eclipse的用户群体十分庞大，如果你自己开发的插件所解决的问题比较有普遍性（比如做代码统计），别人可能恰好也有类似需求，那么你就可以把自己开发的插件分享（比如通过GitHub等）给其他人使用，或者开源出来和其他人交流（Eclipse本身就是开源的），体会帮助到别人的乐趣。

# 怎样开发一个Hello Word插件
### 安装Eclipse
插件开发需要使用**for Java EE**的Eclipse版本，Eclipse的具体安装细节这里不再赘述。
> Eclipse官网下载地址：https://www.eclipse.org/downloads/

### 创建一个Hello World插件工程（plugin-in project）
* 打开Eclipse，点击菜单`file > new > other`，找到并选择`Plugin-in Project`，然后点击`Next`按钮：
![](https://upload-images.jianshu.io/upload_images/8819542-a628953228c8c67c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
* 输入工程的名称为`HelloWorld`，其他选项都保持默认，然后点`Next`：
![](https://upload-images.jianshu.io/upload_images/8819542-a448cf1da8312aaa.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
* 这个页面的内容都保持默认，继续点`Next`：
![](https://upload-images.jianshu.io/upload_images/8819542-39a7ed242460a448.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
* 在左边选择`Hello, World`这样一个模板，然后点`Next`：
![](https://upload-images.jianshu.io/upload_images/8819542-ad4d7a0a639ddec4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
* 在这里可以指定插件的包名、Action类名和运行程序后弹出的`Hello World`窗口所显示的文本，最后点击`Finish`：
![](https://upload-images.jianshu.io/upload_images/8819542-b9f672a77223eade.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
* 经过上面的步骤，一个最简单的插件工程就创建好了，工程的结构如下，其中最重要的是`META-INF`目录下的`MANIFEST.MF`工程清单文件，它统领着插件的全局，以后会细讲。其次，Eclipse插件是基于Java语言开发的。
![](https://upload-images.jianshu.io/upload_images/8819542-562e43075aa235a4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 运行Hello World插件工程
* 右键点击刚刚创建好的插件工程，点击`Run As > Eclipse Application`菜单：
![](https://upload-images.jianshu.io/upload_images/8819542-28b4d35bd2090e76.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
* 稍等片刻后，可以看到会启动一个新的Eclipse程序，并在工具栏有一个提示为`Hello, Eclipse world`的按钮：
![](https://upload-images.jianshu.io/upload_images/8819542-1a6feb93f4884b10.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
* 点击`Hello, Eclipse world`按钮，弹出一个弹窗如下：
![](https://upload-images.jianshu.io/upload_images/8819542-87cf31de2aa8c535.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
* 可以看到，我们的Hello World插件程序顺利运行起来了！弹窗中所展示的文字正是我们在创建插件工程最后一步所填写的文本内容。

# 下一步应该做什么
在了解了一个Hello World插件程序是怎样创建并运行起来之后，下一步要做的有：
* 插件工程中各部分代码都是干什么的？
* Eclipse工作台窗口的认识。
* Eclipse插件体系结构——扩展点机制。

# 学习资源
下面是一些收集的学习资源：
*  [CSDN专栏：Eclipse插件开发实战系列](https://blog.csdn.net/column/details/eclipse-plugin.html)
* [《Eclipse插件开发学习笔记》目录书签版（百度网盘）](https://pan.baidu.com/s/1Enr13dkhtZqJihSG-kxY2w)
