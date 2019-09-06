# -*- coding: utf-8 -*-
import scrapy
import re
import json
from scrapy import Request
import time
import random
import os
import requests
from bs4 import BeautifulSoup
from ..items import LazadaGongYingItem
import pymysql
import requests


class SpiderDataSpider(scrapy.Spider):
    name = 'spider_data'
    start_urls = ['https://www.lazada.com.my/']

    def parse(self, response):
        item = LazadaGongYingItem()
        two_class_name_list_list = response.xpath('//ul[@class="lzd-site-menu-root"]/ul')

        for two_class_name_list in two_class_name_list_list:
            two_class_name_list = two_class_name_list.xpath('./li/a')

            for two_class_name_2 in two_class_name_list:
                two_class_name = two_class_name_2.xpath('./span/text()').extract()[0]
                two_class_url = two_class_name_2.xpath('./@href').extract()[0]
                two_class_url = 'https:' + two_class_url

                headers = {
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
                }
                res_text = requests.get(url=two_class_url, headers=headers).text
                json_text = re.findall('window.pageData=(.*?)</script>', res_text, re.S)[0]
                data_text = json.loads(json_text)

                title_list = data_text["mods"]["listItems"]
                for title in title_list:
                    name = title["name"]
                    item['name'] = name
                    review = title["review"]
                    item['review'] = review
                    priceShow = title["priceShow"]
                    item['priceShow'] = title["priceShow"]

                    item['two_class_name'] = two_class_name

                    print('name:', name)
                    print("review:", review)
                    print('priceShow:', priceShow)
                    print('...............................')
                    print('two_class_name:', two_class_name)
                    print('two_class_url:', two_class_url)

                    yield item





