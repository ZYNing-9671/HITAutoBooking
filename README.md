# HIT 自动预约游泳馆等资源

github地址：[https://github.com/xrervip/HITAutoBooking](https://github.com/xrervip/HITAutoBooking)

## 如何使用

依赖于python运行环境+chorme+selenium+ chromedriver驱动

 1. 安装**python3**，并：

    ```
    pip install selenium argparse logging
    ```

 2. 安装**Chorme**浏览器

 3. 下载安装**chromedriver**并添加到Path。chormedriver 镜像地址: [https://npm.taobao.org/mirrors/chromedriver/](https://npm.taobao.org/mirrors/chromedriver/) 

 4. 定时启动python脚本

 **参数格式：**


```
usage: AutoBooking.py [-h] [-t] [--today] [-v] [-l LOG] [--threads THREADS] [--debug] [--headless] [--nowait] id pw {游泳馆,羽毛球正心} timeFlag

HIT 资源自动预约脚本

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
  -l LOG, --log LOG  日志文件路径
  --threads THREADS  并行线程数
  --debug            debug flag
  --headless         debug flag
  --nowait           debug flag
```
**时间段代号**

A\B\C\D 对应预约界面时间段的第1\2\3\4段，比如A对应游泳馆的06:00 - 08:00时间段，在前的代号会被优先预约

**案例：**

```
python3 AutoBooking.py 21S123456 passwd 羽毛球正心 EABCD
```
## 开源许可证

**AGPL-3.0**

简单来说，建议您做到以下几点：

- 任何基于或与本项目有间接接触的项目均使用AGPL-3.0协议
- 当你使用本项目或对其修改时，如果你所服务的对象向您索要源代码，请不要拒绝
- 请不要将本项目用于商业用途

## 免责声明

本项目仅供学习交流，严禁用于商业用途，按照**LICENSE**，开发者不对本工具的使用负责。

