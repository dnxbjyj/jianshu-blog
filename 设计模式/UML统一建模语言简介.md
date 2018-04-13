# UML概述

* 面向对象软件开发的过程：

（1）OOA(面向对象分析)：建立分析模型并文档化。

（2）OOD(面向对象设计)：用面向对象思想对OOA的结果进行细化，得出设计模型。

（3）OOP(面向对象编程)

* UML就是将OOA和OOD的结果用统一的符号来描述和记录。

* UML已经是可视化建模事实上的工业标准。

* 不要把UML当成一种负担，而是当成工具。

* UML有13种图形，最常用的有：用例图、类图、组件图、部署图、顺序图、活动图、状态机图。

# 用例图

### 用例图的概念
用例图用于描述系统的系列功能，一个用例图代表系统的一个功能模块，由“用例+角色”组成，主要在需求分析阶段使用。

* 用例：用椭圆表示。

* 角色：用一个人形符号表示。

* 用例之间的依赖关系：用虚线箭头表示

### 一个BBS系统的用例图：

![](http://upload-images.jianshu.io/upload_images/8819542-252a5e53901b7d34.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

# 类图

* 类图用一个三层的矩形框表示，第一层写类名，第二层包含类的属性，第三层包含类的方法。如下图示例：

![](http://upload-images.jianshu.io/upload_images/8819542-8fd54303937ad8fe.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

* 类之间的三种关系：关联（包括聚合和组合）、泛化（和继承是同一概念）、依赖。

* 关联：

（1）关联和属性很像，两者的区别：类里的某个属性引用到另外一个实体时，就变成了关联。

（2）关联用一条实线来表示，带箭头的实线表示单向关联。

（3）关联包含两种特例：聚合和组合。两者区别：

①聚合：当某个实体A聚合成另一个实体B时，A还可以同时是另外一个实体的一部分。比如学生既可以是网球俱乐部的成员，也可以是羽毛球俱乐部的成员。

聚合使用带空心菱形框的实线表示。

②组合：当某个实体A组合成另一个实体B时，A不能同时是另外一个实体的一部分。比如手是人这个实体的一部分，手组合成为一个人的一部分后，不能同时是另外一个人的一部分。

组合使用带实心菱形框的实线表示。

关联关系示例图如下：

![](http://upload-images.jianshu.io/upload_images/8819542-06a5cdddecb4adb0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

* 泛化关系：即继承关系，用带空心三角形的实线表示。对接口的实现也可以看成是一种特殊的继承，

实现接口的关系用带空心三角形的虚线表示。示例图如下：

![](http://upload-images.jianshu.io/upload_images/8819542-7cbec5a4ad9dee05.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

* 依赖关系：如果一个类的改动会导致另一个类的改动，则两者之间存在依赖关系。依赖的常见原因：

（1）改动的类将消息发送给另一个类；

（2）改动的类以另一个类作为数据部分；

（3）改动的类以另一个类作为操作参数。

依赖用带箭头的虚线表示，箭头在被依赖的类一侧，依赖关系示例图如下：

![](http://upload-images.jianshu.io/upload_images/8819542-646b7346d07a7f84.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

# 组件图

* 对于一个大型应用程序而言，通常由多个可部署的组件组成。

（1）Java：可复用的组件通常打包成JAR、WAR等文件。

（2）C/C++：可复用的组件通常是一个函数库，或者DLL（动态链接库）文件。

* 组件图的用途是显示系统中的软件对其他软件组件（如库函数）的依赖关系。组件图通常包含组件、接口、Port等元素，UML

用带![](http://upload-images.jianshu.io/upload_images/8819542-5045f2a0e2155b8d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

符号的矩形表示组件，用圆圈代表接口，用位于组件边界上的小矩形代表Port。

组件接口表示它能对外提供的服务规范，有两种表示形式：

（1）用一条实线连接到组件边界的圆圈表示；

（2）使用位于组件内部的圆圈表示。

组件依赖于某个接口用一条带半圆弧的实线来表示。

* 组件图示例如下：

![](http://upload-images.jianshu.io/upload_images/8819542-9eea5f74ffefb160.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![](http://upload-images.jianshu.io/upload_images/8819542-a59105ac8a8a553a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

# 部署图

* 部署图显示系统不同组件在何处物理运行，以及它们之间如何通信。

* 部署图示例：

![](http://upload-images.jianshu.io/upload_images/8819542-cb24ce39a0caedf2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

# 顺序图

* 顺序图描述对象之间的交互，注重描述消息及其时间顺序。

* 顺序图示例：

![](http://upload-images.jianshu.io/upload_images/8819542-4216280d86367ae6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

# 活动图

* 活动图 = 传统流程图 + 并行。

* 用于描述用例内部的活动或方法的流程，用于描述过程原理、业务逻辑、工作流。

* 活动图和状态机图都属于演化图，演化图五要素：状态、事件、动作、活动、条件。

* 活动图用圆角矩形表示活动，用带箭头的实线表示事件。

* 活动图示例：

![image](http://upload-images.jianshu.io/upload_images/8819542-160dec7786d912a8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

# 状态机图

* 状态机图表示某个对象所处的不同状态和状态之间的转换信息，当对象的状态大于等于3个时才需要考虑使用状态机图。

* 状态机图5个基本元素：

（1）初始状态：用实心圆来表示。

（2）状态之间的转换：用带箭头的实线表示。

（3）状态：用圆角矩形来表示。

（4）判断点：使用空心圆来表示。

（5）终止点：有一个或多个终止点，使用内部包含实心圆的空心圆表示。

* 状态机图示例：

![](http://upload-images.jianshu.io/upload_images/8819542-5adb46b006c7007a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
