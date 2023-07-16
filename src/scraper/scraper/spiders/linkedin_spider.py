from pathlib import Path

import scrapy


class LinkedInSpider(scrapy.Spider):
    name = "linkedin"

    def start_requests(self):
        # urls = ['https://www.linkedin.com/jobs/']
        # urls = ['https://www.linkedin.com/jobs/search?trk=guest_homepage-basic_guest_nav_menu_jobs&position=1&pageNum=0']
        urls = ['https://www.linkedin.com/jobs/search?keywords=software+developer&location=Toronto%2C+Ontario%2C+Canada&geoId=100025096&trk=public_jobs_jobs-search-bar_search-submit']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        job_listings = response.xpath('/html/body/div[1]/div/main')
        xpath_results = response.xpath('//*[@id="main-content"]/section[2]/ul')
        # xpath_listings = response.xpath('//*[@id="main-content"]/section[2]/ul/li[1]/div')
        for posting in xpath_results:
            link = posting.xpath('//*[@id="main-content"]/section/ul/li[1]/div/a').get()
            job_title = posting.xpath('//*[@id="main-content"]/section/ul/li[1]/div/div[2]/h3').get()
            company = posting.css('#main-content > section > ul > li:nth-child(1) > div > div.base-search-card__info > h4 > a').get()
            company_link = posting.css('#main-content > section > ul > li:nth-child(1) > div > div.base-search-card__info > h4 > a').href()
            location = posting.xpath('//*[@id="main-content"]/section/ul/li[1]/div/div[2]/div/span').get()
            date_posted = posting.xpath('//*[@id="main-content"]/section/ul/li[1]/div/div[2]/div/time').get()

            job_post =  {
                'link': link,
                'job_title': job_title,
                'company': company,
                'company_link': company_link,
                'location': location,
                'date_posted': date_posted,
            }
            yield job_post