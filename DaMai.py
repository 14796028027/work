

from selenium.webdriver import Chrome,ChromeOptions
from selenium.webdriver.common.by import By
# from seleniumwire.webdriver import Chrome,ChromeOptions
import os,time,pickle


# 大麦网首页
damai_url = "https://www.damai.cn/"

#登录
login_url = "https://passport.damai.cn/login?ru=https%3A%2F%2Fwww.damai.cn%2F"

#抢票页面
target_url = "https://detail.damai.cn/item.htm?spm=a2oeg.search_category.0.0.4c064d15k2QIot&id=714876827958&clicktitle=%E3%80%8C%E4%B9%90%E8%85%BE%E6%BC%94%E8%89%BA%C2%B7%E7%B2%A4%E8%AF%AD%E9%9F%B3%E4%B9%90%E8%AE%A1%E5%88%92%E3%80%8D%20%E5%86%9C%E5%A4%AB%E5%98%BB%E5%93%88%E5%98%BB%E5%98%BB%E5%93%88%E5%93%88%E6%BC%94%E5%94%B1%E4%BC%9A"


#请求头w3
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"



class Connet:
    def __init__(self):
        self.start = 0  #表示执行到哪个步骤
        self.login_method = 1  #{ 0 : 模拟登录 , 1 : cookie登录}
        #浏览器配置
        self.options = ChromeOptions()
        #添加请求头
        self.options.add_argument("User-Agent=%s" % user_agent)
        #s设置开发者模式防止被识别
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option("useAutomationExtension", False)
        #添加代理
        # PROXY = "182.91.12.22:8085"
        # self.options.add_argument('--proxy-server=http://%s'%PROXY)
            #创建浏览器对象
        self.driver = Chrome(chrome_options=self.options)
        self.driver.maximize_window()
        #隐藏seleium
        with open('./stealth.min.js') as f:
            js = f.read()

        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": js,
        })


    def set_cookies(self):
        self.driver.get(login_url)
        print("模拟登录")
        time.sleep(20)
        print("模拟登录成功")
        #保存cookie
        pickle.dump(self.driver.get_cookies(),open("cookies.pkl","wb"))
        print("cookies:")
        print(self.driver.get_cookies())
        #抢票
        self.driver.get(target_url)


    def get_cookies(self):
        cookies = pickle.load(open("cookies.pkl",'rb'))
        for cookie in cookies:
            cookie_dict = {
                'domain':'.damai.cn',
                'name':cookie.get('name'),
                'value':cookie.get('value')
            }
            self.driver.add_cookie(cookie_dict)



    """登录"""
    def login(self):
        if self.login_method == 0:
            self.driver.get(login_url)
        elif self.login_method == 1:
            if not os.path.exists("cookies.pkl"):
                self.set_cookies()
            else:
                self.driver.get(target_url)
                self.get_cookies()


    """打开浏览器"""
    def enter_concert(self):
        print("打开浏览器")
        self.login()
        self.driver.refresh()
        self.start = 2


    '''抢票'''
    def choose_ticket(self):
        print("="*30)
        while True:
            #点击 + 号
            add = self.driver.find_element(by=By.XPATH,
                                             value="/html/body/div[2]/div/div[1]/div[1]/div/div[2]/div[3]/div[6]/div[2]/div/div/a[2]"
                                             )

            # 点击立即购买
            bybut = self.driver.find_element(by=By.XPATH,
                                             value="/html/body/div[2]/div/div[1]/div[1]/div/div[2]/div[3]/div[10]/div/div[3]/div[3]"
                                             )

            not_bybut = self.driver.find_element(by = By.XPATH,
                                     value="/html/body/div[2]/div/div[1]/div[1]/div/div[2]/div[3]/div[8]/div"
                                     )
            if not_bybut.text == "提交缺货登记":
                self.driver.refresh()
            elif bybut.text == "不，立即购买":
                add.click()
                bybut.click()
                self.start = 5
                time.sleep(1)
                break
            elif not_bybut.text == "选座购买":
                bybut.click()
                self.start = 5
                break
            else:
                self.start = 4
                self.driver.refresh()


    '''下单'''
    def buy_ticket(self):

        time.sleep(1.5)
        self.driver.execute_script('window.scrollTo(0,700)')
        choose_rem1 = self.driver.find_element(by=By.XPATH,
                                             value='//*[@id="dmViewerBlock_DmViewerBlock"]/div[2]/div/div[1]/div[3]/i'
                                               )
        choose_rem1.click()

        choose_rem2 = self.driver.find_element(by=By.XPATH,
                                             value='//*[@id="dmViewerBlock_DmViewerBlock"]/div[2]/div/div[2]/div[3]/i'
                                               )

        choose_rem2.click()

        pay = self.driver.find_element(by=By.XPATH,
                                             value='//*[@id="dmOrderSubmitBlock_DmOrderSubmitBlock"]/div[2]/div/div[2]/div[3]/div[2]/span'
                                       )
        pay.click()
        time.sleep(30)

if __name__ == "__main__":
    con = Connet()
    con.login()
    con.choose_ticket()
    con.buy_ticket()