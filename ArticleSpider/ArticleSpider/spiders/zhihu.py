# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    def parse(self, response):
        pass

    def start_requests(self):
        browser = webdriver.Chrome(executable_path="/Users/chengyinliu/D/DevelopmentProject/chromedriver")
        browser.get('https://www.zhihu.com/signin')
        browser.find_element_by_xpath("//div[@class='SignFlow-account']//input[@class='Input']").send_keys(
            "15810952153")
        browser.find_element_by_xpath("//div[@class='SignFlow-password']//input[@class='Input']").send_keys("123456")

        browser.find_element_by_xpath(
            "//button[@class='Button SignFlow-submitButton Button--primary Button--blue']").click()
