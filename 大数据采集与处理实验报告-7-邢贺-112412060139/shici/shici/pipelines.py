import csv
from pathlib import Path
from itemadapter import ItemAdapter


class CsvPipeline:
    def open_spider(self, spider=None):
        self.file = (Path.cwd() / "tangshi.csv").open(
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
