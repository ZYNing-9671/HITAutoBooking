
import platform

from selenium import webdriver
import time

from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException, NoSuchElementException,JavascriptException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import sys

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

PlacePath={'游泳馆': "/html/body/div[1]/div/main/div/div/div[2]/div/div[6]/div/div/p",
           '正心楼乒乓球馆B': "/html/body/div[1]/div/main/div/div/div[2]/div/div[1]/div/div/p"}
timePathToday={'早': "/html/body/div[1]/div[1]/main/div/div/div[4]/div[1]/div[1]/div/div[2]/div[1]/div[3]",
          '上': "/html/body/div[1]/div[1]/main/div/div/div[4]/div[1]/div[1]/div/div[2]/div[2]/div[3]",
          '中':"/html/body/div[1]/div[1]/main/div/div/div[4]/div[1]/div[1]/div/div[2]/div[3]/div[3]",
          '晚':"/html/body/div[1]/div[1]/main/div/div/div[4]/div[1]/div[1]/div/div[2]/div[4]/div[3]"}
timePathTomorrow={'早': "/html/body/div[1]/div[1]/main/div/div/div[4]/div[1]/div[2]/div/div[2]/div[1]/div[3]",
          '上':"/html/body/div[1]/div[1]/main/div/div/div[4]/div[1]/div[2]/div/div[2]/div[2]/div[3]",
          '中':"/html/body/div[1]/div[1]/main/div/div/div[4]/div[1]/div[2]/div/div[2]/div[3]/div[3]",
          '晚':"/html/body/div[1]/div[1]/main/div/div/div[4]/div[1]/div[2]/div/div[2]/div[4]/div[3]"}

class Booking(object):

    def __init__(self,kindPath,timeChoice):
        self.kindPath = kindPath
        self.timeChoice= timeChoice
        self.user_id = id
        self.password = Password
        self.home_url = 'https://booking.hit.edu.cn/sport//#/'

        chrome_options = Options()
        sysstr = platform.system()
        #根据系统类型配置chrome_options
        if (sysstr == "Linux"):
            chrome_options.add_argument('--headless')  # 16年之后，chrome给出的解决办法，抢了PhantomJS饭碗
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')  # root用户不加这条会无法运行
            self.driver = webdriver.Chrome(chrome_options=chrome_options)
        else:
            self.driver = webdriver.Chrome(chrome_options=chrome_options)

        self.log("调用chrome")
        while self.home_url != self.driver.current_url:
            self.log("尝试登陆")
            try:
                self.login()
            except Exception as e:
                print(str(e))
                Booking.log(str(e))
                self.driver.refresh()
            time.sleep(0.5)

        self.Book()
        self.log("------------")
        self.driver.quit()
        return

    def login(self):
        self.load_url(self.home_url)
        time.sleep(0.5)
        if self.home_url == self.driver.current_url:
            return
        self.driver.find_element_by_id("username").send_keys(id)
        self.driver.find_element_by_id("password").send_keys(Password)
        self.driver.find_element_by_id("password").send_keys(Keys.ENTER)
        time.sleep(0.5)
        if 'https://booking.hit.edu.cn/sport//#/' == self.driver.current_url:
            self.log("登陆成功")
        else:
            self.log("登陆失败")
        return


    def Book(self):

        time.sleep(0.5)
        self.wait_and_click_path(self.kindPath)
        self.log("进入预约界面")
        ConfirmButton = self.wait_element_path("/html/body/div[1]/div[3]/div/div/div[3]/button")
        try:
            time.sleep(1)
            ConfirmButton.click()
        except Exception:
            self.driver.execute_script("arguments[0].scrollIntoView();", ConfirmButton)
            time.sleep(1)
            ConfirmButton.click()

        if '晚' in self.timeChoice:
            self.log("尝试预约：明日晚")
            if self.BookElement(timePathTomorrow.get('晚')):
                return

        time.sleep(0.5)

        if '中' in self.timeChoice:
            self.log("尝试预约：明日中")
            if self.BookElement(timePathTomorrow.get('中')):
                return

        time.sleep(0.5)

        if '上' in self.timeChoice:
            self.log("尝试预约：明日上")
            if self.BookElement(timePathTomorrow.get('上')):
                return

        time.sleep(0.5)

        if '早' in self.timeChoice:
            self.log("尝试预约：明日早")
            if self.BookElement(timePathTomorrow.get('早')):
                return

        time.sleep(0.5)

        if '晚' in self.timeChoice:
            self.log("尝试预约：今日晚")
            if self.BookElement(timePathToday.get('晚')):
                return

        time.sleep(0.5)

        if '中' in self.timeChoice:
            self.log("尝试预约：今日中")
            if self.BookElement(timePathToday.get('中')):
                return

        time.sleep(0.5)

        if '上' in self.timeChoice:
            self.log("尝试预约：今日上")
            if self.BookElement(timePathToday.get('上')):
                return

        time.sleep(0.5)

        if '早' in self.timeChoice:
            self.log("尝试预约：今日早")
            if self.BookElement(timePathToday.get('早')):
                return

        time.sleep(0.5)


        self.log("没有可用的预约，已返回")
        return


    def BookElement(self,path):
        """
        预约具体的资源
        :param path: 资源按钮对应的Xpath
        :return:  如果预约成功，则返回True
        """
        try:
            button = self.driver.find_element_by_xpath(path)
        except NoSuchElementException:
            self.log("预约尚未开放！")
            return

        if '已满' in button.text:
            self.log("预约失败，目标时间已满！")
            return False
        self.log("目标时间未满，开始预约")
        time.sleep(1)
        button.click()
        time.sleep(1)
        try:
            self.log("寻找checkbox")
            self.driver.find_element_by_xpath("/html/body/div[1]/div[4]/div/div/div[2]/div/div[2]/div[7]/div/div/div[1]/div/div").click()
        except Exception:
            self.log("未发现checkbox")

        time.sleep(0.5)
        self.wait_and_click_path("/html/body/div[1]/div[4]/div/div/div[3]/button[2]/span")
        time.sleep(0.5)
        self.log("预约成功！")
        time.sleep(0.5)
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

    def log(self,msg):
        print(id+" "+msg)
        f.write(id)
        f.write(time.strftime(" %Y-%m-%d %H:%M:%S ", time.localtime(time.time())))
        f.write(msg+"\n")



if __name__ == '__main__':
    id=""
    Password=""
    f = open('log', 'a')
    if len(sys.argv)==5:
        id=sys.argv[1]
        Password=sys.argv[2]
        timeChoice = sys.argv[4]
        if(not ('早' in timeChoice or '中' in timeChoice or '晚' in timeChoice )):
            print("参数错误，请设置预约时间 早/中/晚")
            sys.exit(0)

        if(PlacePath.get(sys.argv[3]) != None):
            r = Booking(PlacePath.get(sys.argv[3]), sys.argv[4])
        else:
            print("参数错误，场馆未找到")
        sys.exit(0)
    else:
        print("参数格式错误：id+密码+场馆类型（游泳馆）+时间（早中晚）")



