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


class SWEPostSpider(scrapy.Spider):
    """
    Extract data from the scraped links.
    """
    def __init__(self):
        name = 'SWE_post_spider'
        export_feed_path = f'{EXPORT_FEED_DIR}/SWE_role_spider/'
        self.urls = []

    custom_settings = {
        'FEEDS': {
            f'{EXPORT_FEED_DIR}/%(name)s/%(name)s_%(time)s': {
                'format': 'csv',
            }
        }
    }

    def start_requests(self):
        with open(self.export_feed_path, 'rt') as f:
            self.urls = [url.strip() for url in f.readlines()]

        for url in self.urls[1:]:
            yield scrapy.Request(url=url, callback=self.parse_posts)

    def parse_job_details(self):
        """
        Extract data from job links.
        """
        job_description = response.css('div.show-more-less-html__markup').get()
        output = w3lib.html.remove_tags(job_description)

        yield {
            'role': response.css('h1::text').get().strip(),
            'seniority_level' : response.css('span.description__job-criteria-text::text').get().strip(),
            'employment_type' : response.css('span.description__job-criteria-text').get().strip(),
            'description' : output
        }

class DAPostSpider(scrapy.Spider):
    """
    Extract data from the scraped links.
    """
    def __init__(self):
        self.name = 'DA_post_spider'
        self.export_feed_path = f'{EXPORT_FEED_DIR}/DA_role_spider/2023-08-24T10-41-11.csv'
        self.urls = []

    custom_settings = {
        'FEEDS': {
            f'{EXPORT_FEED_DIR}/%(name)s/%(time)s.json': {
                'format': 'json',
            }
        }
    }

    def start_requests(self):
        with open(self.export_feed_path, 'rt') as f:
            self.urls = [url.strip() for url in f.readlines()]

        for url in self.urls[1:]:
            yield scrapy.Request(url=url, callback=self.parse_posts)

    def parse_posts(self, response):
        """
        Extract data from job links.
        """
        seniority_level = response.css('span.description__job-criteria-text::text').get().strip()
        seniority_level_no_tags = w3lib.html.remove_tags(seniority_level)

        employment_level = response.css('span.description__job-criteria-text').get().strip()
        employment_level_no_tage = w3lib.html.remove_tags(employment_level)

        job_description = response.css('div.show-more-less-html__markup').get()
        job_description_no_tags = w3lib.html.remove_tags(job_description)

        yield {
            'role': response.css('h1::text').get().strip(),
            'seniority_level' : seniority_level_no_tags,
            'employment_type' : employment_level_no_tage,
            'job_description' : job_description_no_tags 
        }
