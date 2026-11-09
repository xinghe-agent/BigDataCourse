import re
import scrapy
from house.items import ShellsItem


class ShellsSpider(scrapy.Spider):
    name = "shell"
    allowed_domains = ["www.bspider.top", "bspider.top"]
    start_urls = [f"http://www.bspider.top/fangke/pg{i}" for i in range(1, 4)]

    def parse(self, response):
        # 每个 li 对应一条房源记录
        rows = response.xpath('//ul[@class="resblock-list-wrapper"]/li')
        for row in rows:
            item = ShellsItem()
            item["house"] = row.xpath('div/div[1]/a/text()').get(default="").strip()
            item["address"] = row.xpath('div/a[1]/@title').get(default="").strip()

            # string() 合并节点中的文本，去掉空白字符
            price = row.xpath('string(.//div/div[4]/div[1])').get(default="")
            item["price"] = re.sub(r"\s+", "", price)

            total = row.xpath('div/div[4]/div[2]/text()').get(default="")
            item["total"] = total.replace("总价:", "").replace("总价：", "").strip()

            if item["house"]:
                yield item
