import re
import scrapy
from shici.items import ShiciItem


class TangshiSpider(scrapy.Spider):
    name = "tangshi"
    allowed_domains = ["www.bspider.top", "bspider.top"]
    start_urls = ["http://www.bspider.top/gushiwen/ts"]

    def parse(self, response):
        # 列表页：定位每首诗所在的 span
        for row in response.xpath('//div[@class="typecont"]/span'):
            href = row.xpath('a/@href').get()
            if not href:
                continue

            item = ShiciItem()
            item["name"] = row.xpath('a/text()').get(default="").strip()
            author = "".join(row.xpath('text()').getall())
            item["author"] = re.sub(r"[()（）\s]", "", author)

            # 把列表页数据传入详情页回调
            yield response.follow(
                href, callback=self.parse_detail, meta={"item": item}
            )

    def parse_detail(self, response):
        item = response.meta["item"]

        if not item["author"]:
            item["author"] = response.css("p.source a:first-child::text").get(default="").strip()

        # string() 合并正文及 br 分隔的文本
        content = response.xpath('string(//div[@class="contson"])').get(default="")
        item["content"] = re.sub(r"\s+", "", content)
        yield item
