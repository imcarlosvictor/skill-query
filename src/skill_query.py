import dashboard

from search_pool import *
from scraper.scraper.spiders.linkedin_spider import LinkedinKeywordSpider

def main():
    db = dashboard.Dashboard()
    linkedin_url = db.get_URL()

    # print(programming_lang)

if __name__ == '__main__':

    main()
