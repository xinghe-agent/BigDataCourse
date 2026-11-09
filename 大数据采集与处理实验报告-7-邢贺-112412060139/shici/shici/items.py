import scrapy


class ShiciItem(scrapy.Item):
    name = scrapy.Field()
    author = scrapy.Field()
    content = scrapy.Field()
