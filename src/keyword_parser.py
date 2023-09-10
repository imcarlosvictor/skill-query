import os
import json
from datetime import date
# from export_feed.dashboard_data.keyword_data import data

# FILENAME = __file__
DIRECTORY_PATH = os.path.abspath(os.path.dirname(__file__))
SEARCH_POOL_FILE = os.path.abspath(os.path.join(DIRECTORY_PATH, 'keyword_search_pool.json'))
EXPORT_FEED_DIR = os.path.abspath(os.path.join(DIRECTORY_PATH, 'export_feed/SWE_post_spider/'))
TARGET_FILE = ''


today = date.today()
cur_year = today.strftime("%Y")
cur_month = today.strftime("%m")
cur_year_month = cur_year + '-' + cur_month

# Get scraped file for the current date
for file in os.listdir(EXPORT_FEED_DIR):
    if (file[:7] == cur_year_month):
        TARGET_FILE = os.path.join(EXPORT_FEED_DIR, file)

# Search for keywords
with open(TARGET_FILE, 'r') as jsonFile:
    scraped_data = json.load(jsonFile)

with open(SEARCH_POOL_FILE, 'r') as jsonFile:
    keywords = json.load(jsonFile)

for i in range(1, len(scraped_data)):
    for desc in scraped_data[i]['description']:
        for word in desc.split():
            if word.lower() in keywords['technology'].keys():
                keywords['technology'][word.lower()] += 1
            if word.lower() in keywords['frameworks'].keys():
                keywords['frameworks'][word.lower()] += 1
            if word.lower() in keywords['education'].keys():
                keywords['education'][word.lower()] += 1

# Create count for country
for i in range(1, len(scraped_data)):
    for word in scraped_data[i]['location'].split(', '):
        print(word.lower())
        if word.lower() in keywords['location'].keys():
            keywords['location'][word.lower()] += 1
            continue
        if word.lower() in keywords['usa_states']:
            keywords['usa_states'][word.lower()] += 1
keywords['location']['united states'] += sum(keywords['usa_states'].values())

# Add transformed data to dashboard data file
keyword_file_path = os.path.abspath(os.path.join(DIRECTORY_PATH, 'export_feed/dashboard_data/keyword_data.json'))
data_json_file = open(keyword_file_path)

with open(keyword_file_path, 'r') as json_file:
    data = json.load(json_file)
# Add year
if cur_year not in data.items():
    data[cur_year] = {}
# Add month
# if cur_month not in data[cur_year].items():
prev_month = cur_month
data[cur_year] = ({prev_month: keywords})
# data[cur_year][cur_month] = {} 
# Update JSON file with new changes
with open(keyword_file_path, 'w') as json_file:
    json.dump(data, json_file)
