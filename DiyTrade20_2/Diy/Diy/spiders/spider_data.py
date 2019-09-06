# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy import Request
from pyppeteer import launch
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from time import sleep


class SpiderDataSpider(scrapy.Spider):
    name = 'spider_data'
    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    # 创建一个浏览器对象
    bro = webdriver.Chrome(executable_path=r'D:\chromedriver', chrome_options=option)
    # start_urls = ['https://rarasearch.ralali.com/search?alias=q&brand_names=&category=&free_shipping=false&key_alias=&maxprice=9007199254740991&minprice=0&order=&page=1&payload=eyJ3aG9sZXNhbGVfcHJpY2VfZXhpc3QiOjEsImRpc2NvdW50X3BlcmNlbnRhZ2UiOjAuMDEsImlzX21hcmtldHBsYWNlIjotMTAsInZpcnR1YWxfYm9vc3QiOjEsImZyZWVfb25na2lyX251c2FudGFyYSI6MSwiaXNfbmVnb3RpYWJsZSI6LTEsInZlbmRvcl9zY29yZSI6MSwiZ29vZF9pbWFnZSI6MTAsImZyZWVfb25na2lyX2xva2FsIjowLjYsIml0ZW1fc29sZF9ub3JtIjoxLCJwYWdlX3ZpZXdfbm9ybSI6MX0%3D&q=headset&vendor_location=&wholesale=']

    def start_requests(self):
        url = 'https://www.ralali.com/'
        bro = self.bro
        bro.get(url=url)
        bro.find_element_by_class_name("dropdown-toggle").click()
        sleep(1)
        bro.find_element_by_link_text("Bahasa Indonesia").click()
        sleep(1)
        bro.find_element_by_xpath("/html/body/header/section/div[2]/div/div[4]/div/form/div/input").send_keys('headset')
        sleep(1)
        bro.find_element_by_class_name("btn btnSearchHome").click()







    # def parse(self, response):
    #     res_text_json = response.text
    #     res_text_data = json.loads(res_text_json)
    #     # print(res_text_data, type(res_text_data))
    #     hits_list = res_text_data.get("hits").get("hits")[0]
    #     print(hits_list)
    #     # for hits in hits_list:
    #     res_url = hits_list.get("_source").get("alias")
    #     res_url = "https://www.ralali.com/v/rantchromegarage/product/" + res_url
    #     headers = {
    #         'cookie': 'rll_grnt=7b82376c43f74900d225fdab213ab177115e78e5-10433ecc8ed7b42bef9da37454fc81ed_fcc763d11eec41950913c6e7c28eec59; _ga=GA1.2.848148245.1567129123; _gid=GA1.2.1836881632.1567129123; cto_lwid=e661febf-cb6a-41ab-beab-c551b854542e; dayOfYear=242; show_top_banner=1; _hjid=a0226024-f4ac-4f90-a629-7aef4f7b056d; _gat_UA-42713825-6=1; previous_url=eyJpdiI6Imx3c0lrWHV1UUlwOStZaGNGbUN1bmc9PSIsInZhbHVlIjoiWXRVY1JZVkZ0Ynl1ZU5wWXRWYWZjS2hOSFZ5Q1FHaWNMMUpNQXo2aEkzXC9JMStMWk5OOGY2cEwrM29aVkNodDB0YWNZSlU5cmMzRGpyV3Y1UUZxYXRWRGR2QVc5bDN3VHVcL3hFWWlpV2tzT2J1dFNhaXVkQ1dDb3hnMWpJQW8yZyIsIm1hYyI6ImRkZTIzODY1MmNmYmE5OWEwZTdjYmNhNjFkNDI4OTM2MDk5YjEzZmIwMWJmZjgzMDRjZDNiMDhhN2M1NzU0NjAifQ%3D%3D; XSRF-TOKEN=eyJpdiI6IjJQVHZKUWx1bFFpZnd5K3JTQXFSMkE9PSIsInZhbHVlIjoiUTRZR2M3XC9jOUFNV0swaGFWNkx0eUFRM2lHRzI0OHZMQWJFVG5LTWdJVHhQNmNVdlNNNHlKVkFQWHROM0R1UnBXblwva1FWVkhMRkZKVU9jWUZDa1NnUT09IiwibWFjIjoiZWYzZTBmMDQzMGJmOGQzNTg0YjBkMDE0M2U4NjcyNTc5ZDM4N2VlZjdjMThhNWQwNDFmYjk5OTkyOGEyODY1OSJ9; ralali=eyJpdiI6Imx2REhQYmlyaUFrTHppbGM0RVBuNEE9PSIsInZhbHVlIjoibFRITTk4eTlBSlwveEx1Y01zalFZaVV5UFdUenhKd2RBNW1JK3doWUkrUkNNRHl2TWpjRkNKbkw1VDU5bUhlU3I3aDNJNlwvQ0ZpMHcwV1NIZEZkTVZVZz09IiwibWFjIjoiNWU2ZDIxYTA3MGRmNWJkYWMyZjIxMWQxYTNkNmNhZjE5ZGY0NDk0MGVkMjI3YThjMWRjMmY3NDBkNGU4YTkxOCJ9; amplitude_id_2c1a3f70ab02cb610ab2905c0c4c63c6ralali.com=eyJkZXZpY2VJZCI6IjJkNDhlYTE5LWQ1MTctNDkxOC1hNTg4LTI1NDRhZTA5ZDlkNVIiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTU2NzEyOTEyMzgzNCwibGFzdEV2ZW50VGltZSI6MTU2NzEzNTE5NTUxNSwiZXZlbnRJZCI6MzMsImlkZW50aWZ5SWQiOjAsInNlcXVlbmNlTnVtYmVyIjozM30='
    #     }
    #     yield Request(url=res_url, headers=headers, callback=self.parse_detail)


    # def parse_detail(self, response):
    #     # print(response.text)
    #     with open('jj.html', 'w', encoding='utf-8') as f:
    #         f.write(response.text)




# https://www.ralali.com/v/rantchromegarage/product/ach1001-belink-wireless-bluetooth-headset-100000092720001
