import scrapy


class LinkedinKeywordSpider(scrapy.Spider):
    name = 'linkedin_crawler'
    # url = ''
    # api_url = 'https://ca.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/software-engineer-jobs-toronto-on?start=25'
    url = 'https://ca.linkedin.com/jobs/search?keywords=junior+software+devloper&location=mississauga,on&geoId=100761630&trk=public_jobs_jobs-search-bar_search-submit'


    def start_requests(self):
        first_job_on_page = 0
        url = self.url + str(first_job_on_page)
        yield scrapy.Request(url=url, callback=self.parse_keywords, meta={'first_job_on_page': first_job_on_page})

    def parse_keywords(self, response):
        jobs = response.css('li') # Job postings

        num_jobs_returned = len(jobs)
        print("******* Num Jobs Returned *******")
        print(num_jobs_returned)
        print('*****')

        job_item = {}
        for job in jobs:
            job_item['role'] = job.css('a::text').get(default='n/a').strip()
            job_item['link'] = job.css('a::attr(href)').get(default='n/a')
            yield job_item
