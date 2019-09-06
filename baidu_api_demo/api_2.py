# -*- coding: utf-8 -*-
import hashlib
import requests
import pymysql
from time import sleep
from lxml import etree
from bs4 import BeautifulSoup

conn = pymysql.connect(host='192.168.1.210', user='root', passwd='zhangxing888', db='ktcx_buschance_20190806',
                       port=3306,
                       charset='utf8')
cur = conn.cursor()


def connect(q):
    appid = '20190828000330193'  # 你的appid
    secretKey = 'U3cK8WcRr21HCYImQiUJ'  # 你的密钥
    myurl = '/api/trans/vip/translate'
    fromLang = 'auto'
    toLang = 'th'
    salt = 1435660288
    sign = appid + q + str(salt) + secretKey

    m1 = hashlib.md5()
    m1.update(sign.encode("utf8"))
    sign = m1.hexdigest()
    myurl = 'http://api.fanyi.baidu.com' + myurl + '?appid=' + appid + '&q=' + q + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
        salt) + '&sign=' + sign

    res_text = ''
    try:
        response = requests.get(url=myurl)
        print(response.text)
        response_json = response.json()
        res_text = response_json.get('trans_result')[0].get('dst')
    except:
        print('res_text出错')

    print('状态码:', response.status_code)

    if res_text != '':
        return res_text
    else:
        print('api出错')


def sql_query():

    sql = 'select id, detail  from bus_industry_news_ty where  detail is not null and detail != ""'

    try:
        cur.execute(sql)
        data = cur.fetchall()
        print('....')
        print(data)
        return data
    except:
        conn.rollback()


if __name__ == '__main__':
    word_list = sql_query()
    for word in word_list:
        sql_id = word[0]
        detail_chinese = word[1]

        soup = BeautifulSoup(str(detail_chinese), 'lxml')
        tree = etree.HTML(detail_chinese)


        img_p = ''
        try:
            img_list = soup.find_all('img')
            print(img_list)
            for img in img_list:
                img_p += str(img)
        except:
            print('没有图片')
        img_p_2 = "<p>" + img_p + "</p>"
        img_p_2 = str(img_p_2).replace('"', "'")
        print(img_p_2)

        name_trans_all = ''
        try:
            detail_text_list = tree.xpath('//p//text()')[0]
            # detail_text_list = tree.xpath('//div//text()')[1]
            print("detail_text_list", detail_text_list)
            # for detail_text in detail_text_list:
            name_trans = connect(detail_text_list)
            if name_trans == None:
                name_trans = ''
            name_trans_all += str(name_trans)
        except:
            print('没有文字')
        name_trans_all_2 = "<p>" + name_trans_all + "</p>"
        print("name_trans_all_2:", name_trans_all_2)


        test_all = name_trans_all_2 + img_p_2
        test_all = test_all.replace('"', "'")
        try:
            sql = 'update bus_industry_news_ty set  detail  = "{}" where id = "{}"' .format(test_all, sql_id)
            print(sql)
            data = cur.execute(sql)
            conn.commit()
        except:
            print('此处有个错')

cur.close()
conn.close()