> Bmob后端云官网：http://www.bmob.cn/
> Bmob后端云微信小程序开发文档：http://docs.bmob.cn/data/wechatApp/b_developdoc/doc/index.html

Bmob是一个很好用的后端云平台，自己在开发小程序的过程中有用到，比较好用，免去了搭建服务器、配置数据库的烦恼，这也符合小程序即用即走的轻量型设计理念。特写一篇文章总结一下常用功能的用法，详细用法可以参看上面的开发文档。

在小程序中使用Bmob后端云的前提是要先接入Bmob，接入方法请参见我的另一篇博文。

# 添加一行数据到diary表中

下面的代码可以在远程创建一个名为'diary'的数据库表并插入一条数据，该表有两个字段：`title`和`content`：

```javascript
// 创建一个表对象
var Diary = Bmob.Object.extend('diary');
// 创建一个表记录对象
var diary = new Diary();

// 插入字段数据
diary.set('title','hello');
diary.set('content','hello world!');

// 保存数据到远程数据库
diary.save(null,{
    success:function(result){
        console.log('create success! data id is:' + result,id);
    },
    error:function(object,error){
        console.log('create failed! error code is:' + error.code + ', error message is:' + error.message);
    }
});
```

# 根据ID查询单条数据

```javascript
var Diary = Bmob.Object.extend('diary');
// 创建一个查询对象
var query = new Bmob.Query(Diary);
// 要查询的记录的ID
var id = '4ecdf7a';

// 查询
query.get(id,{
    success:function(result){
        console.log('标题为：' + result.get('title'));
    },
    error:function(object,error){
        console.log('query failed! error code is:' + error.code + ', error message is:' + error.message);
    }
});
```

# 修改一条数据

```javascript
var Diary = Bmob.Object.extend('diary');
var query = new Bmob.Query(Diary);
// 要修改的记录的ID
var id = '4ecdf7a';

query.get(id,{
    success:function(result){
        result.set('title','a new title');
        result.set('content','hi,guy!');
        
        // 保存提交修改
        result.save();
    },
    error:function(object,error){
        console.log('update failed! error code is:' + error.code + ', error message is:' + error.message);
    }
});
```

# 删除一条数据

```javascript
var Diary = Bmob.Object.extend('diary');
var query = new Bmob.Query(Diary);
// 要删除的记录的ID
var id = '4ecdf7a';

query.get(id,{
    success:function(object){
        object.destroy({
            success:function(deleteObject){
                console.log('删除成功！');
            },
            error:function(object,error){
                console.log('delete failed! error code is:' + error.code + ', error message is:' + error.message);
            }
        });
    },
    error:function(object,error){
        console.log('query failed! error code is:' + error.code + ', error message is:' + error.message);
    }
});
```

# 批量删除

```javascript
Bmob.Object.destroyAll(objects);

```

# 按条件删除

```javascript
query.destroyAll({
    success:function(object){
        ...
    },
    error:function(error){
        ...
    }
});

```

# 条件查询

```javascript
var Diary = Bmob.Object.extend('diary');
var query = new Bmob.Query(Diary);

query.equalTo('title','hello');
query.find({
    success:funciton(results){
        console.log('共查询到' + results.length + '条数据');
        for(var i = 0;i < results.length;i++){
            var obj = results[i];
            console.log(obj.id + ':' + obj.get('title'));
        }
    },
    error:function(error){
        console.log('find failed! error code is:' + error.code + ', error message is:' + error.message);
    }
})
```

# 分页查询

```javascript
// 设置起始位置
query.skip(10);
// 设置查询个数
query.limit(10);
```

# 对查询结果排序

```javascript
// 对结果按照'title'字段升序排列
query.ascending('title');

// 对结果按照'title'字段降序排列
query.descending('title');
```

# 查询某个字段是特定几种取值

```javascript
query.containedIn('title',['hello','hi','hey']);
```

# 查询指定列

```javascript
query.select('title');
query.find().then(function(results){
    ...
});
```

# 查询字符串字段以某个子串开头

```javascript
query.startsWith('title','he');
```

# 或查询

```javascript
var q1 = new Bmob.Query(Diary);
q1.greaterThan('age',10);
var q2 = new Bomb.Query(Diary);
q2.lessThan('age',20);

var mainQuery = Bmob.Query.or(q1,q2);
mainQuery.find({
    success:function(results){
        ...
    },
    error:function(error){
        ...
    }
});
```

# 查询满足条件的记录的数量

```javascript
query.count({
    success:function(count){
        console.log('共查询到了' + count + '条数据');
    },
    error:function(error){
        ...
    }
});
```

# Bmob对象的默认属性
```
obj.id
obj.createdAt
obj.updatedAt
```
# 支持的常见数据类型

```javascript
var num = 42;
var string = 'hello';
var date = new Date();
var array = [string,num];
var object = {number:num,string:string};

var bigObj = new BigObject();
bigObj.set('myNumber',num);
bigObj.set('myString',string);
bigObj.set('myDate',date);
bigObj.set('myArray',array);
bigObj.set('myObject',object);
bigObj.set('myNull',null);

bigObj.save();
```
