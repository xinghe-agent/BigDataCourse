BOT_NAME = "house"
SPIDER_MODULES = ["house.spiders"]
NEWSPIDER_MODULE = "house.spiders"

ROBOTSTXT_OBEY = True
DOWNLOAD_DELAY = 0.5
DOWNLOAD_TIMEOUT = 20
LOG_LEVEL = "INFO"

ITEM_PIPELINES = {"house.pipelines.CsvPipeline": 300}
