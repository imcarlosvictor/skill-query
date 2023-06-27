import scrapy


class LinkedinSpider(scrapy.Spider):
    name = 'Linkedin Spider'
    start_urls = ['https://www.linkedin.com/jobs/']

    def parse(self, response):
        pass

    def parse_URL(self, url):
        

    def scrape_tech(self):
        pass

    def scrape_library(self):
        pass
        
    def scrape_education(self):
        pass

    def scrape_location(self):
        pass

    def scrape_date(self):
        pass
