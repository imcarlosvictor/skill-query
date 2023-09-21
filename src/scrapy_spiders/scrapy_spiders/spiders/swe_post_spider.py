import os
import sys
import re
import json
import w3lib.html
import scrapy
from datetime import date, datetime
from scrapy.spiders import CrawlSpider
from scrapy.linkextractors import LinkExtractor

# set path
FILENAME = __file__
DIRECTORY_PATH = os.path.abspath(os.path.dirname(__file__))
EXPORT_FEED_DIR = os.path.abspath(os.path.join(DIRECTORY_PATH, '../../../export_feed/'))
# PROXY_LIST_PATH = os.path.abspath(os.path.join(DIRECTORY_PATH, '../../proxy_list.txt'))

class SoftwareEngineerPostSpider(scrapy.Spider):
    """
    Extract data from the scraped links.
    """
    name = 'swe_post_spider'
    urls = []

    custom_settings = {
        'FEEDS': {
            f'{EXPORT_FEED_DIR}/%(name)s/%(time)s.json': {
                'format': 'json',
            }
        },
        'LOG_LEVEL': 'INFO',
        # 'LOG_ENABLED': False,
        'DOWNLOAD_DELAY': 1.4,
    }

    def start_requests(self):
        extract_target_file = self.get_latest_file_extract()
        try:
            with open(extract_target_file, 'rt') as f:
                urls = [url.strip() for url in f.readlines()]
            # visit links
            print('########################################')
            print('<< software engineer >> parsing job posts...')
            for url in urls[1:]:
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
        swe_export_feed_directory = f'{EXPORT_FEED_DIR}/software_engineer_link_spider/'
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
