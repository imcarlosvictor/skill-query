import scrapy
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from twisted.internet import reactor, defer

from scrapy_spiders.scrapy_spiders.spiders.linkedin_spider import LinkedinSpider


# TODO: Immediately stop spider after scraping links
@defer.inlineCallbacks
def crawl_linkedin(url):
    # Set url
    LinkedinSpider.api_url = url
    # Create process
    runner = CrawlerRunner(
        settings={
            'FEEDS': {
                'src/data_extracts/linkedin_links.csv': {'format': 'csv'}
            }
        }
    )
    crawler = runner.crawl(LinkedinSpider)
    crawler.addBoth(lambda _: reactor.stop())
    reactor.run()

def start_linkedin_spider(url):
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

# @defer.inlineCallbacks
# def crawl():
#     # Process
#     runner = CrawlerRunner(
#         settings={
#             'FEEDS': {
#                 'src/data_extracts/linkedin_links.csv': {'format': 'csv'}
#             }
#         }
#     )
#     d = runner.crawl(LinkedinSpider)
#     d.addBoth(lambda _: reactor.stop())
#     yield runner.crawl(LinkedinSpider)
#     reactor.stop()

# def spider_start(url):
#     # Set url
#     LinkedinSpider.api_url = url
#     crawl()
#     reactor.run()
