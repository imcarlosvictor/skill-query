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


class JobPostSpider(scrapy.Spider):
    """
    Extract data from the scraped links.
    """

    name = 'post_spider'

    custom_settings = {
        'FEEDS': {
            f'{EXPORT_FEED_DIR}/%(name)s/%(name)s_%(time)s': {
                'format': 'csv',
            }
        }
    }

    def parse_job_details(self):
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


link_extracts = LINK_EXTRACT_DIR + '19-'
with open(link_extracts, 'r') as f:
    for link in f:
        print(link)
