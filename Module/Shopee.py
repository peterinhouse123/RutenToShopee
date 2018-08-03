from selenium import webdriver
import time
import os
import json
import requests
from Module import net_fn

class Shopee:

    def __init__(self,Root_Dir="",Cookie_Path=""):
        self.web = None
        self.Root_Dir = Root_Dir
        self.Cookie_Path = Cookie_Path
        self.Net = net_fn.Net()
        self.Cookie_Data = self.Loading_Cookie()


    def Loading_Cookie(self):
        fp = open(self.Cookie_Path,'r')
        Cookie_Str = fp.read()
        fp.close()
        Cookie_JSON = json.loads(Cookie_Str)

        jar = requests.cookies.RequestsCookieJar()

        for item in Cookie_JSON:

            jar.set(item['name'], item['value'], domain=item['domain'], path=item['path'])

        return jar

    def Get_Product_List(self,Cookie_Data,Page_Number=0):
        Start_Offset = 24 * Page_Number
        header = "Host: seller.shopee.tw###Connection: keep-alive###Accept: application/json, text/javascript, */*; q=0.01###User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36###Referer: https://seller.shopee.tw/portal/product/list/all###Accept-Encoding: gzip, deflate, br###Accept-Language: zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        url = "https://seller.shopee.tw/api/v2/products/?limit=24&offset="+format(Start_Offset)+"&order=list_time_dsc&search=&type=&SPC_CDS_VER=2"
        rs = self.Net.Get(header_string=header,url=url,cookie=Cookie_Data)
        data = rs.content.decode()
        return data

    def Shopee_Login_By_Cookie(self,Cookie_Data):
        url = "https://seller.shopee.tw/"

        rs = self.Net.Get(url=url,cookie=Cookie_Data)
        data = rs.content.decode()
        print(data)





    def Shopee_Login_Selenium(self,account,password):
        if self.web == None:
            self.Init_Browser()
        self.web.get("https://seller.shopee.tw/account/signin")

        # self.web = webdriver.Chrome()


        time.sleep(1)
        self.web.find_element_by_css_selector("#ember616").send_keys(account)
        self.web.find_element_by_css_selector("#ember618").send_keys(password)
        self.web.find_element_by_css_selector("#ember628").click()

        #等待驗証簡訊
        while self.web.current_url != "https://seller.shopee.tw/":

            time.sleep(0.2)

        cookies = self.web.get_cookies()

        json_cookie = json.dumps(cookies)
        fp = open("login_cookie.cok",'w+')
        fp.write(json_cookie)
        fp.close()


    def Init_Browser(self):

        Chrome_Path = self.Root_Dir + "Tool/chromedriver.exe"
        chrome_options = webdriver.ChromeOptions()

        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--mute-audio")

        self.web = webdriver.Chrome(chrome_options=chrome_options, executable_path=Chrome_Path)
        return self.web


if __name__ == '__main__':
    obj = Shopee(Root_Dir="../",Cookie_Path="login_cookie.cok")
    obj.Get_Product_List(obj.Cookie_Data)
