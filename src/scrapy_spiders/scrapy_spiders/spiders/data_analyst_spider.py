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
EXPORT_FEED_DIR = os.path.abspath(os.path.join(DIRECTORY_PATH, '../../../export_feed/'))


class DataAnalystSpider(scrapy.Spider):
    """
    Scrape all job links from the given URL and store the data collected in a file.
    """
    name = 'DA_role_spider'
    api_url = 'https://ca.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=data+analyst&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum'

    custom_settings = {
        'FEEDS': {
            f'{EXPORT_FEED_DIR}/%(name)s/%(time)s.csv': {
                'format': 'csv'
            },
        },
        'DOWNLOAD_DELAY': 0.9,
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

        job_links = {}
        for job in jobs:
            job_links['link'] = job.css('a::attr(href)').get(default='')
            yield job_links

        ########## Request Next Page ##########
        if num_jobs_returned > 0:
            first_job_on_page = int(first_job_on_page) + 25
            next_url = self.api_url + str(first_job_on_page)
            yield scrapy.Request(url=next_url, callback=self.parse_links, meta={'first_job_on_page': first_job_on_page})


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
