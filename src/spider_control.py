import os
import sys
import json
import scrapy
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, defer
from datetime import date, datetime

from scrapy_spiders.scrapy_spiders.spiders.software_eng_spider import SoftwareEngineerSpider,SoftwareEngineerPostSpider
from scrapy_spiders.scrapy_spiders.spiders.data_analyst_spider import DataAnalystSpider, DataAnalystPostSpider


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
        yield runner.crawl(DataAnalystSpider)
        reactor.stop()

    # def run_link_spider(self):
    #     """
    #     Scrape job links simultaneously.
    #     """
    #     settings = get_project_settings()
    #     configure_logging(settings)
    #     process = CrawlerProcess(settings)
    #     yield process.crawl(SoftwareEngineerSpider)
    #     yield process.crawl(DataAnalystSpider)
    #     process.start()

    def run_post_spider(self):
        """
        Crawl and scrape job posts simultaneously.
        """
        settings = get_project_settings()
        configure_logging(settings)
        process = CrawlerProcess(settings)
        process.crawl(SoftwareEngineerPostSpider)
        process.crawl(DataAnalystPostSpider)
        process.start()
        # TODO: Implment keyword parser to execute once post scraper is completed.
        # yield self.keyword_parser('software_eng')
        # yield self.keyword_parser('data_analyst')

    def keyword_parser(self, job_title):
        """
        Track the number of times a keyword appears from the extracted data.
        """
        # FILENAME = __file__
        DIRECTORY_PATH = os.path.abspath(os.path.dirname(__file__))
        SEARCH_POOL_FILE = os.path.abspath(os.path.join(DIRECTORY_PATH, 'keyword_search_pool.json'))
        if job_title == 'software_eng':
            EXPORT_FEED_DIR = os.path.abspath(os.path.join(DIRECTORY_PATH, 'export_feed/software_engineer_post_spider/'))
        elif job_title == 'data_analyst':
            EXPORT_FEED_DIR = os.path.abspath(os.path.join(DIRECTORY_PATH, 'export_feed/data_analyst_post_spider/'))

        today = date.today()
        cur_year = today.strftime("%Y")
        cur_month = today.strftime("%m")
        cur_year_month = cur_year + '-' + cur_month

        # Get scraped file for the current date
        TARGET_FILE = ''
        for file in os.listdir(EXPORT_FEED_DIR):
            if (file[:7] == cur_year_month):
                TARGET_FILE = os.path.join(EXPORT_FEED_DIR, file)

        # Search for keywords
        with open(TARGET_FILE, 'r') as jsonFile:
            scraped_data = json.load(jsonFile)

        with open(SEARCH_POOL_FILE, 'r') as jsonFile:
            keywords = json.load(jsonFile)

        for i in range(1, len(scraped_data)):
            for desc in scraped_data[i]['description']:
                for word in desc.split():
                    if word.lower() in keywords['technology'].keys():
                        keywords['technology'][word.lower()] += 1
                    if word.lower() in keywords['frameworks'].keys():
                        keywords['frameworks'][word.lower()] += 1
                    if word.lower() in keywords['education'].keys():
                        keywords['education'][word.lower()] += 1

        # Create count for country
        for i in range(1, len(scraped_data)):
            for word in scraped_data[i]['location'].split(', '):
                print(word.lower())
                if word.lower() in keywords['location'].keys():
                    keywords['location'][word.lower()] += 1
                    continue
                if word.lower() in keywords['usa_states']:
                    keywords['usa_states'][word.lower()] += 1
        keywords['location']['united states'] += sum(keywords['usa_states'].values())

        # Add transformed data to dashboard data file
        keyword_file_path = os.path.abspath(os.path.join(DIRECTORY_PATH, 'export_feed/dashboard_data/keyword_data.json'))
        data_json_file = open(keyword_file_path)

        with open(keyword_file_path, 'r') as json_file:
            data = json.load(json_file)
        # Add year
        if cur_year not in data.items():
            data[cur_year] = {}
        # Add month
        # if cur_month not in data[cur_year].items():
        prev_month = cur_month
        data[cur_year] = ({prev_month: keywords})
        # data[cur_year][cur_month] = {} 
        # Update JSON file with new changes
        with open(keyword_file_path, 'w') as json_file:
            json.dump(data, json_file)


    # @reactor_manager
    # @defer.inlineCallbacks
    # def run_job_post_spider(self):
    #     """
    #     Start both spiders
    #     """
    #     # Configure settings
    #     settings = get_project_settings()
    #     configure_logging(settings)
    #     runner = CrawlerRunner(settings)
    #     # Start spider
    #     yield runner.crawl(SWEPostSpider)
    #     # yield runner.crawl(DAPostSpider)
    #     reactor.stop()


sc = SpiderControl()
# sc.run_link_spider()
# sc.run_post_spider()
sc.keyword_parser('software_eng')
