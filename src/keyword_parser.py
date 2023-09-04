import os
import json
from datetime import date
# from export_feed.dashboard_data.keyword_data import data

FILENAME = __file__
DIRECTORY_PATH = os.path.abspath(os.path.dirname(__file__))
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

TARGET_FILE = os.path.abspath(os.path.join(DIRECTORY_PATH, 'export_feed/SWE_post_spider/2023-08-31T00-21-11.json'))

# TODO: Parse data and add it to the corresponding year and month in the dicitonary
f = open(TARGET_FILE)
data = json.load(f)

keywords = {
    'technology': {
        'assembly': 0,
        'aws': 0,
        'c++': 0,
        'c/c++': 0,
        'c#': 0,
        'dart': 0,
        'go': 0,
        'git': 0,
        'graphql': 0,
        'haskell': 0,
        'js': 0,
        'javascript': 0,
        'java': 0,
        'kotlin': 0,
        'kubernetes': 0,
        'linux': 0,
        'lua': 0,
        'matlab': 0,
        'mongodb': 0,
        'mysql': 0,
        'nosql': 0,
        'python': 0,
        'php': 0,
        'postgresql': 0,
        'ruby': 0,
        'rust': 0,
        'swift': 0,
        'scala': 0,
        'sql': 0,
        'typescript': 0,
    },
    'library': {
        'tensorflow': 0,
        'pytorch': 0,
        'theano': 0,
        'opencv': 0,
        'requests': 0,
        'scikit-learn': 0,
        'numpy': 0,
        'keras': 0,
        'scipy': 0,
        'pandas': 0,
        'requests': 0,
        'pillow': 0,
        'scrapy': 0,
        'selenium': 0,
        'kivy': 0,
        'theano': 0,
        'matplotlib': 0,
        'seaborn': 0,
        'beautifulsoup': 0,
    },
    'frameworks': {
        '.net': 0,
        'angular': 0,
        'bootstrap': 0,
        'django': 0,
        'flask': 0,
        'jquery': 0,
        'laravel': 0,
        'next.js': 0,
        'node.js': 0,
        'node': 0,
        'ruby on rails': 0,
        'redis': 0,
        'react': 0,
        'spring': 0,
        'spark': 0,
        'vue': 0,
    },
    'education': {
        'bachelor': 0,
        'masters': 0,
        'phd': 0,
    }
}

for i in range(0, len(data)):
    for key, val_dict in data[i]['keywords'].items():
        for kword, val in val_dict.items():
            # print(f'key:{kword}  |  val:{val}')
            keywords[key][kword] += val


# TODO: Create a dictionary with year (2023) and month (01,02) as keys
keyword_file_path = os.path.abspath(os.path.join(DIRECTORY_PATH, 'export_feed/dashboard_data/keyword_data.json'))
data_json_file = open(keyword_file_path)

with open(keyword_file_path, 'r') as json_file:
    data = json.load(json_file)
# Add year
if cur_year not in data.items():
    data[cur_year] = {}
# Add month
# if cur_month not in data[cur_year].items():
prev_month = str(int(cur_month)-1)
data[cur_year] = ({prev_month: keywords}) 
# data[cur_year][cur_month] = {} 
# Update JSON file with new changes
with open(keyword_file_path, 'w') as json_file:
    json.dump(data, json_file)

print(data)
