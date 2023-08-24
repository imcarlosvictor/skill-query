import os
import sys
import json
import scrapy
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, defer
from datetime import datetime

from scrapy_spiders.spiders.linkedin_spider import SoftwareEngineerSpider, DataAnalystSpider



@defer.inlineCallbacks
def run_spider():
    """
    Start both spiders
    """
    settings = get_project_settings()
    configure_logging(settings)
    runner = CrawlerRunner(settings)
    # crawl linkedin spider
    yield runner.crawl(SoftwareEngineerSpider)
    yield runner.crawl(DataAnalystSpider)
    reactor.stop()

run_spider()
reactor.run()
