import os
import sys
import json
import scrapy
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, defer
from datetime import datetime

from .scrapy_spiders.spiders.software_eng_spider import SoftwareEngineerSpider, SWEPostSpider
from .scrapy_spiders.spiders.data_analyst_spider import DataAnalystSpider, DAPostSpider



class SpiderControl:
    def reactor_manager(spider):
        def wrapper(self):
            spider(self)
            reactor.run()
        return wrapper

    @reactor_manager
    @defer.inlineCallbacks
    def run_link_spider(self):
        """
        Start both spiders
        """
        # Configure settings
        settings = get_project_settings()
        configure_logging(settings)
        runner = CrawlerRunner(settings)
        # Start spider
        yield runner.crawl(SoftwareEngineerSpider)
        yield runner.crawl(SWEPostSpider)
        reactor.stop()

    def run_swe_spider(self):
        """
        Start both spiders
        """
        # Configure settings
        settings = get_project_settings()
        configure_logging(settings)
        process = CrawlerProcess(settings)
        # Start spider
        process.crawl(SoftwareEngineerSpider)
        if SoftwareEngineerSpider.page_num > 5:
            process.crawl(SWEPostSpider)
            process.start()
        process.start()

    @reactor_manager
    @defer.inlineCallbacks
    def run_job_post_spider(self):
        """
        Start both spiders
        """
        # Configure settings
        settings = get_project_settings()
        configure_logging(settings)
        runner = CrawlerRunner(settings)
        # Start spider
        yield runner.crawl(SWEPostSpider)
        # yield runner.crawl(DAPostSpider)
        reactor.stop()


sc = SpiderControl()
# sc.run_swe_spider()
# sc.run_job_post_spider()
