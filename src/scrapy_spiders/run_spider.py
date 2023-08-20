import os
import sys
import json
import scrapy
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, defer
from datetime import datetime

from scrapy_spiders.scrapy_spiders.spiders.linkedin_spider import LinkedinSpider


def get_time():
    """
    Get current date and time.
    """
    now = datetime.now()
    return now.strftime('%d%m%Y_%H%M%S') # Format: DDMMYY_HHMMSS

def start_spider(url, position):
    # set parameters
    LinkedinSpider.api_url = url
    # create crawler
    settings = get_project_settings()
    configure_logging(settings)
    runner = CrawlerRunner(settings)
    crawler = runner.crawl(LinkedinSpider)
    # end process by asking the reactor to stop itself
    crawler.addBoth(lambda _: reactor.stop())
    # start up the Twisted reactor (event) loop handler) manually
    reactor.run()

# TODO: Restart reactor after crawler execution
def start_crawler(url):
    # Set url
    LinkedinSpider.api_url = url

    process = CrawlerProcess(
        settings={
            'FEEDS': {
                'src/data_extracts/linkedin_links.csv': {'format': 'csv'},
            },
        }
    )
    process.crawl(LinkedinSpider)
    process.start(stop_after_crawl=True, install_signal_handlers=False)
