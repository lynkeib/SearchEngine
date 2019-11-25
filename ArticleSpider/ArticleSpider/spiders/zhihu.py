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
        browser.find_element_by_css_selector("")
