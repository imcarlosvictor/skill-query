import os
import sys
import json
import w3lib.html
import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.linkextractors import LinkExtractor

FILENAME = __file__
DIRECTORY_PATH = os.path.abspath(os.path.dirname(__file__))
DATA_EXTRACT_DIR = os.path.abspath(os.path.join(DIRECTORY_PATH, '../../../data_extracts'))
DATA_FILE = f'{DATA_EXTRACT_DIR}/data_links.csv'


class LinkedinSpider(scrapy.Spider):
    """Extract keywords from the job description for data visualization."""

    name = 'linkedin_spider'
    api_url = 'https://ca.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=junior+software+engineer&location=toronto&geoId=100761630&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum'
    # api_url = ''

    custom_settings = {
        'FEEDS': {
            DATA_FILE: {'format': 'csv'}
        }
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

    def get_job_details(self):
        """
        Extract data from job links.
        """

        # job_link_file = '/home/lucas/Documents/code/projects/python/skill-query/src/src/scrapy_spiders/data_extract/job_links.json'
        # with open(job_link_file, 'r') as f:
        #     for link in f:
        #         print(link)

        job_description = response.css('div.show-more-less-html__markup').get()
        output = w3lib.html.remove_tags(job_description)

        yield {
            'role': response.css('h1::text').get().strip(),
            'seniority_level' : response.css('span.description__job-criteria-text::text').get().strip(),
            'employment_type' : response.css('span.description__job-criteria-text').get().strip(),
            'description' : output
        }
