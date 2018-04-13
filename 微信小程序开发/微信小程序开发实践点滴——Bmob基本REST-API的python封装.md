> Bmob后端云REST API接口文档：http://docs.bmob.cn/data/Restful/a_faststart/doc/index.html

本文使用python对Bmob REST API的基本增删改查接口进行封装，方便在小程序开发时批量插入原始数据。

# 常用操作函数封装

```python
#!/usr/bin/python
# coding:utf-8
# Bmob后端云基本REST API封装
import requests
import json

# 每个应用都会有这两个ID，以下方法如果不传入这两个参数，那么使用这里默认的值
APP_ID = 'XXX'
REST_API_KEY = 'XXX'

# 封装rest api的get方法，根据对象ID获取一条数据
# table_name：要查询的表名
# object_id：要查询的数据记录的ID
def query(table_name,object_id,app_id = APP_ID,rest_api_key = REST_API_KEY):
    # 构建请求头
    headers = {}
    headers['X-Bmob-Application-Id'] = app_id
    headers['X-Bmob-REST-API-Key'] = rest_api_key

    # 构建url
    url = 'https://api.bmob.cn/1/classes/{table_name}/{object_id}'.format(table_name = table_name,object_id = object_id)

    # 发起请求
    resp = requests.get(url,headers = headers,verify = False)
    
    # 设置响应体编码
    resp.encoding = 'utf-8'
    
    if resp and resp.status_code == 200:
        return json.loads(resp.text)
    return None

# 封装rest api的post方法，插入一条记录
# table_name：表名，如果表名还不存在，则先创建一个表再插入数据
# data：字典，要插入的记录的各个字段的字段名和值
def insert(table_name,data,app_id = APP_ID,rest_api_key = REST_API_KEY):
    # 构建请求头
    headers = {}
    headers['X-Bmob-Application-Id'] = app_id
    headers['X-Bmob-REST-API-Key'] = rest_api_key
    headers['Content-Type'] = 'application/json'

    # 构建url
    url = 'https://api.bmob.cn/1/classes/{table_name}'.format(table_name = table_name)

    # 发起请求
    resp = requests.post(url,headers = headers,data = json.dumps(data),verify = False)
    
    # 设置响应体编码
    resp.encoding = 'utf-8'
    
    if resp and resp.status_code == 201:
        print 'insert success!'
        return json.loads(resp.text)
    return None

# 封装rest api的put方法,传入记录ID，修改一条数据
# table_name：要更新的表名
# object_id：要更新的数据记录的ID
# data：字典类型，要更新的数据的键值对
def update(table_name,object_id,data,app_id = APP_ID,rest_api_key = REST_API_KEY):
    # 构建请求头
    headers = {}
    headers['X-Bmob-Application-Id'] = app_id
    headers['X-Bmob-REST-API-Key'] = rest_api_key
    headers['Content-Type'] = 'application/json'

    # 构建url
    url = 'https://api.bmob.cn/1/classes/{table_name}/{object_id}'.format(table_name = table_name,object_id = object_id)

    # 发起请求
    resp = requests.put(url,headers = headers,data = json.dumps(data),verify = False)
    
    # 设置响应体编码
    resp.encoding = 'utf-8'
    
    if resp and resp.status_code == 200:
        print 'update {0} success!'.format(object_id)
        return json.loads(resp.text)
    return None


# 封装rest api的delete方法，根据对象ID删除一条记录
# table_name：要删除的记录所在的表名
# object_id：要删除的数据记录的ID
def delete(table_name,object_id,app_id = APP_ID,rest_api_key = REST_API_KEY):
    # 构建请求头
    headers = {}
    headers['X-Bmob-Application-Id'] = app_id
    headers['X-Bmob-REST-API-Key'] = rest_api_key

    # 构建url
    url = 'https://api.bmob.cn/1/classes/{table_name}/{object_id}'.format(table_name = table_name,object_id = object_id)

    # 发起请求
    resp = requests.delete(url,headers = headers,verify = False)
    
    # 设置响应体编码
    resp.encoding = 'utf-8'
    
    if resp and resp.status_code == 200:
        print 'delete {0} success!'.format(object_id)
        return json.loads(resp.text)
    return None

# 查询一个表中的所有数据
# table_name：要查询的表名
def list(table_name,app_id = APP_ID,rest_api_key = REST_API_KEY):
    # 构建请求头
    headers = {}
    headers['X-Bmob-Application-Id'] = app_id
    headers['X-Bmob-REST-API-Key'] = rest_api_key

    # 构建url
    url = 'https://api.bmob.cn/1/classes/{table_name}'.format(table_name = table_name)

    # 发起请求
    resp = requests.get(url,headers = headers,verify = False)
    
    # 设置响应体编码
    resp.encoding = 'utf-8'
    
    if resp and resp.status_code == 200:
        return json.loads(resp.text)['results']
    return None

# 批量操作：批量创建
# request_data结构：
'''
table_name = 'test'
{
    "requests":[
        {
            "method":"POST",
            "path":"/1/classes/{0}".format(table_name),
            "body":{
                "name":"Tom",
                "age":18
            }
        },
        {
            "method":"POST",
            "path":"/1/classes/{0}".format(table_name),
            "body":{
                "name":"John",
                "age":21
            }
        }
    ]
}

'''
def batch_insert(request_data,app_id = APP_ID,rest_api_key = REST_API_KEY):
    # 构建请求头
    headers = {}
    headers['X-Bmob-Application-Id'] = app_id
    headers['X-Bmob-REST-API-Key'] = rest_api_key
    headers['Content-Type'] = 'application/json'

    # url
    url = 'https://api.bmob.cn/1/batch'

    # 发起请求
    resp = requests.post(url,data = json.dumps(request_data),headers = headers,verify = False)
    
    # 设置响应体编码
    resp.encoding = 'utf-8'
    
    if resp and resp.status_code == 200:
        return json.loads(resp.text)
    return None
```

# 调用示例
```python
#!/usr/bin/python
# coding:utf-8
# 测试工具方法的使用
import bmob_base_utils as utils

def main():
    # 测试query方法
    #resp = utils.query(table_name = 'monthly', object_id = '2290ce60cc')
    #print resp

    # 测试insert方法
    '''
    data = {'name':'Ben','age':18}
    resp = utils.insert(table_name = 'test',data = data)
    print resp
    '''

    # 测试update方法
    #data = {'age':999}
    #utils.update(table_name = 'test',object_id = '79cfd8639b',data = data)

    # 测试delete方法
    #utils.delete(table_name = 'test', object_id = '79cfd8639b')

    # 测试list方法
    # print utils.list('test')

    # 测试batch_insert方法
    request_data = {}
    request_data['requests'] = []
    
    table_name = 'test'
    data1 = {
        "method":"POST",
        "path":"/1/classes/{0}".format(table_name),
        "body":{
            "name":"Tom",
            "age":18
        }
    }
    data2 = {
        "method":"POST",
        "path":"/1/classes/{0}".format(table_name),
        "body":{
            "name":"John",
            "age":21
        }
    }

    request_data['requests'].append(data1)
    request_data['requests'].append(data2)

    utils.batch_insert(request_data)


if __name__ == '__main__':
    main()

```

# 补充
* 查询成功响应：200 OK
* 创建成功响应：201 Created
* 更新成功响应：200 OK
* 删除成功响应：200 OK
