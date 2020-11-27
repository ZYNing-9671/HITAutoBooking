# HIT 自动预约游泳馆等资源

github地址：[https://github.com/xrervip/HITAutoBooking](https://github.com/xrervip/HITAutoBooking)

**Q:如何使用此脚本？**

A:
**使用方法：**
依赖于python运行环境+chorme+selenium+ chromedriver驱动

 1. 安装Chorme浏览器
 2. 下载安装**python运行环境**+**selenium 包**+ **chromedriver驱动**    selenium可以直接可以用pip安装。`pip install selenium` 。chormedriver 镜像地址: [https://npm.taobao.org/mirrors/chromedriver/](https://npm.taobao.org/mirrors/chromedriver/) 寻找对应您的chrome浏览器的版本即可，解压后将`chromedriver.exe`文件放在chrome浏览器根目录，也就是`chrome.exe`同目录下，同时需要将该目录添加到`环境变量`里 [第二步教程](https://www.cnblogs.com/lfri/p/10542797.html)
 3. 定时（预约一般于9点开放）启动python脚本，建议于9点后数分钟内启动
 
 **参数格式：**
 

```
 统一身份认证id + 密码 + 场馆类型（游泳馆）+ 时间（早中晚）
```
**案例：**

```
1180300100 password 游泳馆 早中晚
```
就会预约游泳馆的早中晚场（默认优先晚场——中午场——早场）



 程序会默认预约明日的场次，因此第二天的预约于第一天9点开发，如果明日的场次都满，就会尝试预约今日的场次， 基于生活习惯，会以 晚-中-早的优先级进行预约
 
 ---

**Q:如何设置定时任务？**
**A**:在Linux下可以使用crontab [Linux crontab 命令]，(https://www.runoob.com/linux/linux-comm-crontab.html)
在windows操作系统下可以使用**控制面板->管理工具->任务计划程序**
下面的定时任务[windows定时任务](https://blog.csdn.net/wd2011063437/article/details/79168735)



