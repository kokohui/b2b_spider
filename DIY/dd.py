from selenium import webdriver
from time import sleep
from selenium.webdriver import ChromeOptions
import requests
from lxml import etree
import json
from bs4 import BeautifulSoup
import re
import random
import os
import pymysql
# from .pynysql_db import DataBaseHandle
from time import sleep



class spider():

    def __init__(self):
        option = ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        # 创建一个浏览器对象
        self.bro = webdriver.Chrome(executable_path=r'D:\chromedriver', chrome_options=option)
        # self.bro = webdriver.Chrome(executable_path=r'C:\谷歌selenium驱动\chromedriver', chrome_options=option)
        self.url = 'https://login.1688.com/member/signin.htm?spm=b26110380.sw1688.1.3.780e4510sQlgTW&Done=https%3A%2F%2Fs.1688.com%2Fselloffer%2Foffer_search.htm%3Fkeywords%3D%25B6%25FA%25BB%25FA%26button_click%3Dtop%26earseDirect%3Dfalse%26n%3Dy%26netType%3D1%252C11'
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
        }

    def seacch(self):
        url = 'https://www.ralali.com'
        bro = self.bro
        bro.get(url=url)
        sleep(1)
        # bro.find_element_by_class_name('dropdown').click()
        # sleep(1)
        # bro.find_element_by_class_name('linkBahasa').click()
        # sleep(1)
        bro.find_element_by_xpath('/html/body/header/section/div[2]/div/div[4]/div/form/div/input').send_keys('headset')
        sleep(1)
        bro.find_element_by_xpath('/html/body/header/section/div[2]/div/div[4]/div/form/div/span[2]').click()
        sleep(1)

        bro.find_element_by_xpath('//*[@id="menu-list"]/div[2]/div[2]/div/item[1]/div/div/article/figure/a').click()
        sleep(1)
        res_text = bro.page_source
        tree = etree.HTML(res_text)
        text = tree.xpath('//h1[@class="item-detail-name text-larger hidden-sm hidden-xs"]/text()')
        print('text:', text)




if __name__ == '__main__':
    ss = spider()
    ss.seacch()