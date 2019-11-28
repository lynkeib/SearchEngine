# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver


class QuoraSpider(scrapy.Spider):
    name = 'quora'
    allowed_domains = ['www.quora.com']
    start_urls = ['http://www.quora.com/']

    def parse(self, response):
        pass

    def login(self):
        browser = webdriver.Chrome(executable_path="/Users/chengyinliu/D/DevelopmentProject/chromedriver")
        browser.get('https://www.quora.com/')

        browser.find_element_by_xpath("//div[@class='text header_login_text_box ignore_interaction']")[0].send_keys(
            "123456")
