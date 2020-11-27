# HIT 自动预约游泳馆等资源
Q:如何使用此脚本？

A:
**使用方法：**
依赖于python运行环境+chorme+selenium chromedriver驱动

 1. 安装Chorme浏览器
 2. 下载安装**python运行环境**+**selenium 包**+ **chromedriver驱动**    selenium可以直接可以用pip安装。`pip install selenium` 。chormedriver 镜像地址: [https://npm.taobao.org/mirrors/chromedriver/](https://npm.taobao.org/mirrors/chromedriver/) 寻找对应您的chrome浏览器的版本即可，解压后将`chromedriver.exe`文件放在chrome浏览器根目录，也就是`chrome.exe`同目录下，同时需要将该目录添加到`环境变量`里 [第二步教程](https://www.cnblogs.com/lfri/p/10542797.html)
 3. 定时（预约一般于9点开放）启动python脚本
 
 **参数格式：**
 
 **id+密码+场馆类型（游泳馆）+时间（早中晚）**
 程序会默认预约明日的场次，如果明日的场次都满，就会尝试预约今日的场次
 基于生活习惯，会以 晚-中-早的优先级进行预约
 

