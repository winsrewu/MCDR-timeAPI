TimeApi
-------

一个为了让大伙知道服务器时间的东西
注意！目前这个东西还在开发，BUG和漏洞不可避免！

# 指令说明
这些指令默认只适用于Helper权限及以上！

!!Time 获取帮助文档

!!Time reget 重新获得时间戳

!!Time startServer 重新启动WebServer

!!Time info 获取时间戳

# 请求Api返回格式
默认的端口是38899（可以在Config文件处修改，默认路径config/time_api/config.json）

返回的是一串Json，就像这个：

{"day":43,"daytime":18409,"realTime":"2022-10-02 23:34:31"}

day：当前天数；daytime：当前一天的第几个gt；realTime：之前两个时间所对应的现实时间（是服务器所在的计算机时间哦）

# 开始前准备工作
flask
flask_cors
flask_limiter
werkzeug

这几个库要装好

还有，要配置好RCON，去看MCDR文档

# 最后
祝你好运！

# 还有一件事
1.这个东西默认每个ip每分钟只能访问6次

2.前端自己写去

3.“startServer”指令会导致一些奇奇怪怪的错误，但是重启服务器一般可以解决 所以除非访问不了，别用这个

4.时间戳保存在config/time_api/time.json

5.记得开防火墙

6.cloudflare tunnel的不错，可以拿来当这个的内网穿透

7.README里没提到的就去看源码罢（悲
