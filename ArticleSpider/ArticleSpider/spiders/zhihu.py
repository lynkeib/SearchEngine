# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from decouple import config
from pymouse import PyMouse
import pickle

'''
    generate a new spider: scrapy genspider mydomain mydomain.com
'''


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    def parse(self, response):

        pass

    def start_requests(self):
        # Initiate Chrome manually
        '''
        terminal command: cd /Applications/Google\ Chrome.app/Contents/MacOS/ &Google\ Chrome --remote-debugging-port=9222
        '''

        m = PyMouse()

        chrome_option = Options()
        chrome_option.add_argument("--disable-extensions")
        chrome_option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

        browser = webdriver.Chrome(executable_path="/Users/chengyinliu/D/DevelopmentProject/chromedriver",
                                   chrome_options=chrome_option)

        # browser = webdriver.Chrome(executable_path="/Users/chengyinliu/D/DevelopmentProject/chromedriver")
        browser.get('https://www.zhihu.com/signin')
        browser.find_element_by_xpath("//div[@class='SignFlow-tab']").click()
        # browser.find_element_by_xpath("//div[@class='SignFlow-account']//input[@class='Input']").clear()

        browser.find_element_by_xpath("//div[@class='SignFlow-account']//input[@class='Input']").send_keys(
            Keys.CONTROL + 'a')

        browser.find_element_by_xpath("//div[@class='SignFlow-account']//input[@class='Input']").send_keys(
            config('ZHIHU_USERNAME'))

        browser.find_element_by_xpath("//div[@class='SignFlow-password']//input[@class='Input']").send_keys(
            Keys.CONTROL + 'a')

        browser.find_element_by_xpath("//div[@class='SignFlow-password']//input[@class='Input']").send_keys(
            config('ZHIHU_PASSWORD'))

        # browser.find_element_by_xpath(
        #     "//button[@class='Button SignFlow-submitButton Button--primary Button--blue']").click()

        loc = browser.find_element_by_xpath(
            "//button[@class='Button SignFlow-submitButton Button--primary Button--blue']").location

        m.click(loc['x'], loc['y'])

        # browser.get("https://www.zhihu.com")
        # cookies = browser.get_cookies()
        # pickle.dump(cookies, open("../../cookies/zhihu.cookie", 'wb'))
        # cookie_dict = dict()
        # for cookie in cookies:
        #     cookie_dict[cookie['name']] = cookie['value']

        return [scrapy.Request(url=self.start_urls[0], dont_filter=True, cookies=cookie_dict)]


        # browser.close()

