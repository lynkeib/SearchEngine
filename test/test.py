__author__ = 'Connor'

import re
from selenium import webdriver
#
# line = "djkhalkfskahc2019-3dbakbfkh"
#
# regex_str = '.*?((\d+).(\d+).(\d+)).*'
#
# match_obj = re.match(regex_str, line)
#
# if match_obj:
#     print('yes')
#     print(match_obj.group(1), match_obj.group(2), match_obj.group(3), match_obj.group(4))
#     print("fdsjnafkj" "fdjsnkafl")
# else:
#     print('no')


browser = webdriver.Chrome(executable_path="/Users/chengyinliu/D/DevelopmentProject/chromedriver")
browser.get('https://www.zhihu.com/signin')
browser.find_element_by_xpath("//div[@class='SignFlow-tab']").click()
browser.find_element_by_xpath("//div[@class='SignFlow-account']//input[@class='Input']").send_keys(
    "15810952153")
browser.find_element_by_xpath("//div[@class='SignFlow-password']//input[@class='Input']").send_keys("123456")

browser.find_element_by_xpath(
    "//button[@class='Button SignFlow-submitButton Button--primary Button--blue']").click()