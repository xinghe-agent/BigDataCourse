import importlib.util
import subprocess
import sys

missing = [p for p in ("scrapy", "pandas") if importlib.util.find_spec(p) is None]
if missing:
    subprocess.run([sys.executable, "-m", "pip", "install", *missing], check=True)

import csv
import re
from pathlib import Path

import scrapy
import pandas as pd
from itemadapter import ItemAdapter
from scrapy.crawler import CrawlerProcess

CSV_PATH = Path(__file__).resolve().parent / "shici" / "tangshi.csv"


class ShiciItem(scrapy.Item):
    name = scrapy.Field()
    author = scrapy.Field()
    content = scrapy.Field()



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



class CsvPipeline:
    def open_spider(self, spider=None):
        self.file = CSV_PATH.open(
            "w", encoding="utf-8-sig", newline=""
        )
        self.writer = csv.DictWriter(
            self.file, fieldnames=["name", "author", "content"]
        )
        self.writer.writeheader()

    def process_item(self, item, spider=None):
        self.writer.writerow(ItemAdapter(item).asdict())
        return item

    def close_spider(self, spider=None):
        self.file.close()

def main():
    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    settings = {'BOT_NAME': 'shici', 'ROBOTSTXT_OBEY': True, 'DOWNLOAD_DELAY': 0.5, 'DOWNLOAD_TIMEOUT': 30, 'RETRY_TIMES': 5, 'LOG_LEVEL': 'INFO'}
    settings["ITEM_PIPELINES"] = {CsvPipeline: 300}
    process = CrawlerProcess(settings=settings)
    process.crawl(TangshiSpider)
    process.start()
    csv_path = CSV_PATH
    df = pd.read_csv(csv_path)
    if df.empty:
        raise RuntimeError("No poems collected. Check the crawl log for HTTP or network errors and rerun the crawl cell.")
    if df[["name", "author", "content"]].isna().any().any():
        raise RuntimeError("Some poem fields are missing. Check the detail page parsing and crawl log.")
    print(df.head(10).to_string(index=False))
    print("记录数：", len(df))


if __name__ == "__main__":
    main()
