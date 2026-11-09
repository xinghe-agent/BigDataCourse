import scrapy


class ShellsItem(scrapy.Item):
    house = scrapy.Field()
    address = scrapy.Field()
    price = scrapy.Field()
    total = scrapy.Field()
