import os
import sys
import re
import json
import logging
import w3lib.html
import scrapy
from datetime import date, datetime
from scrapy.spiders import CrawlSpider
from scrapy.linkextractors import LinkExtractor


# set path
FILENAME = __file__
DIRECTORY_PATH = os.path.abspath(os.path.dirname(__file__))
EXPORT_FEED_DIR = os.path.abspath(os.path.join(DIRECTORY_PATH, '../../../export_feed/'))
PROXY_LIST_PATH = os.path.abspath(os.path.join(DIRECTORY_PATH, '../../proxy_list.txt'))


class DataAnalystSpider(scrapy.Spider):
    """
    Scrape all job links from the given URL and store the data collected in a file.
    """
    name = 'data_analyst_link_spider'
    api_url = 'https://ca.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=data+analyst+worldwide&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum='
    page_num = 0

    custom_settings = {
        'FEEDS': {
            f'{EXPORT_FEED_DIR}/%(name)s/%(time)s.csv': {
                'format': 'csv'
            },
        },
        'DOWNLOAD_DELAY': 0.9,
        # 'PROXY_POOL_ENABLED': True,
        # 'RETRY_TIMES': 10,
        # 'RETRY_HTTP_CODES': [500,503,504,400,403,404,408],
        # 'DOWNLOADER_MIDDLEWARES': {
        #     'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
        #     'scrapy_proxies.RandomProxy': 100,
        #     'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
        # },
        # 'PROXY_LIST': PROXY_LIST_PATH,
        # 'PROXY_MODE': 0,

        # 'ROTATING_PROXY_LIST_PATH': PROXY_LIST_PATH,
        # 'DOWNLOADER_MIDDLEWARES': {
        #     # 'scrapy_proxy_pool.middlewares.ProxyPoolMiddleware': 610,
        #     # 'scrapy_proxy_pool.middlewares.BanDetectionMiddleware': 620,
        #     'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
        #     'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
        # },
        # 'PROXY_POOL_BAN_POLICY': 'scrapy_spiders.policy.BanDetectionPolicyNotText',
        'LOG_LEVEL': 'INFO',
        # 'LOG_ENABLED': False,
    }

    def start_requests(self):
        first_job_on_page = 0
        start_url = self.api_url + str(first_job_on_page)
        yield scrapy.Request(url=start_url, callback=self.parse_links, meta={'first_job_on_page': first_job_on_page})
        # self.get_job_details()

    def parse_links(self, response):
        """
        Grab links from each job post.
        """
        first_job_on_page = response.meta['first_job_on_page']
        jobs = response.css('li') # Job postings
        num_jobs_returned = len(jobs)
        print('####################################')
        print(f'<< Data Analyst >> Page number: {self.page_num}')

        job_links = {}
        for job in jobs:
            job_links['link'] = job.css('a::attr(href)').get(default='')
            yield job_links

        ########## Request Next Page ##########
        if num_jobs_returned > 0:
            self.page_num += 1
            first_job_on_page = int(first_job_on_page) + 25
            next_url = self.api_url + str(first_job_on_page)
            yield scrapy.Request(url=next_url, callback=self.parse_links, meta={'first_job_on_page': first_job_on_page})
