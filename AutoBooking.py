#!/bin/usr/python3
import platform
import selenium
import time
import datetime
import sys
import argparse
import logging
import threading
import os

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException, NoSuchElementException, JavascriptException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


PlacePath = "/html/body/div[1]/div/main/div/div/div[2]/div/div[{0}]/div/div/p"
timePathToday = "/html/body/div[1]/div[1]/main/div/div/div[4]/div[1]/div[1]/div/div[2]/div[{0}]/div[3]"
timePathTomorrow = "/html/body/div[1]/div[1]/main/div/div/div[4]/div[1]/div[2]/div/div[2]/div[{0}]/div[3]"

timeSlice1 = [
    '06:00 - 07:30',
    '08:00 - 09:00',
    '09:00 - 10:00',
    '10:00 - 11:00',
    '11:00 - 12:00',
    '12:00 - 13:00',
    '13:00 - 14:00',
    '14:00 - 15:00',
    '15:00 - 16:00',
    '16:00 - 17:00',
    '17:00 - 18:00',
    '18:00 - 19:00',
    '19:00 - 20:00',
    '20:00 - 21:00']

timeSlice2 = [
    '06:00 - 08:00',
    '09:00 - 11:00',
    '12:00 - 14:00',
    '18:00 - 20:00']

timeSlice3 = [
    '06:00 - 07:00',
    '07:00 - 08:00',
    '12:00 - 13:30',
    '18:00 - 19:00',
    '19:00 - 20:00',
    '20:00 - 21:00',
    '21:00 - 22:00'
]

placeMap = {
    '羽毛球正心': [12, timeSlice1, '正心楼羽毛球馆B'],
    '羽毛球体育馆': [11, timeSlice3, '体育馆羽毛球馆'],
    '羽毛球二区': [10, timeSlice3, '羽毛球预约-二校区活动中心'],
    '游泳馆': [9, timeSlice2, '游泳馆（4楼泳池）']
}



class Booking(object):

    def __init__(self, n, handlers):
        self.n = n
        self.logger = logging.getLogger(name='AutoBooking[{0}]'.format(n))
        _level = logging.INFO
        if args.verbose:
            _level = logging.DEBUG
        for handler in handlers:
            self.logger.addHandler(handler)
        self.logger.setLevel(_level)
        self.home_url = 'https://booking.hit.edu.cn/sport//#/'

    def start(self):
        self.home_url = 'https://booking.hit.edu.cn/sport//#/'
        chrome_options = Options()
        sysstr = platform.system()
        if not args.nowait:
            self.wait()
        # 根据系统类型配置chrome_options
        if sysstr == "Linux":
            chrome_options.add_argument('--headless')  # 16年之后，chrome给出的解决办法，抢了PhantomJS饭碗
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')  # root用户不加这条会无法运行
            self.driver = webdriver.Chrome(options=chrome_options)
        elif sysstr == "Windows":
            chrome_options.add_argument('–disable-infobars')
            chrome_options.add_argument('–incognito')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('blink-settings=imagesEnabled=false')
            if not args.debug or args.headless:
                chrome_options.add_argument('--headless')
            self.driver = webdriver.Chrome(options=chrome_options)
        else:
            self.driver = webdriver.Chrome(options=chrome_options)

        self.driver.implicitly_wait(0)
        self.login()
        self.driver.implicitly_wait(0)
        self.Book()
        self.driver.quit()
        return

    def login(self):
        times = 10
        while times:
            times -= 1
            self.logger.debug('刷新浏览器')
            self.driver.refresh()
            time.sleep(0.1)

            self.logger.info('尝试登录【{0}】'.format(9 - times))
            self.load_url(self.home_url)

            self.logger.debug('等待加载登录界面')
            if self.check_element('/html/body/div[2]/div[2]/div[2]/div/div[3]/div/form/p[1]', 30):  # 登录框
                self.driver.find_element_by_id("username").send_keys(args.id)
                self.driver.find_element_by_id("password").send_keys(args.pw)
                self.driver.find_element_by_id("password").send_keys(Keys.ENTER)
            else:
                self.logger.error("加载登录登录框超时")
                continue

            self.logger.debug('等待加载https://booking.hit.edu.cn/sport//#/')
            if self.check_element('/html/body/div/div/main/div/div/div[2]/div', 30):  # 场馆表
                self.logger.info("登陆成功")
                return
            else:
                self.logger.error("加载https://booking.hit.edu.cn/sport//#/超时")
                self.logger.error("登陆失败")
                continue


    def Book(self):
        times = 10
        while times:
            times -= 1
            self.logger.debug('刷新浏览器')
            self.driver.refresh()
            time.sleep(0.1)

            self.logger.debug('等待资源预约平台')
            if self.check_element(PlacePath.format(placeMap[args.place][0]), 30):  # 场馆表
                pass
            else:
                self.logger.error("加载https://booking.hit.edu.cn/sport//#/超时")
                continue

            self.logger.debug("进入场馆")
            self.driver.find_element_by_xpath(PlacePath.format(placeMap[args.place][0])).click()

            self.logger.debug("等待温馨提示")
            if self.check_element("/html/body/div[1]/div[3]/div/div/div[3]/button", 120):  # 温馨提示的确认按钮
                pass
            else:
                self.logger.error("温馨提示超时")
                continue

            self.logger.debug("确认温馨提示")
            try:
                time.sleep(0.2)  # 这个元素加载是有一段动画的
                ConfirmButton = self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/div[3]/button")
                self.driver.execute_script("arguments[0].scrollIntoView();", ConfirmButton)
                self.driver.execute_script("arguments[0].scrollIntoView();", ConfirmButton)
                self.driver.execute_script("arguments[0].scrollIntoView();", ConfirmButton)
                self.driver.execute_script("arguments[0].scrollIntoView();", ConfirmButton)
                ConfirmButton.click()
            except Exception as e:
                self.logger.error(str(e))
                self.logger.error('“温馨提示”-确认失败')
                if args.debug:
                    with open('web[{0}][{1}].html'.format(self.n, sys._getframe().f_lineno), 'w') as f:
                        f.write(self.driver.page_source)
                return

            self.logger.debug("确认时间表已经加载")
            if self.check_element('/html/body/div/div[1]/main/div/div/div[4]/div[1]/div[1]', 30):  # 今天的时间表
                pass
            else:
                self.logger.error("时间表加载超时")
                continue

            time_path = ''
            if args.today:
                self.logger.info("预约今日的。。。")
                time_path = timePathToday
            else:
                self.logger.info("预约明日的。。。")
                time_path = timePathTomorrow
                self.logger.info("检查预约时间是否开放")
                if self.check_element('/html/body/div/div[1]/main/div/div/div[4]/div[1]/div[2]', 0.1):  # 今天的时间表
                    pass
                else:
                    self.logger.info("预约时间未开放，重新刷新")
                    times += 1
                    continue

            self.logger.info("开始预约")
            for char in args.timeFlag:
                self.logger.info('预约{0}的{1}'.format(placeMap[args.place][2], placeMap[args.place][1][ord(char) - ord('A')]))
                if self.BookElement(time_path.format(ord(char) - ord('A') + 1)):
                    self.logger.info("以下是预约成功的信息：")
                    self.logger.info('预定信息如下')
                    if args.today:
                        self.logger.info('学号={0},场馆={1},时间段为今天的{2}'.format(args.id, placeMap[args.place][2], placeMap[args.place][1][ord(char) - ord('A')]))
                    else:
                        self.logger.info('学号={0},场馆={1},时间段为明天的{2}'.format(args.id, placeMap[args.place][2], placeMap[args.place][1][ord(char) - ord('A')]))
                    return

            self.logger.warning("没有可用的预约，已返回")
            return

    def BookElement(self, path):
        """
        预约具体的资源
        :param path: 资源按钮对应的Xpath
        :return:  如果预约成功，则返回True
        """

        if not self.check_element(path, 0.01):
            self.logger.warning("Exception:预约时间安排表有变化")
            return False
        button = self.driver.find_element_by_xpath(path)
        sub_button = self.driver.find_element_by_xpath(path + "/button[1]")
        if sub_button.get_attribute('disabled') == "true":
            self.logger.warning("Exception:预约失败，不在可预约时间")
            return False
        if '已满' in button.text:
            self.logger.warning("Exception:预约失败，目标时间已满！")
            return False

        self.logger.info("目标时间未满，开始预约")

        try:
            sub_button.click()
        # except selenium.common.exceptions.ElementNotInteractableException:
        except Exception as e:
            self.logger.error(str(e))
            self.logger.error("Error:按钮不可交互")
            if args.debug:
                with open('web[{0}][{1}].html'.format(self.n, sys._getframe().f_lineno), 'w') as f:
                    f.write(self.driver.page_source)
            return False

        if '游泳馆' in placeMap[args.place][2]:
            self.logger.debug('游泳馆的checkbox')
            if self.check_element("/html/body/div[1]/div[4]/div/div/div[2]/div/div[2]/div[7]/div/div/div[1]/div/div", 5):
                checkbox = self.driver.find_element_by_xpath("/html/body/div[1]/div[4]/div/div/div[2]/div/div[2]/div[7]/div/div/div[1]/div/div")
                if '我同意' in self.driver.find_element_by_xpath('/html/body/div/div[4]/div/div/div[2]/div/div[2]/div[7]/div/div/div[1]/label').text:
                    checkbox.click()
            else:
                self.logger.error("Exception:未发现checkbox")

        if self.check_element("/html/body/div[1]/div[4]/div/div/div[3]/button[2]/span", 30):
            self.driver.find_element_by_xpath("/html/body/div[1]/div[4]/div/div/div[3]/button[2]/span").click()
            # self.wait_and_click_path("/html/body/div/div[4]/div/div/div[3]/button[2]")
        else:
            self.logger.info('预约失败')
            return False

        if self.check_element("/html/body/div/div[5]/div/div/div[1]", 60):
            text_title = self.driver.find_element_by_xpath('/html/body/div/div[5]/div/div/div[1]').text
            text = self.driver.find_element_by_xpath('/html/body/div/div[5]/div/div/div[2]').text
            self.logger.info('{0}:{1}'.format(text_title, text))
            if args.debug:
                if '由于预约过于火爆' in text:
                    with open('web[{0}][{1}].html'.format(self.n, sys._getframe().f_lineno), 'w') as f:
                        f.write(self.driver.page_source)

            if '预定成功' in text_title or '预定成功' in text:
                return True
            else:
                self.driver.find_element_by_xpath('/html/body/div/div[5]/div/div/div[3]/button').click()
                return False
        else:
            self.logger.info('预约失败')
            return False



    def wait_url(self, target_url, timeout=10.0):
        """
        等待直到url更新为目标url
        :param target_url: 预计更新后的目标url
        :param timeout: 超时时间
        :return:
        """
        while target_url != self.driver.current_url and timeout > 0:
            time.sleep(0.1)
            timeout -= 0.1
        if timeout <= 0:
            raise TimeoutException()

    def wait_url_redirect(self, origin_url, timeout=10.0):
        """
        等待直到url更新为另一个url
        :param origin_url: 更新前的url
        :param timeout: 超时时间
        :return:
        """
        while origin_url == self.driver.current_url and timeout > 0:
            time.sleep(0.1)
            timeout -= 0.1
        if timeout <= 0:
            raise TimeoutException()

    def wait_element_id(self, element_id):
        """
        等待相应id的元素加载完成
        :param element_id: 元素id
        :return: 对对应的元素
        """
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, element_id))
        )
        return element

    def wait_element_path(self, element_xpath):
        """
        等待相应xpath的元素加载完成
        :param element_xpath: 元素xpath
        :return: 对对应的元素
        """
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, element_xpath))
        )
        return element



    def wait_and_send_keys(self, element_id, keys):
        """
        等待相应id的元素加载完成后输入字符
        :param element_id: 元素id
        :param keys: 需要输入的字符
        :return:
        """
        element = self.wait_element_id(element_id)
        element.send_keys(keys)

    def wait_and_click_id(self, element_id):
        """
        等待相应id的元素加载完成后点击元素
        :param element_id: 元素id
        :return:
        """
        element = self.wait_element_id(element_id)
        element.click()
        return element

    def wait_and_click_path(self, element_path):
        """
        等待相应id的元素加载完成后点击元素
        :param element_id: 元素id
        :return:
        """
        element = self.wait_element_path(element_path)
        element.click()
        return element

    def load_url(self, url):
        self.driver.get(url)
        self.driver.implicitly_wait(5)

    def checkArgs(self):
        for char in args.timeFlag:
            if len(placeMap[args.place][1]) <= ord(char) - ord('A') or 0 > ord(char) - ord('A'):
                self.logger.error("当前场馆[{1}]没有时间段{0}".format(char, args.place))
                return False
        return True

    def info(self):
        self.logger.info('预定信息如下')
        if args.today:
            self.logger.info('学号={0},场馆={1},时间段为今天的：'.format(args.id, placeMap[args.place][2]))
        else:
            self.logger.info('学号={0},场馆={1},时间段为明天的：'.format(args.id, placeMap[args.place][2]))
        strs = []
        for char in args.timeFlag:
            strs.append(placeMap[args.place][1][ord(char) - ord('A')])
        self.logger.info(strs)

    def wait(self):
        self.logger.info('等待到下一个8:59之后开始预约')
        while True:
            hour = datetime.datetime.now().hour
            if hour >= 12:
                hour -= 24
            if hour + 0.01 * datetime.datetime.now().minute > 8.58:
                return
            time.sleep(20)

    def check_element(self, element_xpath, timeout):
        """
        检查元素是否加载成功
        :param element_xpath: 元素xpath
        :param timeout: 超时
        :return:
        """
        t = time.time()
        while True:
            try:
                self.driver.find_element_by_xpath(element_xpath)
            except Exception:
                pass
            else:
                return True
            time.sleep(0.01)
            if time.time() - t > timeout:
                return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='HIT 资源自动预约脚本')
    parser.add_argument('id', type=str, help="学号")
    parser.add_argument('pw', type=str, help="密码")
    parser.add_argument('place', type=str, choices=['游泳馆', '羽毛球正心'], help="运动场馆")
    parser.add_argument('timeFlag', type=str, help="预约时间段代号")
    parser.add_argument('-t', '--test', action="store_true", help="仅输出信息，不进行预约")
    parser.add_argument('--today', action="store_true", help="预约今天，否则都是预约明天")
    parser.add_argument('-v', '--verbose', action="store_true", help='详细输出')
    parser.add_argument('-l', '--log', type=str, default='./log.txt', help="日志文件路径")
    parser.add_argument('--threads', type=int, default=1, help="并行线程数")
    parser.add_argument('--debug', action="store_true", help='debug flag')
    parser.add_argument('--headless', action="store_true", help='debug flag')
    parser.add_argument('--nowait', action="store_true", help='debug flag')
    args = parser.parse_args()

    # 加载日志
    level = logging.INFO
    if args.verbose:
        level = logging.DEBUG
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # Setup file handler
    fhandler = logging.FileHandler(args.log)
    fhandler.setLevel(level)
    fhandler.setFormatter(formatter)
    # Configure stream handler for the cells
    chandler = logging.StreamHandler()
    chandler.setLevel(level)
    chandler.setFormatter(formatter)

    def run(n):
        booking = Booking(n, [fhandler, chandler])
        if booking.checkArgs():
            booking.info()
            booking.start()

    booking_threads = []
    for i in range(args.threads):
        booking_threads.append(threading.Thread(target=run, args=(i,)))

    for i in range(args.threads):
        booking_threads[i].start()

    for i in range(args.threads):
        booking_threads[i].join()

    if not args.debug:
        if platform.system() == "Windows":
            os.system('taskkill /im chromedriver.exe /F')
            os.system('taskkill /im chrome.exe /F')
