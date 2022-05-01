# Web Chat 项目说明

（未使用可视化界面设计软件，纯手敲的爆肝项目……）

## 运行方式

```
python main.py
```

## 主要思路

登录和注册使用数据库，用POST方法传输数据，登录后用session存储登录的用户名

浏览器发送消息时使用POST方法发送到服务端，服务端将消息接收并更新到对应的数据库。



服务端对每个已登陆的用户维护一个Dictionary，存储每个用户的消息记录中，最后更新的消息ID

比如```cache_msg_id['Alice']['Bob']==2```，代表Alice最后更新的和Bob聊天的消息记录是第2条

浏览器每隔3秒中像服务器请求验证是否有新消息，服务器对比cache_msg_id和实际消息记录数据库中的最大编号，如果有新的消息，则发送给浏览器，浏览器将新的消息显示出来。

比如服务端发现```cache_msg_id['Alice']['Bob']==2```，而读取数据库```.\msglogdb\Alice.db```中的表```Bob```时，发现有3条消息，则把第3条发送给浏览器客户端。



浏览器每隔20秒向服务器请求验证是否有新的好友添加，即Alice单方面添加了Bob好友。Bob如果此时在线，当他的浏览器向服务器发送更新好友列表的请求时，服务器会把好友Alice的信息发送给Bob，在Bob的浏览器上显示出来。

创建群组同理



群组创建后，由服务器为群组分配唯一编号。当用户请求更新消息记录时，服务器会检查用户加入的群组的消息记录，从而更新消息。

## 文件解释

**main.py**

flask服务端的主要代码，处理各种HTTP请求

**DBdebug.py**

用于调试数据库的代码（请勿运行）

**users.db**

用户数据库，存储用户列表即密码

**groups.db**

群组数据库，存储群组列表

**\groupdatas**

存储与群组相关的数据库，即群组的用户列表

**\msglogdb**

存储消息记录

用户名.db表示该用户与其他用户聊天的消息记录

Group.db表示群组的消息记录，所有用户共用。内部有多个表，每个表代表一个群组的消息记录。

**\userdatas**

用户的数据库，存储用户的好友列表，加入的群组

