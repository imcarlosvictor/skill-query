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
        num_jobs_returned = len(jobs)

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
        self.urls = []

    custom_settings = {
        'FEEDS': {
            f'{EXPORT_FEED_DIR}/%(name)s/%(time)s.json': {
                'format': 'json',
            }
        }
    }

    def start_requests(self):
        # get latest extract file
        extract_target_file = self.get_latest_file_extract()
        with open(extract_target_file, 'rt') as f:
            self.urls = [url.strip() for url in f.readlines()]
        # scrape through links
        for url in self.urls[1:]:
            yield scrapy.Request(url=url, callback=self.parse_posts)

    def parse_posts(self, response):
        """
        Extract data from job links.
        """
        ##############################################
        # Get Data
        job_role  = response.css('h1::text').get()
        job_role_clean = self.clean_text(job_role)

        seniority_level = response.css('span.description__job-criteria-text::text').get()
        seniority_level_clean = self.clean_text(seniority_level)

        employment_level = response.css('span.description__job-criteria-text::text').get()
        employment_level_clean = self.clean_text(employment_level)

        ##############################################
        ##############################################
        # Extract keywords for tables
        job_description = response.css('div.show-more-less-html__markup ul li::text').getall()
        technology = {
            'python': 0,
            'r': 0,
            'java': 0,
            'scala': 0,
            'matlab': 0,
            'sql': 0,
            'nosql': 0,
            'linux': 0,
            'jupyter': 0,
            'tableau': 0,
            'bi': 0,
            'airflow': 0,
            'spark': 0,
            'hive': 0,
            'hadoop': 0,
            'sas': 0,
            'excel': 0,
        }

        for list in job_description:
            new_list = list.split()
            for word in new_list:
               if word.lower() in technologies.keys():
                   technologies[word.lower()] += 1

        ##############################################
        # library keyword extract 
        library = {
            'tensorflow': 0,
            'pytorch': 0,
            'theano': 0,
            'opencv': 0,
            'requests': 0,
            'scikit-learn': 0,
            'numpy': 0,
            'keras': 0,
            'scipy': 0,
            'pandas': 0,
            'requests': 0,
            'pillow': 0,
            'scrapy': 0,
            'selenium': 0,
            'kivy': 0,
            'theano': 0,
            'matplotlib': 0,
            'seaborn': 0,
            'beautifulsoup': 0,
        }

        for list in job_description:
            new_list = list.split()
            for word in new_list:
               if word.lower() in libraries.keys():
                   libraries[word.lower()] += 1

        ##############################################
        # Education keyword extract
        education = {
            'bachelor': 0,
            'masters': 0,
            'phd': 0,
        }

        for list in job_description:
            new_list = list.split()
            for word in new_list:
               if word.lower() in education.keys():
                   education[word.lower()] += 1
        ##############################################
        ##############################################

        yield {
            'role': job_role_clean,
            'seniority_level' : seniority_level_clean,
            'employment_type' : employment_level_clean,
            'tech_keyword_count': technology,
            'library_keyword_count': library,
            'education_keyword_count': education,
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
        current_date = datetime.date.today()
        swe_export_feed_directory = f'{EXPORT_FEED_DIR}/SWE_role_spider/'
        # find file path of latest extract to scrape
        extract_target_file = ''
        for file in os.listdir(swe_export_feed_directory):
            if (file[:10] == str(current_date)):
                target_file = os.path.join(swe_export_feed_directory, file)
                if os.path.isfile(target_file):
                    extract_target_file = target_file
        return extract_target_file
