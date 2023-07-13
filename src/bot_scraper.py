import scrapy



class LinkedinScraper(scrapy.Spider):
        name = 'Linkedin Spider'
        start_urls = [self.URL]

    def __init__(self, url):
        self.URL = url

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
