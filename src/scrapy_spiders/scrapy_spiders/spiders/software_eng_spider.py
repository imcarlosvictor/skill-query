import os
import sys
import re
import json
import w3lib.html
import scrapy
from datetime import date, datetime
from scrapy.spiders import CrawlSpider
from scrapy.linkextractors import LinkExtractor

# from ...search_pool import technologies, libraries, education

# set path
FILENAME = __file__
DIRECTORY_PATH = os.path.abspath(os.path.dirname(__file__))
EXPORT_FEED_DIR = os.path.abspath(os.path.join(DIRECTORY_PATH, '../../../export_feed/'))


class SoftwareEngineerSpider(scrapy.Spider):
    """
    Scrape all job links from the given URL and store the data collected in a file.
    """
    name = 'SWE_link_spider'
    page_num = 0
    api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=software+developer+jobs+worldwide&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum='

    custom_settings = {
        'FEEDS': {
            f'{EXPORT_FEED_DIR}/%(name)s/%(time)s.csv': {
                'format': 'csv',
            }
        },
        'DOWNLOAD_DELAY': 1.2,
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
        print('########')
        print(len(jobs))
        print('########')

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


class SWEPostSpider(scrapy.Spider):
    """
    Extract data from the scraped links.
    """
    def __init__(self):
        self.name = 'SWE_post_spider'
        self.urls = []

    custom_settings = {
        'FEEDS': {
            f'{EXPORT_FEED_DIR}/%(name)s/%(time)s.json': {
                'format': 'json',
            }
        },
        'DOWNLOAD_DELAY': 1,
    }

    def start_requests(self):
        # get the latest extract file from the export feed directory
        extract_target_file = self.get_latest_file_extract()
        try:
            with open(extract_target_file, 'rt') as f:
                self.urls = [url.strip() for url in f.readlines()]
            # visit links
            for url in self.urls[1:]:
                yield scrapy.Request(url=url, callback=self.parse_posts)
        except FileNotFoundError as e:
            print('###################################################')
            print('# FileNotFoundError: No file matches current date #')
            print('###################################################')

    def parse_posts(self, response):
        """
        Extract data from job links.
        """
        ##############################################
        # Get Data
        job_location = response.css('span.topcard__flavor--bullet::text').get()
        job_location_clean = self.clean_text(job_location)

        job_role  = response.css('h1::text').get()
        job_role_clean = self.clean_text(job_role)

        seniority_level = response.css('span.description__job-criteria-text::text').get()
        seniority_level_clean = self.clean_text(seniority_level)

        employment_level = response.css('span.description__job-criteria-text::text').get()
        employment_level_clean = self.clean_text(employment_level)

        job_description = response.css('div.show-more-less-html__markup::text').get()
        job_description_list = response.css('div.show-more-less-html__markup ul li::text').getall()


        time_format = datetime.now()
        year = time_format.strftime('%Y')
        month = time_format.strftime('%m')
        yield {
            'year': year,
            'month': month,
            'location': job_location_clean,
            'role': job_role_clean,
            'seniority_level' : seniority_level_clean,
            'employment_type' : employment_level_clean,
            'description': job_description_list,
        }

    def clean_text(self, text):
        """
        Remove html tags from string.
        """
        html_pattern = re.compile('<.*?>')
        no_tag_text = re.sub(html_pattern, '', text)
        clean_text = re.sub('\n', '', no_tag_text)
        clean_text = clean_text.strip()
        return clean_text

    def get_latest_file_extract(self):
        """
        Find the most recent extract in the directory.
        """
        # get current date
        current_date = date.today()
        swe_export_feed_directory = f'{EXPORT_FEED_DIR}/SWE_link_spider/'
        # find file path of latest extract
        extract_target_file = ''
        for file in os.listdir(swe_export_feed_directory):
            # Find file with "YYYY-MM"
            if (file[:10] == str(current_date)):
                target_file = os.path.join(swe_export_feed_directory, file)
                if os.path.isfile(target_file):
                    extract_target_file = target_file
        print(extract_target_file)
        return extract_target_file
