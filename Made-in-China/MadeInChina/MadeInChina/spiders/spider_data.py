# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from ..items import MadeinchinaItem
import re
import pymysql
import time
from bs4 import BeautifulSoup
import random
import os
import requests
from lxml import etree

conn = pymysql.connect(host='192.168.1.210', user='root', passwd='zhangxing888', db='ktcx_buschance', port=3306,
                       charset='utf8')

cur = conn.cursor()  # 获取一个游标


class SpiderDataSpider(scrapy.Spider):
    name = 'spider_data'

    # start_urls = ['https://www.made-in-china.com/multi-search/headset/F2/8.html']

    def start_requests(self):
        item = MadeinchinaItem()
        sql_id = "SELECT url, id FROM bus_spider_data WHERE source = 'MadeChina' and   TYPE = 'gongying' AND is_del = '0' AND isuse = '0' ORDER BY create_date LIMIT 1 "
        cur.execute(sql_id)
        res_all_list = cur.fetchall()
        url = res_all_list[0][0]
        spdier_data_id = res_all_list[0][-1]
        item['spdier_data_id'] = spdier_data_id
        for num in range(1, 3):
            url_2 = 'https://www.made-in-china.com/multi-search/{}/F1/{}.html'.format(url, num)
            print(url_2)
            yield Request(url=url_2, callback=self.parse, meta={"item": item})

    def parse(self, response):
        item = response.meta['item']
        res_url_list = response.xpath('//h2/a/@href').extract()
        for res_url in res_url_list:
            res_url = 'https:' + res_url
            yield Request(url=res_url, callback=self.parse_detail, meta={"item": item})

    def parse_detail(self, response):

        item = response.meta['item']

        # 数据库获取id
        sql_id = "SELECT one_level,two_level,three_level,keyword  FROM bus_spider_data WHERE source = 'MadeChina' and  TYPE = 'gongying' AND is_del = '0' AND isuse = '0' ORDER BY create_date LIMIT 1 "
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


        # # 保存商品图片
        os_img_2_list = []
        try:
            str_ran = str(random.randint(0, 999999999))
            os.makedirs('/home/imgServer/img_tian/{}'.format(str_ran))
            #     将图片链接保存到硬盘
            res_img_list_11 = response.xpath('//*[@class="swiper-wrapper"]/div/@fsrc').extract()
            for img_url in res_img_list_11:
                img_url = 'https:' + img_url.strip()
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

        # 创建时间
        create_date = time.strftime('%Y.%m.%d %H:%M:%S ', time.localtime(time.time()))
        item['create_date'] = create_date

        # 价格
        price = 'discuss personally'
        try:
            price = str(response.xpath('//div[@class="sr-proMainInfo-baseInfo-propertyPrice"]/table//tr[2]/td[2]/strong//text()').extract()[0].strip())
            print('price', price)
        except:
            print('price', price)
        item['price'] = price

        # units
        units = ''
        try:
            units = response.xpath('//span[@class="unit"]/text()').extract()[0]
            print('units', units)
        except:
            print('units', units)
        item['units'] = units

        # 标题
        title = ''
        try:
            title = str(response.xpath('//h1/text()').extract()[0]).strip()
            print('title', title)
        except:
            print('title', title)
        item['title'] = title

        # way
        if price != '':
            way = '0'
        else:
            way = '1'
        item['way'] = way

        # linkman
        linkman = ''
        try:
            linkman = response.xpath('//div[@class="sr-side-contSupplier-name"]//text()').extract()[0]
            print('linkman', linkman)
        except:
            print('linkman', linkman)
        item['linkman'] = linkman

        res_detail_html = response.text
        try:
            soup = BeautifulSoup(res_detail_html, 'lxml')
            html = str(soup.find('div', class_="sr-layout-content detail-desc"))

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

        con_tel_url = response.xpath('//div[@class="sr-nav-wrap"]/div/div/ul/li[5]/a/@href')[0].extract()
        self.con_tel(item, con_tel_url)
        con_url = response.xpath('//div[@class="sr-nav-wrap"]/div/div/ul/li[3]/a/@href')[0].extract()
        self.con_detail(item, con_url)

        yield item

    @classmethod
    def con_tel(self, item, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        }
        res_text = requests.get(url=url, headers=headers).text
        tree = etree.HTML(res_text)

        # mobile
        mobile = ''
        try:
            mobile = tree.xpath('//div[@class="sr-layout-block contact-block"]/div[2]/div[4]/div[2]//text()')[0].strip()
            print('mobile', mobile)
        except:
            print('mobile', mobile)
        item['mobile'] = mobile

    @classmethod
    def con_detail(self, item, url):
        print('con_detail.....')
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        }
        res_text = requests.get(url=url, headers=headers).text
        tree = etree.HTML(res_text)

        # com_name
        com_name = '个体'
        try:
            com_name = tree.xpath('//h1/text()')[0].strip()
            print('com_name', com_name)
        except:
            print('com_name', com_name)
        item['com_name'] = com_name

        # summary
        summary = ''
        try:
            summary = tree.xpath('//div[@class="sr-layout-block J-block sr-comProfile"]/div[@class="J-txt-wrap sr-comProfile-intro"]/p//text()')[0].strip()
            print('summary', summary)
        except:
            print('summary', summary)
        item['summary'] = summary

        scopes = '-'
        try:
            scopes_list = tree.xpath('//div[@class="sr-layout-main"]/div[2]/div[2]/div[2]/table//tr[2]/td[3]/a/text()')[:-1]
            scopes = ','.join(scopes_list)
            print('scopes', scopes)
        except:
            print('scopes', scopes)
        item['scopes'] = scopes

        address = '-'
        try:
            address = tree.xpath('//div[@class="sr-layout-main"]/div[4]/div[2]/div[1]/div[2]//text()')[0].strip()

            print('address', address)
        except:
            print('address', address)
        item['address'] = address
