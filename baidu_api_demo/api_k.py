# -*- coding: utf-8 -*-
import hashlib
import requests
import pymysql
import asyncio
import json
from lxml import etree
from bs4 import BeautifulSoup
from time import sleep

conn = pymysql.connect(host='192.168.1.210', user='root', passwd='zhangxing888', db='ktcx_buschance_20190806',
                       port=3306,
                       charset='utf8')

cur = conn.cursor()  # 获取一个游标


def connect(q):
    appid = '20190828000330193'  # 你的appid
    secretKey = 'U3cK8WcRr21HCYImQiUJ'  # 你的密钥
    myurl = '/api/trans/vip/translate'
    # q = '你好'
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
        print(response_json)
    except:
        print('res_text出错')

    print('状态码:', response.status_code)

    if res_text != '':
        return res_text
    else:
        print('api出错')


def sql_query():

    sql = 'select id, keywords from bus_industry_news_ty where  keywords is not null and keywords != "" '

    try:
        cur.execute(sql)
        data = cur.fetchall()
        print("data", data)
        return data
    except:
        conn.rollback()


async def main():
        word_list = sql_query()
        for word in word_list:
            sql_id = word[0]
            standards_chinese_list = word[1]
            name_trans = ''
            try:
                standards_chinese_list = json.loads(word[1])
                standards_trans_list = []
                for standards_chinese_dict in standards_chinese_list:
                    standards_chinese = standards_chinese_dict['keyword']
                    print(standards_chinese)
                    if standards_chinese == 'None':
                        pass

                    try:
                        name_trans = connect(standards_chinese)
                        if name_trans == 'None':
                            name_trans = ''
                        standards_chinese_dict['keyword'] = name_trans
                        standards_trans_list.append(standards_chinese_dict)
                        print(name_trans)
                    except:
                        print('没有文字')
            except:
                print('不是json')

            if name_trans != '':
                test_all = str(standards_trans_list).replace('"', "'")
                print('test_all_1', test_all)
                test_all = json.dumps(test_all).replace('"', "'")
                print('test_all_2', test_all)

                try:
                    sql = 'update bus_industry_news_ty set  keywords  = "{}" where id = "{}"'.format(test_all, sql_id)
                    print(sql)
                    data = cur.execute(sql)
                    conn.commit()
                except Exception as e:
                    raise e
                    print('此处有个错')
            else:
                print('此条无效~')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

    # sql_query()

cur.close()
conn.close()