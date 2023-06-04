from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

settings = get_project_settings()
process = CrawlerProcess(settings)

for spider_name in process.spider_loader.list():
    process.crawl(spider_name)
process.start()
