# 用户接口

- ### 用户注册：

##### 1.请求URL：

- `http://api.mr-lin.site/api/user`

##### 2.请求方法：

- POST

##### 3.请求参数：

| 参数名   | 必选                 | 类型   | 说明                       |
| -------- | -------------------- | ------ | -------------------------- |
| Action   | 是，且必须为"signin" | string | 指定POST方法所要执行的动作 |
| Username | 是                   | string | 用户名                     |
| Password | 是                   | string | 密码                       |

##### 4.返回示例：

```python
{
    "status": 0,
    "message": "succeed",
    "data": {
        "username": "admin",
        "uid": 4
    }
}
```

```python
{
    "status": 1,
    "message": "username already exits",
    "data": {}
}
```



- ### 用户登录：

##### 1.请求URL：

- `http://api.mr-lin.site/api/user`

##### 2.请求方法：

- POST

##### 3.请求参数：

| 参数名   | 必选                | 类型   | 说明                       |
| -------- | ------------------- | ------ | -------------------------- |
| Action   | 是，且必须为"login" | string | 指定POST方法所要执行的动作 |
| Username | 是                  | string | 用户名                     |
| Password | 是                  | string | 密码                       |

##### 4.返回示例：

```python
{
    "status": 0,
    "message": "succeed",
    "data": {
        "username": "lin",
        "uid": 5
    }
}
```

```python
{
    "status": 1,
    "message": "wrong password",
    "data": {}
}
```

```python
{
    "status": 1,
    "message": "user do not exit",
    "data": {}
}
```



- ### 用户登出：

##### 1.请求URL：

- `http://api.mr-lin.site/api/user`

##### 2.请求方法：

- POST

##### 3.请求参数：

| 参数名 | 必选                 | 类型   | 说明                       |
| ------ | -------------------- | ------ | -------------------------- |
| Action | 是，且必须为"logout" | string | 指定POST方法所要执行的动作 |

##### 4.返回示例：

```python
{
    "status": 0,
    "message": "succeed",
    "data": {}
}
```



- ### 获取当前用户信息：

##### 1.请求URL：

- `http://api.mr-lin.site/api/user`

##### 2.请求方法：

- GET

##### 3.请求参数：

- 无

##### 4.返回示例：

```python
{
    "status": 0,
    "message": "succeed",
    "data": {
        "username": "lin",
        "uid": 5
    }
}
```

##### 5.备注：

当前必须已有用户登录，否则返回

```python
{
    "status": 0,
    "message": "login please",
    "data": {}
}
```



- ### 修改用户信息：


**简要描述：** 

- 修改用户信息

**请求URL：** 
- ` http://api.mr-lin.site/api/user/ `
  

**请求方式：**
- PUT 

**参数：** 

| 参数名   | 必选 | 类型   | 说明   |
| :------- | :--- | :----- | ------ |
| username | 否   | string | 用户名 |
| password | 否   | string | 密码   |

 **返回示例**

``` 
{
    "status": 0,
    "message": "succeed",
    "data": {
        "username": "lin",
        "uid": 5
    }
}
```


 **备注** 

- 必须登录，且修改的为当前登录用户的信息



- ### 删除用户


**简要描述：** 

- 删除用户

**请求URL：** 
- ` http://api.mr-lin.site/api/user `
  

**请求方式：**
- DELETE 

**参数：** 

无

 **返回示例**

``` 
{
    "status": 0,
    "message": "succeed",
    "data": {}
}
```


 **备注** 

- 必须登录且删除的是当前登录用户



# 任务API

- ## 一些说明：

##### 该API目前只对已注册用户提供服务，对匿名用户不开放，因此该目录下的任务API接口都只有在当前有用户登录时才可使用，否则返回：
```
{
    "status": 0,
    "message": "login please",
    "data": {}
}
```



- ## 单个任务：

- ### 获取任务

**简要描述：** 

- 获取任务

**请求URL：** 
- ` http://api.mr-lin.site/api/tasks/<int:task_id> `
  

**请求方式：**
- GET 

**参数：** 

无

 **返回示例**

``` 
{
    "status": 0,
    "message": "succeed",
    "data": {
        "timestart": "2020-03-05 23:27:31",
        "uid": 2,
        "title": "test6",
        "uri": "/api/tasks/5",
        "timeend": "2020-03-10 00:00:00",
        "content": "server_test",
        "finished": false
    }
}
```



 **备注** 

- 一些其他情况：
```
{
    "status": 1,
    "message": "该事项不存在或无权限查看",
    "data": {}
}
```



- ### 修改任务

欢迎使用ShowDoc！
    
**简要描述：** 

- 修改任务

**请求URL：** 
- ` http://api.mr-lin.site/api/tasks/<int:id> `
  

**请求方式：**
- PUT 

**参数：** 

| 参数名   | 必选 | 类型   | 说明     |
| :------- | :--- | :----- | -------- |
| title    | 否   | string | 任务概述 |
| content  | 否   | string | 详细内容 |
| finished | 否   | string | 完成状态 |
| timeend  | 否   | string | 结束时间 |

 **返回示例**

``` 
{
    "status": 0,
    "message": "succeed",
    "data": {
        "timestart": "2020-03-05 23:27:31",
        "uid": 2,
        "title": "test6",
        "uri": "/api/tasks/5",
        "timeend": "2020-03-10 00:00:00",
        "content": "server_test",
        "finished": false
    }
}
```



- ### 删除任务

**简要描述：** 

- 修改任务

**请求URL：** 
- ` http://api.mr-lin.site/api/tasks/<int:id> `
  

**请求方式：**
-DELETE 

**参数：** 

无

 **返回示例**

``` 
{
    "status": 0,
    "message": "succeed",
    "data": {}
}
```



- ## 任务清单

- ### 新建任务

**简要描述：** 

- 新建任务

**请求URL：** 
- ` http://api.mr-lin.site/api/tasks/ `
  

**请求方式：**
- POST 

**参数：** 

| 参数名  | 必选 | 类型   | 说明         |
| :------ | :--- | :----- | ------------ |
| title   | 是   | string | 任务标题     |
| content | 否   | string | 任务详细内容 |
| timeend | 是   | string | 任务截止日期 |
###### ##### 备注：timeend的格式需类似为“2020-01-01 00:00:00”这般


**返回示例：**

``` 
{
    "status": 0,
    "message": "succeed",
    "data": {
        "timestart": "2020-03-05 23:37:51",
        "uid": 2,
        "title": "test9",
        "uri": "/api/tasks/8",
        "timeend": "2020-03-10 00:00:00",
        "content": "server_test",
        "finished": false
    }
}
```



- ### 获取所有任务


**简要描述：** 

- 获取当前用户所有任务

**请求URL：** 
- ` http://api.mr-lin.site/api/tasks/?status= `
  

**请求方式：**
- GET 

**参数：** 

无

 **返回示例**

``` 
{
    "status": 0,
    "message": "succeed",
    "data": [
        {
            "timestart": "2020-03-05 23:27:31",
            "uid": 2,
            "title": "test6",
            "uri": "/api/tasks/5",
            "timeend": "2020-03-10 00:00:00",
            "content": "server_test",
            "finished": false
        },
        {
            "timestart": "2020-03-05 23:27:56",
            "uid": 2,
            "title": "test7",
            "uri": "/api/tasks/6",
            "timeend": "2020-03-10 00:00:00",
            "content": "server_test",
            "finished": false
        },
        {
            "timestart": "2020-03-05 23:27:59",
            "uid": 2,
            "title": "test8",
            "uri": "/api/tasks/7",
            "timeend": "2020-03-10 00:00:00",
            "content": "server_test",
            "finished": false
        }
    ]
}
```
<br/>
##### 备注：
- 可为请求URL添加参数 **status** 来请求指定完成状态的任务， **status** 为 **0** 请求所有<u>未完成的任务</u>，**status** 为 **1** 请求所有<u>已完成的任务</u>，不添加status参数或status参数既不为0也不为1则返回所有任务。



- ### 批量修改任务


**简要描述：** 

- 批量修改任务

**请求URL：** 
- ` http://api.mr-lin.site/api/tasks/?status= `
  

**请求方式：**
- PUT 

**参数：** 

| 参数名   | 必选 | 类型   | 说明     |
| :------- | :--- | :----- | -------- |
| title    | 否   | string | 任务概述 |
| content  | 否   | string | 详细内容 |
| finished | 否   | string | 完成状态 |
| timeend  | 否   | string | 结束时间 |

 **返回示例**

``` 
{
    "status": 0,
    "message": "succeed",
    "data": {
        "timestart": "2020-03-05 23:27:31",
        "uid": 2,
        "title": "test6",
        "uri": "/api/tasks/5",
        "timeend": "2020-03-10 00:00:00",
        "content": "server_test",
        "finished": false
    }
}
```
- 备注：该请求URL的status参数同获取任务列表的status参数相同



- ### 批量删除任务


**简要描述：** 

- 批量删除任务

**请求URL：** 
- ` http://api.mr-lin.site/api/tasks/?status= `
  

**请求方式：**
-DELETE 

**参数：** 

无

 **返回示例**

``` 
{
    "status": 0,
    "message": "succeed",
    "data": {}
}
```

- 该请求URL的status参数同获取任务清单的URL参数