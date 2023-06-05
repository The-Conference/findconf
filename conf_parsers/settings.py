# Scrapy settings for conf_parsers project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import os
from datetime import date
from logging.handlers import RotatingFileHandler

from scrapy import logformatter
import logging
from distutils.util import strtobool

from scrapy.utils.log import configure_logging

BOT_NAME = "conf_parsers"
SPIDER_MODULES = ["conf_parsers.spiders"]
NEWSPIDER_MODULE = "conf_parsers.spiders"

DEBUG = strtobool(os.getenv("DEBUG", 'True'))
LOG_LEVEL = 'INFO'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "conf_parsers (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/109.0.0.0 Safari/537.36',
    "Accept-Language": "ru-RU,ru",
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "conf_parsers.middlewares.ConfParsersSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "conf_parsers.middlewares.ConfParsersDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "conf_parsers.pipelines.DropOldItemsPipeline": 10,
    "conf_parsers.pipelines.FillTheBlanksPipeline": 100,
    # This pipeline must be the last
    "conf_parsers.pipelines.SaveToDBPipeline": 999,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 429, 403]


class PoliteLogFormatter(logformatter.LogFormatter):
    def dropped(self, item, exception, response, spider):
        return {
            'level': logging.DEBUG if DEBUG else logging.INFO,
            'msg': "Dropped: %(exception)s" + os.linesep + "conf_id: %(conf_id)s",
            'args': {
                'exception': exception,
                'conf_id': item.get('conf_id'),
            }
        }


LOG_FORMATTER = 'conf_parsers.settings.PoliteLogFormatter'
rotating_log_handler = RotatingFileHandler(
    filename='./logs/scrapy.log',
    encoding="utf-8",
    maxBytes=5 * 1000000,
    backupCount=5,
)

configure_logging(install_root_handler=False)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s: %(message)s",
    handlers=[rotating_log_handler, ],
)

# Items older than this date will be dropped
FILTER_DATE = date(date.today().year, 1, 1)

DB_USER: str = os.getenv("DB_USER", "postgres")
DB_PASS: str = os.getenv("DB_PASS", "changeme")
DB_HOST: str = os.getenv("DB_HOST", "postgres")
DB_PORT: str = os.getenv("DB_PORT", "5432")
DB_NAME: str = os.getenv("DB_NAME", "mydatabase")

if DEBUG:
    # FEEDS = {
    #     'conf_parsers/data/%(name)s/%(name)s_%(time)s.json': {
    #         'format': 'json',
    #         'overwrite': True,
    #         'indent': 4,
    #         'store_empty': False,
    #         'encoding': 'utf8',
    #     }
    # }
    DATABASE_URL = "sqlite:///my_db.sqlite3"
else:
    DATABASE_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

PLAYWRIGHT_BROWSER_TYPE = "webkit"
