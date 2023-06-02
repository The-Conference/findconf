# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import logging
from scrapy import signals
from scrapy.utils.project import get_project_settings

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

from scrapy.http import HtmlResponse
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

settings = get_project_settings()


class ConfParsersSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class ConfParsersDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class SeleniumMiddleware:
    """
    To route requests through Selenium, add this middleware to Spider's settings:

        "DOWNLOADER_MIDDLEWARES": {
            'conf_parsers.middlewares.SeleniumMiddleware': 543,
        },

    No further changes to code required.
    """
    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.spider_opened, signals.spider_opened)
        crawler.signals.connect(middleware.spider_closed, signals.spider_closed)
        return middleware

    def process_request(self, request, spider):
        logging.debug(f"Selenium processing request - {request.url}")
        self.driver.get(request.url)
        return HtmlResponse(
            request.url,
            body=self.driver.page_source,
            encoding='utf-8',
            request=request,
        )

    def spider_opened(self, spider):
        options = webdriver.ChromeOptions()
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "eager"
        options.add_argument("--headless")
        options.add_argument("--disable-3d-apis")
        if settings.get('DEBUG'):
            self.driver = webdriver.Chrome(options=options,
                                           desired_capabilities=caps,
                                           executable_path=ChromeDriverManager().install())
        else:
            self.driver = webdriver.Remote(options=options,
                                           desired_capabilities=caps,
                                           command_executor="http://selenium:4444/wd/hub")

    def spider_closed(self, spider):
        self.driver.close()
