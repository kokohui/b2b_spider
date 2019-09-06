# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from time import sleep
from ..items import AlibabaItem
import time
import requests
from lxml import etree
import re
import random
import os
from bs4 import BeautifulSoup
from ..items import AlibabaItem
import pymysql

conn = pymysql.connect(host='192.168.1.210', user='root', passwd='zhangxing888', db='ktcx_buschance', port=3306,
                       charset='utf8')

cur = conn.cursor()  # 获取一个游标


class SpiderDataSpider(scrapy.Spider):
    name = 'spider_data'
    start_urls = ['https://thai.alibaba.com/products/%25E0%25B8%2596%25E0%25B9%2589%25E0%25B8%25A7%25E0%25B8%25A2.html?spm=a2700.galleryofferlist.pagination.2.44576a6fiuBFUz&IndexArea=product_en&page=1']

    def start_requests(self):
        item = AlibabaItem()
        sql_id = "SELECT url, id FROM bus_spider_data WHERE source = 'alibaba' and   TYPE = 'gongying' AND is_del = '0' AND isuse = '0' ORDER BY create_date LIMIT 1 "
        cur.execute(sql_id)
        res_all_list = cur.fetchall()
        url = res_all_list[0][0]
        spdier_data_id = res_all_list[0][-1]
        item['spdier_data_id'] = spdier_data_id
        for num in range(1, 3):
            url_2 = 'https://thai.alibaba.com/products/{}.html?spm=a2700.galleryofferlist.pagination.2.44576a6fiuBFUz&IndexArea=product_en&page={}'.format(url, num)
            print(url_2)
            yield Request(url=url_2, callback=self.parse, meta={"item": item})

    def parse(self, response):
        item = response.meta["item"]
        con_url_list = response.xpath('//div[@class="item-img-inner"]/a/@href').extract()
        for con_url in con_url_list:
            con_url = 'https:' + con_url
            print(con_url)
            yield Request(url=con_url, callback=self.detail_parse, meta={"item": item})

    def detail_parse(self, response):
        print('.........................')
        item = response.meta["item"]

        # 数据库获取id
        sql_id = "SELECT one_level,two_level,three_level,keyword  FROM bus_spider_data WHERE source = 'alibaba' and  TYPE = 'gongying' AND is_del = '0' AND isuse = '0' ORDER BY create_date LIMIT 1 "
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

        # 价格
        price = ''
        try:
            price = response.xpath('//*[@class="ma-spec-price"]//text()').extract()[0]
            if print == '':
                price = response.xpath('//*[@class="ma-reference-price"]//text()').extract()[0]
            print('price', price)
        except:
            print('price', price)
        item['price'] = price

        # units
        units = ''
        try:
            units = response.xpath('//*[@class="ma-quantity-range"]//text()').extract()[0].strip()
            units = units.split(' ')[-1]
            print('units', units)
        except:
            print('units', units)
        item['units'] = units

        # 标题
        title = ''
        try:
            title = str(response.xpath('//h1/text()').extract()[0]).strip()
            print('title:', title)
        except:
            print('title:', title)
        item['title'] = title

        # way
        if price != '':
            way = '0'
        else:
            way = '1'
        item['way'] = way

        com_name = ''
        try:
            com_name = response.xpath('//div[@class="company-name-container"]/a//text()').extract()[0]
            com_name = com_name.strip()
            print('com_name', com_name)
        except:
            print('com_name', com_name)
        item['com_name'] = com_name

        # mobile
        mobile = ''
        try:
            prelist = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151", "152",
                       "153", "155", "156", "157", "158", "159", "186", "187", "188"]
            mobile = random.choice(prelist) + "".join(random.choice("0123456789") for i in range(8))
            print('mobile', mobile)
        except:
            print('mobile', mobile)
        item['mobile'] = mobile



        # # 保存商品图片
        os_img_2_list = []
        try:
            str_ran = str(random.randint(0, 999999999))
            os.makedirs('/home/imgServer/img_tian/{}'.format(str_ran))
            #     将图片链接保存到硬盘
            res_img_list_11 = response.xpath('//*[@class="thumb"]/a/img/@src').extract()
            for img_url in res_img_list_11:
                img_url = 'https:' + img_url.strip()
                strinfo = re.compile('_50x50.jpg')
                img_url = strinfo.sub('', img_url)
                # print('>>>>>>>>>>>>>img_url<<<<<<<<<<<<<<<<<', img_url)

                code_img = requests.get(url=img_url).content
                img_name = str(random.randint(1, 999999999))
                with open('/home/imgServer/img_tian/{}/{}.jpg'.format(str_ran, img_name), 'wb') as f:
                    f.write(code_img)
                os_img_2 = 'http://img.youkeduo.com.cn/img_tian/' + '{}/{}.jpg'.format(str_ran, img_name)
                os_img_2_list.append(os_img_2)
            os_img_2_str_1 = os_img_2_list[0]
            os_img_2_str = ','.join(os_img_2_list)
            item['list_img'] = os_img_2_str_1
            item['imgs'] = os_img_2_str
            print('图片ok', os_img_2_list)
        except:
            print('图片错误.')

        res_detail_html = response.text
        try:
            soup = BeautifulSoup(res_detail_html, 'lxml')
            html = str(soup.find('div', class_="tab-body"))

            strinfo = re.compile('<img.*?>')
            html_2 = strinfo.sub('', html)

            strinfo = re.compile('<br.*?>')
            html_3 = strinfo.sub('', html_2)

            # 把下载图片添加到html
            div_list = ['<div id="img_detail">', '</div>']
            for os_img_2_url in os_img_2_list:
                os_img_2_url = '<img alt="{}" src="{}">'.format(title, os_img_2_url)
                div_list.insert(1, os_img_2_url)
            div_str = '\n'.join(div_list)
            html_all = html_3 + '\n' + div_str
        except Exception as e:
            raise e
        item['detail'] = str(html_all)

        con_url = response.xpath('//div[@class="card-footer"]/a/@href').extract()[0]
        print(con_url)
        self.con_detail(item, con_url)
        sleep(1)

        yield item

    @classmethod
    def con_detail(self, item, url):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
        }
        res_text = requests.get(url=url, headers=headers).text
        tree = etree.HTML(res_text)

        # summary
        summary = ''
        try:
            summary = tree.xpath('//div[@class="company-card-desc"]/div/text()')[0].strip()
            print('summary', summary)
        except:
            print('summary', summary)
        item['summary'] = summary

        scopes = '-'
        try:
            scopes = tree.xpath('//div[@class="block-bottom"]/table/tr[2]/td[2]/div/div/a//text()')
            scopes = str(scopes).strip('[').strip(']')
            print('scopes', scopes)
        except:
            print('scopes', scopes)
        item['scopes'] = scopes

        try:
            conn_url = tree.xpath('//div[@class="nav-box"]/div/ul/li[5]/a/@href')[0]
        except:
            conn_url = tree.xpath('//div[@class="nav-box"]/div/ul/li[4]/a/@href')[0]
        conn_url = 'https://myon.en.alibaba.com' + str(conn_url)
        print(conn_url)

        conn_text = requests.get(url=conn_url, headers=headers).text
        tree = etree.HTML(conn_text)

        # linkman
        linkman = ''
        try:
            linkman = tree.xpath('//div[@class="contact-name"]//text()')[0]
            print('linkman', linkman)
        except:
            print('linkman', linkman)
        item['linkman'] = linkman

        address = '-'
        try:
            address = re.findall('<th>Address:.*?<td>(.*?)</td>', conn_text, re.S)[0]
            print('address', address)
        except:
            print('address', address)
        item['address'] = address

