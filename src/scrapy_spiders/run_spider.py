import os
import sys
import json
import scrapy
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, defer
from datetime import datetime

from .scrapy_spiders.spiders.linkedin_spider import SoftwareEngineerSpider, DataAnalystSpider
from .scrapy_spiders.spiders.job_post_spider import SWEPostSpider, DAPostSpider



def create_reactor(function):
    def wrapper():
        function()
        reactor.run()
    return wrapper

@create_reactor
@defer.inlineCallbacks
def run_linkedin_spider():
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


@create_reactor
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
    yield runner.crawl(DAPostSpider)
    reactor.stop()

