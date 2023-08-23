import os
import sys
import json
import scrapy
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, defer
from datetime import datetime

from scrapy_spiders.scrapy_spiders.spiders.data_analyst_spider import DataAnalystSpider
from scrapy_spiders.scrapy_spiders.spiders.software_eng_spider import SoftwareEngineerSpider


def get_time():
    """
    Get current date and time.
    """
    now = datetime.now()
    return now.strftime('%d%m%Y_%H%M%S') # Format: DDMMYY_HHMMSS

def start_spider():
    # create crawler
    settings = get_project_settings()
    configure_logging(settings)
    runner = CrawlerRunner(settings)
    crawler = runner.crawl(SoftwareEngineerSpider)
    # crawler = runner.crawl(DataAnalystSpider)
    # end process by asking the reactor to stop itself
    crawler.addBoth(lambda _: reactor.stop())
    # start up the Twisted reactor (event) loop handler) manually
    reactor.run()
