# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy import Request
import re
from ..items import DiyItem
import random
import time
import requests
import os
import pymysql

conn = pymysql.connect(host='192.168.1.210', user='root', passwd='zhangxing888', db='ktcx_buschance', port=3306,
                       charset='utf8')

cur = conn.cursor()  # 获取一个游标


class SpiderDataSpider(scrapy.Spider):
    name = 'spider_data'

    def start_requests(self):
        item = DiyItem()
        sql_id = "SELECT url, id FROM bus_spider_data WHERE source = 'Ralali' and   TYPE = 'gongying' AND is_del = '0' AND isuse = '0' ORDER BY create_date LIMIT 1 "
        cur.execute(sql_id)
        res_all_list = cur.fetchall()
        url = res_all_list[0][0]
        spdier_data_id = res_all_list[0][-1]
        item['spdier_data_id'] = spdier_data_id
        for num in range(1, 3):
            url_2 = 'https://rarasearch.ralali.com/search?alias=q&brand_names=&category=&free_shipping=false&key_alias=&maxprice=9007199254740991&minprice=0&order=&page={}&payload=eyJ3aG9sZXNhbGVfcHJpY2VfZXhpc3QiOjEsImRpc2NvdW50X3BlcmNlbnRhZ2UiOjAuMDEsImlzX21hcmtldHBsYWNlIjotMTAsInZpcnR1YWxfYm9vc3QiOjEsImZyZWVfb25na2lyX251c2FudGFyYSI6MSwiaXNfbmVnb3RpYWJsZSI6LTEsInZlbmRvcl9zY29yZSI6MSwiZ29vZF9pbWFnZSI6MTAsImZyZWVfb25na2lyX2xva2FsIjowLjYsIml0ZW1fc29sZF9ub3JtIjoxLCJwYWdlX3ZpZXdfbm9ybSI6MX0%3D&q={}&vendor_location=&wholesale='.format(num, url)
            print(url_2)
            yield Request(url=url_2, callback=self.parse, meta={"item": item})

    def parse(self, response):
        item = response.meta["item"]
        res_text_json = response.text
        res_text_data = json.loads(res_text_json)
        hits_list = res_text_data.get("hits").get("hits")
        # print(hits_list)
        for hits in hits_list:
            res_url_1 = hits.get("_source").get("alias")
            res_url = "https://www.ralali.com/v/rantchromegarage/product/" + res_url_1
            headers = {
                ':path': '/v/mahkotaparts/product/{}'.format(res_url_1),
                'referer': 'https://www.ralali.com/v/mahkotaparts/product/{}'.format(res_url_1),
                'cookie': 'rll_grnt=7b82376c43f74900d225fdab213ab177115e78e5-10433ecc8ed7b42bef9da37454fc81ed_fcc763d11eec41950913c6e7c28eec59; _ga=GA1.2.848148245.1567129123; _gid=GA1.2.1836881632.1567129123; cto_lwid=e661febf-cb6a-41ab-beab-c551b854542e; dayOfYear=242; show_top_banner=1; _hjid=a0226024-f4ac-4f90-a629-7aef4f7b056d; _gat_UA-42713825-6=1; previous_url=eyJpdiI6Imx3c0lrWHV1UUlwOStZaGNGbUN1bmc9PSIsInZhbHVlIjoiWXRVY1JZVkZ0Ynl1ZU5wWXRWYWZjS2hOSFZ5Q1FHaWNMMUpNQXo2aEkzXC9JMStMWk5OOGY2cEwrM29aVkNodDB0YWNZSlU5cmMzRGpyV3Y1UUZxYXRWRGR2QVc5bDN3VHVcL3hFWWlpV2tzT2J1dFNhaXVkQ1dDb3hnMWpJQW8yZyIsIm1hYyI6ImRkZTIzODY1MmNmYmE5OWEwZTdjYmNhNjFkNDI4OTM2MDk5YjEzZmIwMWJmZjgzMDRjZDNiMDhhN2M1NzU0NjAifQ%3D%3D; XSRF-TOKEN=eyJpdiI6IjJQVHZKUWx1bFFpZnd5K3JTQXFSMkE9PSIsInZhbHVlIjoiUTRZR2M3XC9jOUFNV0swaGFWNkx0eUFRM2lHRzI0OHZMQWJFVG5LTWdJVHhQNmNVdlNNNHlKVkFQWHROM0R1UnBXblwva1FWVkhMRkZKVU9jWUZDa1NnUT09IiwibWFjIjoiZWYzZTBmMDQzMGJmOGQzNTg0YjBkMDE0M2U4NjcyNTc5ZDM4N2VlZjdjMThhNWQwNDFmYjk5OTkyOGEyODY1OSJ9; ralali=eyJpdiI6Imx2REhQYmlyaUFrTHppbGM0RVBuNEE9PSIsInZhbHVlIjoibFRITTk4eTlBSlwveEx1Y01zalFZaVV5UFdUenhKd2RBNW1JK3doWUkrUkNNRHl2TWpjRkNKbkw1VDU5bUhlU3I3aDNJNlwvQ0ZpMHcwV1NIZEZkTVZVZz09IiwibWFjIjoiNWU2ZDIxYTA3MGRmNWJkYWMyZjIxMWQxYTNkNmNhZjE5ZGY0NDk0MGVkMjI3YThjMWRjMmY3NDBkNGU4YTkxOCJ9; amplitude_id_2c1a3f70ab02cb610ab2905c0c4c63c6ralali.com=eyJkZXZpY2VJZCI6IjJkNDhlYTE5LWQ1MTctNDkxOC1hNTg4LTI1NDRhZTA5ZDlkNVIiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTU2NzEyOTEyMzgzNCwibGFzdEV2ZW50VGltZSI6MTU2NzEzNTE5NTUxNSwiZXZlbnRJZCI6MzMsImlkZW50aWZ5SWQiOjAsInNlcXVlbmNlTnVtYmVyIjozM30='
            }
            yield Request(url=res_url, headers=headers, callback=self.parse_detail, meta={"item": item})

    def parse_detail(self, response):
        pro_detail_text = response.text
        item = response.meta["item"]

        pro_json = re.findall('var products=JSON.parse(.*?);dataLayer.push', pro_detail_text, re.S)[0]
        pro_json = pro_json.replace('\\', '').strip("('[").strip("]')")
        pro_data = json.loads(pro_json)
        # print('pro_data:', type(pro_data), pro_data)

        price = pro_data.get('productPrice')
        urrency = pro_data.get('productCurrency')
        title = pro_data.get('productName')
        productImageURL = pro_data.get('productImageURL')
        os_img_2_list = []
        try:
            str_ran = str(random.randint(0, 999999))
            os.makedirs('/home/imgServer/hc/{}'.format(str_ran))
            #     将图片链接保存到硬盘
            code_img = requests.get(url=productImageURL).content
            img_name = str(random.randint(1, 999999))
            with open('/home/imgServer/hc/{}/{}.jpg'.format(str_ran, img_name), 'wb') as f:
                f.write(code_img)
            os_img_2 = 'http://img.youkeduo.com.cn/hc/' + '{}/{}.jpg'.format(str_ran, img_name)
            os_img_2_list.append(os_img_2)
            os_img_2_str_1 = os_img_2_list[0]
            os_img_2_str = ','.join(os_img_2_list)
            item['list_img'] = os_img_2_str_1
            item['imgs'] = os_img_2_str

            print('图片ok', os_img_2_list)
        except:
            print('图片错误.')

        print('price:', price)
        print('urrency:', urrency)
        print('title:', title)
        print('productImageURL:', productImageURL)
        item["price"] = price
        item["title"] = title
        item['urrency'] = urrency

        pro_json_2 = re.findall('<script>var result=JSON.parse(.*?);var crsf_token', pro_detail_text, re.S)[0]
        pro_json_2 = pro_json_2.replace('\\', '').strip("('").strip("')").strip('"')
        pro_json_2 = json.loads(pro_json_2)

        detail = pro_json_2["item_detail"]["result"]["description"]
        # print("detail:", detail)
        item["detail"] = detail

        con_name = pro_json_2["item_detail"]["result"]["vendors"][0]["name_shop"]
        if con_name == None:
            con_name = ''
        print("con_name:", con_name)
        item["con_name"] = con_name

        mobile = pro_json_2["item_detail"]["result"]["vendors"][0]["handphone"]
        if mobile == None:
            mobile = ''
        print('mobile:', mobile)
        item["mobile"] = mobile

        position = pro_json_2["item_detail"]["result"]["vendors"][0]["position"]
        if position == None:
            position = ''
        print('position:', position)

        linkman = pro_json_2["item_detail"]["result"]["vendors"][0]["cp_name"]
        if linkman == None:
            linkman = ''
        print('linkman:', linkman)
        item["linkman"] = linkman

        address = pro_json_2["item_detail"]["result"]["vendors"][0]["city_name"]
        if address == None:
            address = ''
        print('address:', address)
        item["address"] = address

        scopes = pro_json_2["item_detail"]["result"]["categories"][0]["cat_name"]
        if scopes == None:
            scopes = ''
        print('scopes:', scopes)
        item["scopes"] = scopes

        summary = pro_json_2["item_detail"]["result"]["meta_keyword"]
        if summary == None:
            summary = ''
        print('summary:', summary)
        item["summary"] = summary

        # 数据库获取id
        sql_id = "SELECT one_level,two_level,three_level,keyword  FROM bus_spider_data WHERE source = 'Ralali' and  TYPE = 'gongying' AND is_del = '0' AND isuse = '0' ORDER BY create_date LIMIT 1 "
        cur.execute(sql_id)
        print('sql_id?????????????', sql_id)
        res_all_list = cur.fetchall()
        for res_all in res_all_list:
            one_level = res_all[0]
            item['one_level_id'] = str(one_level)
            print('id.........', item['one_level_id'])

            two_level = res_all[1]
            item['two_level_id'] = str(two_level)
            print('id.........', item['two_level_id'])

            three_level = res_all[2]
            item['three_level_id'] = str(three_level)
            print('id.........', item['three_level_id'])

            keywords = res_all[-1]
            item['keywords'] = str(keywords)

        # 创建时间
        create_date = time.strftime('%Y.%m.%d %H:%M:%S ', time.localtime(time.time()))
        item['create_date'] = create_date

        # way
        if price != None:
            way = '0'
        else:
            way = '1'
        item['way'] = way

        print('............................................')
        yield item



