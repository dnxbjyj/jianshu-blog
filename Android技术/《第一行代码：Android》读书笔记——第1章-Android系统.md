# （一）Android系统架构

* Linux内核层：各种底层驱动，如显示驱动、音频驱动、电源管理等。

* 系统运行库层：各种库支持，如3D绘图、浏览器内核、数据库等。

* 应用框架层：各种API,各种Manager。

* 应用层：所有的应用程序。

# （二）安卓系统级功能

* 四大组件：`Activity,Service,Broadcast,Content Provider`

* 系统控件：用于写界面，也可以自己定制界面。

* SQLite数据库：轻量级、快速的嵌入式关系型数据库。

* 地理位置定位：内置GPS,基于它可以开发LBS应用。

* 多媒体：音频、视频、录音、拍照、视频等。

* 传感器：加速度传感器、方向传感器。

# （三）搭建Android开发环境

### 准备所需要的软件：

* Android SDK

* 编译器：Eclipse

* ADT：是Eclipse的插件
PS：一整套工具百度网盘存放地址：http://pan.baidu.com/s/1jI6fmjO

* 创建手机模拟器：用ARM架构的更快一些.
PS:模拟器出问题时，先重启adb试试(在DDMS中)，再重启Eclipse

# （四）Eclipse中项目文件结构

* src：放所有Java代码的地方

* gen：这个目录的内容都是自动生成的，主要有一个R.java文件，不要尝试手动去修改它！

java代码中：`R.xx.xx查询`

xml文件中：`@xx/xx查询`

比如：
```java
　　　　R.string.hello_world
　　　　@string/hello_world
```
* assets：存放一些随程序打包的文件

* bin：包含一些在编译时自动产生的文件，其中会有一个apk文件，可以在手机上直接安装.

* libs：包含第三方Jar包

* res：图片、布局、字符串等各种资源

* `AndroidManifest.xml`：项目配置文件，用到的所有四大组件都需要在这里注册.还可以添加权限声明、设置版本等.

* `project.properties`：只有一行代码，指定编译程序时所使用的SDK版本.

# （五）安卓项目中的资源（res目录）

* 以drawable开头的文件夹：存放图片.
PS:项目的图标文件就是在`AndroidManifest.xml`文件中通过下面代码指定的：`android:icon="@drawable/ic_launcher"`

* 以values开头的文件夹：存放字符串

* layout文件夹：存放布局文件

* menu文件夹：存放菜单文件

# （六）日志工具android.util.Log 

* Log.v( )：打印琐碎的日志信息

* Log.d( )：打印调试信息

* Log.i( )：打印比较重要的数据

* Log.w( )：打印警告信息

* Log.e( )：打印错误信息
