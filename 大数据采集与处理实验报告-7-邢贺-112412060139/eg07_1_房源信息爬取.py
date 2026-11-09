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

CSV_PATH = Path(__file__).resolve().parent / "house" / "shells.csv"


class ShellsItem(scrapy.Item):
    house = scrapy.Field()
    address = scrapy.Field()
    price = scrapy.Field()
    total = scrapy.Field()



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



class CsvPipeline:
    def open_spider(self, spider=None):
        self.file = CSV_PATH.open(
            "w", encoding="utf-8-sig", newline=""
        )
        self.writer = csv.DictWriter(
            self.file, fieldnames=["house", "address", "price", "total"]
        )
        self.writer.writeheader()

    def process_item(self, item, spider=None):
        self.writer.writerow(ItemAdapter(item).asdict())
        return item

    def close_spider(self, spider=None):
        self.file.close()

def main():
    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    settings = {'BOT_NAME': 'house', 'ROBOTSTXT_OBEY': True, 'DOWNLOAD_DELAY': 0.5, 'DOWNLOAD_TIMEOUT': 20, 'LOG_LEVEL': 'INFO'}
    settings["ITEM_PIPELINES"] = {CsvPipeline: 300}
    process = CrawlerProcess(settings=settings)
    process.crawl(ShellsSpider)
    process.start()
    csv_path = CSV_PATH
    df = pd.read_csv(csv_path)
    print(df.head(10).to_string(index=False))
    print("记录数：", len(df))


if __name__ == "__main__":
    main()
