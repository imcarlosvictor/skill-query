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



def reactor_manager(function):
    def wrapper():
        function()
        reactor.run()
    return wrapper

@reactor_manager
@defer.inlineCallbacks
def run_link_extract_spider():
    """
    Start both spiders
    """
    # Configure settings
    settings = get_project_settings()
    configure_logging(settings)
    runner = CrawlerRunner(settings)
    # Start spider
    yield runner.crawl(SoftwareEngineerSpider)
    yield runner.crawl(DataAnalystSpider)
    reactor.stop()
# run_link_extract_spider()

@reactor_manager
@defer.inlineCallbacks
def run_job_post_spider():
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
# run_job_post_spider()
# s = SWEPostSpider()
# s.parse_posts()
