# HIT 自动预约游泳馆等资源

github地址：[https://github.com/xrervip/HITAutoBooking](https://github.com/xrervip/HITAutoBooking)

**Q:如何使用此脚本？**

A:
**使用方法：**
依赖于python运行环境+chorme+selenium+ chromedriver驱动

 1. 安装**python运行环境**，并：

    ```
    pip install selenium argparse logging
    ```

 2. 安装Chorme浏览器

 3. 下载安装**chromedriver驱动**。chormedriver 镜像地址: [https://npm.taobao.org/mirrors/chromedriver/](https://npm.taobao.org/mirrors/chromedriver/) 寻找对应您的chrome浏览器的版本即可，解压后将`chromedriver.exe`文件放在chrome浏览器根目录，也就是`chrome.exe`同目录下，同时需要将该目录添加到`环境变量`里 [第二步教程](https://www.cnblogs.com/lfri/p/10542797.html)

 4. 定时（预约一般于9点开放）启动python脚本，建议于9点后数分钟内启动

 **参数格式：**


```
usage: AutoBooking.py [-h] [-t] [--today] [-v] [--wait] [-d DRV] [-l LOG] id pw {游泳馆,羽毛球正心} timeFlag

HIT 自动预约脚本

positional arguments:
  id                 学号
  pw                 密码
  {游泳馆,羽毛球正心}        运动场馆
  timeFlag           预约时间段代号

optional arguments:
  -h, --help         show this help message and exit
  -t, --test         仅输出信息，不进行预约
  --today            预约今天，否则都是预约明天
  -v, --verbose      详细输出
  --wait             等待到下一个9点之后开始预约(12点后执行)
  -l LOG, --log LOG  日志文件路径
```
**时间段代号**

A\B\C\D 对应预约界面时间段的第1\2\3\4段，比如A对应游泳馆的06:00 - 08:00时间段，在前的代号会被优先预约

**案例：**

```
python3 AutoBooking.py 21S123456 passwd 羽毛球正心 EABCD
```
---

**Q:如何设置定时任务？**
**A**:在Linux下可以使用crontab [Linux crontab 命令]，(https://www.runoob.com/linux/linux-comm-crontab.html)
在windows操作系统下可以使用**控制面板->管理工具->任务计划程序**
下面的定时任务[windows定时任务](https://blog.csdn.net/wd2011063437/article/details/79168735)



