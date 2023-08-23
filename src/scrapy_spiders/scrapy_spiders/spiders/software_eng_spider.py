import os
import sys
import json
from datetime import datetime

import w3lib.html
import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.linkextractors import LinkExtractor


# set path
FILENAME = __file__
DIRECTORY_PATH = os.path.abspath(os.path.dirname(__file__))
EXPORT_FEED_DIR = os.path.abspath(os.path.join(DIRECTORY_PATH, '../../../export_feed'))


class SoftwareEngineerSpider(scrapy.Spider):
    """
    Scrape all job links from the given URL and store the data collected in a file.
    """

    name = 'SWE_spider'
    api_url = 'https://ca.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=software+engineer&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum='
    custom_settings = {
        'FEEDS': {
            f'{EXPORT_FEED_DIR}/%(name)s/%(name)s_%(time)s.csv': {
                'format': 'csv',
            }
        },
        'DOWNLOAD_DELAY': 0.9
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
        print('########### Num Jobs Returned ###########')
        print(num_jobs_returned)
        print('##############################')

        job_links = {}
        for job in jobs:
            job_links['link'] = job.css('a::attr(href)').get(default='')
            yield job_links

        ########## Request Next Page ##########
        if num_jobs_returned > 0:
            first_job_on_page = int(first_job_on_page) + 25
            next_url = self.api_url + str(first_job_on_page)
            yield scrapy.Request(url=next_url, callback=self.parse_links, meta={'first_job_on_page': first_job_on_page})
