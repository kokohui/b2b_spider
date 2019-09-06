import pymysql
import json
from openpyxl import Workbook


class LazadaGongYingPipeline(object):

    def open_spider(self, spdier):
        print('爬虫开始》》》》')
        self.wb = Workbook()
        self.wb_sheet = self.wb.create_sheet("index")

    def process_item(self, item, spider):
        print('process_item>>>>>>>>>>>>>>>>>>>>>>>')
        self.wb_sheet.append([item['two_class_name'], item['name'], item['review'], item['priceShow']])
        # 必须保存
        self.wb.save("lazanda_3.xlsx")

        print('保存成功!')
        return item

    def close_spider(self, spider):
        print('爬虫结束>>>>>>>>')
        self.wb.save("lazanda_3.xlsx")

