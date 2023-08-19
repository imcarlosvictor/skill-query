import time
import scrapy
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, defer

from scrapy_spiders.scrapy_spiders.spiders.linkedin_spider import LinkedinSpider


def start_crawler(url):
    # set url
    LinkedinSpider.api_url = url
    # create crawler
    settings = get_project_settings()
    configure_logging(settings)
    runner = CrawlerRunner(settings)
    crawler = runner.crawl(LinkedinSpider)
    crawler.addBoth(lambda _: reactor.stop())


# TODO: Restart reactor after crawler execution
def start_spider(url):
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
