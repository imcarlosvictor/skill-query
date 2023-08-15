from twisted.internet import reactor
import scrapy
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy_spiders.scrapy_spiders.spiders.linkedin_spider import LinkedinSpider



# def crawl_linkedin(url):
#     # set url
#     LinkedinSpider.api_url = url

#     # call spider
#     process = CrawlerProcess(
#         settings={
#             'FEEDS': {
#                 'linkedin_links.csv': {'format': 'csv'}
#             }
#         }
#     )
#     process.crawl(LinkedinSpider)
#     process.start()

def crawl_linkedin(url):
    # set url
    LinkedinSpider.api_url = url
    runner = CrawlerRunner(
        settings={
            'FEEDS': {
                'data_extracts/linkedin_links.csv': {'format': 'csv'}
            }
        }
    )

    d = runner.crawl(LinkedinSpider)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()
