# -*- coding: utf-8 -*-
import pymysql
import hashlib
import requests

conn = pymysql.connect(host='192.168.1.210', user='root', passwd='zhangxing888', db='ktcx_buschance_20190806',
                       port=3306,
                       charset='utf8')
cur = conn.cursor()  # 获取一个游标

YOUDAO_URL = 'http://openapi.youdao.com/api'
APP_KEY = '05d75b8083faae9a'
APP_SECRET = 'JW7cD7E6hC4v5hfNwrjT5oC3Y1cydnXl'


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

    sql = 'select id, company_name from bus_user where  company_name is not null and company_name != ""'
    try:
        cur.execute(sql)
        data = cur.fetchall()
        print("data", data)
        return data
    except:
        conn.rollback()


if __name__ == '__main__':
    word_list = sql_query()
    for word in word_list:
        sql_id = word[0]
        standards_chinese = word[1]
        print(standards_chinese)

        name_trans = ''
        try:
            name_trans = connect(standards_chinese)
            print(name_trans)

        except Exception as e:
            raise e

        if name_trans != '':
            test_all = str(name_trans).replace('"', "'")
            try:
                sql = 'update bus_user set  company_name_ty  = "{}" where id = "{}"'.format(test_all, sql_id)
                print(sql)
                data = cur.execute(sql)
                conn.commit()
            except:
                print('此处有个错')

cur.close()
conn.close()