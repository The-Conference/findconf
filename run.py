from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from conf_parsers import settings

setting = Settings()
setting.setmodule(settings)
process = CrawlerProcess(setting)

for spider_name in process.spider_loader.list():
    process.crawl(spider_name)
process.start()
