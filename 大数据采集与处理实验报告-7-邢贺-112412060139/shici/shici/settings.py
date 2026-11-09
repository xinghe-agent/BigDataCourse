BOT_NAME = "shici"
SPIDER_MODULES = ["shici.spiders"]
NEWSPIDER_MODULE = "shici.spiders"

ROBOTSTXT_OBEY = True
DOWNLOAD_DELAY = 0.5
DOWNLOAD_TIMEOUT = 30
RETRY_TIMES = 5
LOG_LEVEL = "INFO"

ITEM_PIPELINES = {"shici.pipelines.CsvPipeline": 300}
