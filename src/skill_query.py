import dashboard
import bot_scraper
from search_pool import *

def main():
    db = dashboard.Dashboard()
    linkedin_url = db.get_URL()

    scraper = LinkedinScraper(linkedin_url)
    scraper.getURL()
    # print(programming_lang)


if __name__ == '__main__':
    main()
