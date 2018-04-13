> Bmob后端云官网：http://www.bmob.cn/
> 微信公众平台官网：https://mp.weixin.qq.com/
> 微信小程序官方开发文档：https://mp.weixin.qq.com/debug/wxadoc/dev/

本文对如何在微信小程序中接入Bmob后端云做一个简单的总结。所谓后端云，一句话概括就是跑在云端的数据库后台+服务器后台，引入到微信小程序开发中能带来的好处就是：让我们可以专注于小程序本身的业务逻辑开发，而不用去管复杂的后台服务器、后台数据库的搭建和维护。

# 准备一个小程序公众号和Bmob账号

首先需要到微信公众平台官网上去注册一个小程序类型的公众号，假设将要开发的小程序命名为：`MyApp`

打开Bmob官网注册一个账号。

# 获取并记录好MyApp小程序的AppID和AppSecret

这两项信息在小程序后台的"设置－开发设置"页面可以获取到，获取到后需要在一个文本文件中记好，后面要用到。

# 登录Bmob控制台

创建一个应用，假设名字叫`MyBmobApp`，然后进入应用。到"设置"页面输入刚刚获取到的小程序的`AppID`和`AppSecret`并保存。

获取并记好`MyBmobApp`对应的`Application ID`和`REST API key`.

# 登录小程序MyApp后台

到"设置－开发设置－服务器域名"页面添加Bmob安全域名并保存（可一次性添加多个）。

注：四种安全域名(两种类型：`https`和`wss`)全部填`api.bmob.cn`和`xxx.bmobcloud.com`，其中`xxx`为`MyBmobApp`的`Application ID`.

# 下载SDK

到Bmob官网下载微信小程序对应的SDK并解压，将其中的所有js文件都放到小程序工程的utils目录下。

# 初始化和引入Bmob

在小程序工程的app.js中加入如下代码进行全局初始化：

```javascript
var Bmob = require('utils/bmob.js');
Bmob.initialize('XXX','XXXXXX');
// 注：其中'XXX'为MyBmobApp的Application ID,'XXXXXX'为其REST API key
```

在需要用到Bmob的page页的js中引入Bmob：

```javascript
var Bmob = require('../../utils/bmob.js');
```

现在就可以在小程序中对Bmob后端云数据库进行各种操作了，像操作本地数据库那么简单。
