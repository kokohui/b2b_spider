import scrapy


class LazadaGongYingItem(scrapy.Item):
    name = scrapy.Field()
    review = scrapy.Field()
    priceShow = scrapy.Field()
    two_class_name = scrapy.Field()

