#!/bin/usr/python3
import platform
import selenium
import time
import datetime
import sys
import argparse
import logging

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
    '20:00 - 21:00',
    '21:00 - 22:00']
timeSlice2 = [
    '06:00 - 08:00',
    '09:00 - 11:00',
    '12:00 - 14:00',
    '18:00 - 20:00']

placeMap = {
    '羽毛球正心': [12, timeSlice1, '羽毛球预约-正心楼羽毛球馆B'],
    '游泳馆': [9, timeSlice2, '游泳预约-游泳馆（4楼泳池）']
}



class Booking(object):

    def __init__(self):
        self.home_url = 'https://booking.hit.edu.cn/sport//#/'

    def start(self):
        chrome_options = Options()
        sysstr = platform.system()
        # 根据系统类型配置chrome_options
        if sysstr == "Linux":
            chrome_options.add_argument('--headless')  # 16年之后，chrome给出的解决办法，抢了PhantomJS饭碗
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')  # root用户不加这条会无法运行
            self.driver = webdriver.Chrome(chrome_options=chrome_options)
        elif sysstr == "Windows":
            chrome_options.add_argument('--no-sandbox')
            self.driver = webdriver.Chrome(chrome_options=chrome_options)
        else:
            self.driver = webdriver.Chrome(chrome_options=chrome_options)
        logger.debug("调用chrome")
        t = time.time()
        while self.home_url != self.driver.current_url:
            if time.time() - t > 10:
                logger.error('登录超时，请检查学号密码')
                return
            logger.debug("尝试登陆")
            try:
                self.login()
            except Exception as e:
                logger.debug(str(e))
                self.driver.refresh()
            time.sleep(1)

        self.Book()
        self.driver.quit()
        return

    def login(self):
        self.load_url(self.home_url)
        time.sleep(0.5)
        if self.home_url == self.driver.current_url:
            return
        self.driver.find_element_by_id("username").send_keys(args.id)
        self.driver.find_element_by_id("password").send_keys(args.pw)
        self.driver.find_element_by_id("password").send_keys(Keys.ENTER)
        time.sleep(0.5)
        if self.home_url == self.driver.current_url:
            logger.info("登陆成功")
        else:
            logger.error("登陆失败")
        return


    def Book(self):
        time.sleep(0.5)
        self.wait_and_click_path(PlacePath.format(placeMap[args.place][0]))
        logger.info("进入预约界面")
        ConfirmButton = self.wait_element_path("/html/body/div[1]/div[3]/div/div/div[3]/button")
        try:
            time.sleep(1)
            ConfirmButton.click()
        except Exception:
            self.driver.execute_script("arguments[0].scrollIntoView();", ConfirmButton)
            time.sleep(1)
            ConfirmButton.click()

        timePath = ''
        if args.today:
            logger.info("预约今日的。。。")
            timePath = timePathToday
        else:
            logger.info("预约明日的。。。")
            timePath = timePathTomorrow
        for char in args.timeFlag:
            logger.info('预约{0}的{1}'.format(placeMap[args.place][2], placeMap[args.place][1][ord(char) - ord('A')]))
            if self.BookElement(timePath.format(ord(char) - ord('A') + 1)):
                logger.info("以下是预约成功的信息：")
                logger.info('预定信息如下')
                if args.today:
                    logger.info('学号={0},场馆={1},时间段为今天的{2}'.format(args.id, placeMap[args.place][2], placeMap[args.place][1][ord(char) - ord('A')]))
                else:
                    logger.info('学号={0},场馆={1},时间段为明天的{2}'.format(args.id, placeMap[args.place][2], placeMap[args.place][1][ord(char) - ord('A')]))
                return
            time.sleep(0.5)
        logger.warning("没有可用的预约，已返回")
        return


    def BookElement(self, path):
        """
        预约具体的资源
        :param path: 资源按钮对应的Xpath
        :return:  如果预约成功，则返回True
        """
        try:
            button = self.driver.find_element_by_xpath(path)
            sub_button = self.driver.find_element_by_xpath(path + "/button[1]")
        except NoSuchElementException:
            logger.warning("Exception:预约尚未开放！")
            return

        if sub_button.get_attribute('disabled') == "true":
            logger.warning("Exception:预约失败，不在可预约时间")
            return False
        if '已满' in button.text:
            logger.warning("Exception:预约失败，目标时间已满！")
            return False

        logger.info("目标时间未满，开始预约")
        time.sleep(1)
        try:
            button.click()
        except selenium.common.exceptions.ElementNotInteractableException:
            logger.error("Error:按钮不可交互")
            return
        time.sleep(1)
        try:
            self.driver.find_element_by_xpath("/html/body/div[1]/div[4]/div/div/div[2]/div/div[2]/div[7]/div/div/div[1]/div/div").click()
        except Exception:
            logger.error("Exception:未发现checkbox")

        time.sleep(0.5)
        self.wait_and_click_path("/html/body/div[1]/div[4]/div/div/div[3]/button[2]/span")
        time.sleep(0.5)
        logger.info("预约成功！")
        time.sleep(2)
        return True


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
            if len(placeMap[args.place][1]) <= ord(char) - ord('A'):
                logger.error("当前场馆[{1}]没有时间段{0}".format(char, args.place))
                return False
        return True

    def info(self):
        logger.info('预定信息如下')
        if args.today:
            logger.info('学号={0},场馆={1},时间段为今天的：'.format(args.id, placeMap[args.place][2]))
        else:
            logger.info('学号={0},场馆={1},时间段为明天的：'.format(args.id, placeMap[args.place][2]))
        strs = []
        for char in args.timeFlag:
            strs.append(placeMap[args.place][1][ord(char) - ord('A')])
        logger.info(strs)

    def wait(self):
        logger.info('等待到下一个9点之后开始预约')
        while datetime.datetime.now().hour < 9 or datetime.datetime.now().hour >= 12:
            time.sleep(10)
        time.sleep(10)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='HIT 资源自动预约脚本')
    parser.add_argument('id', type=str, help="学号")
    parser.add_argument('pw', type=str, help="密码")
    parser.add_argument('place', type=str, choices=['游泳馆', '羽毛球正心'], help="运动场馆")
    parser.add_argument('timeFlag', type=str, help="预约时间段代号")
    parser.add_argument('-t', '--test', action="store_true", help="仅输出信息，不进行预约")
    parser.add_argument('--today', action="store_true", help="预约今天，否则都是预约明天")
    parser.add_argument('-v', '--verbose', action="store_true", help='详细输出')
    parser.add_argument('--wait', action="store_true", help='等待到下一个9点之后开始预约(12点后执行)')
    # parser.add_argument('-d', '--drv', type=str, default='', help="chromedriver路径")
    parser.add_argument('-l', '--log', type=str, default='./log.txt', help="日志文件路径")
    args = parser.parse_args()

    # 加载日志
    if 'logger' not in vars():
        logger = logging.getLogger(name='AutoBooking')
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
        # Add both handlers
        logger.addHandler(fhandler)
        logger.addHandler(chandler)
        logger.setLevel(level)
        # # Show the handlers
        # for hdr in logger.handlers:
        #     print(hdr)
        # # Log Something
        # logger.info("Test info")

    booking = Booking()
    if args.wait:
        booking.info()
        booking.wait()
    if booking.checkArgs():
        if args.test:
            booking.info()
        else:
            booking.start()
