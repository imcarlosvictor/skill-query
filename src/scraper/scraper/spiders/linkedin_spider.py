import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class LinkedinJobSpider(scrapy.Spider):
    name = 'linkedin_job_post_crawler'
    api_url = 'https://ca.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=junior+software+devloper&location=mississauga,on&geoId=100761630&trk=public_jobs_jobs-search-bar_search-submit&position1&pageNum='

    def start_requests(self):
        first_job_on_page = 0
        start_url = self.api_url + str(first_job_on_page)
        yield scrapy.Request(url=start_url, callback=self.parse_keywords, meta={'first_job_on_page': first_job_on_page})

    def parse_keywords(self, response):
        first_job_on_page = response.meta['first_job_on_page']
        jobs = response.css('li') # Job postings

        num_jobs_returned = len(jobs)
        print("******* Num Jobs Returned *******")
        print(num_jobs_returned)
        print('*****')

        job_item = {}
        for job in jobs:
            job_item['role'] = job.css('h3::text').get(default='n/a').strip()
            job_item['link'] = job.css('a::attr(href)').get(default='n/a')
            yield job_item

        ########## Request Next Page ##########
        if num_jobs_returned > 0:
            first_job_on_page = int(first_job_on_page) + 25
            next_url = self.api_url + str(first_job_on_page)
            yield scrapy.Request(url=next_url, callback=self.parse_keywords, meta={'first_job_on_page': first_job_on_page})


class LinkedinJobPostSpider(scrapy.Spider):
    name = 'linkedin_job_link_spider'
    allowed_domains = ['ca.linkedin.com']
