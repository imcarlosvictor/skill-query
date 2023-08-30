import os
import json


FILENAME = __file__
DIRECTORY_PATH = os.path.abspath(os.path.dirname(__file__))
# target_file = os.path.abspath(os.path.join(DIRECTORY_PATH, 'export_feed/SWE_post_spider/2023-08-28T09-13-20.json'))
target_file = os.path.abspath(os.path.join(DIRECTORY_PATH, 'export_feed/SWE_post_spider/2023-08-29T03-16-07.json'))


f = open(target_file)
data = json.load(f)


technologies = {
    'python': 0,
    'c++': 0,
    'javascript': 0,
    'java': 0,
    'php': 0,
    'ruby': 0,
    'typescript': 0,
    'rust': 0,
    'dart': 0,
    'lua': 0,
    'swift': 0,
    'scala': 0,
    'kotlin': 0,
    'matlab': 0,
    'c#': 0,
    'haskell': 0,
    'assembly': 0,
    'sql': 0,
    'nosql': 0,
    'linux': 0,
}

keywords = {
    'technology': {
        'python': 0,
        'c++': 0,
        'javascript': 0,
        'java': 0,
        'php': 0,
        'ruby': 0,
        'typescript': 0,
        'rust': 0,
        'dart': 0,
        'lua': 0,
        'swift': 0,
        'scala': 0,
        'kotlin': 0,
        'matlab': 0,
        'c#': 0,
        'haskell': 0,
        'assembly': 0,
        'sql': 0,
        'nosql': 0,
        'linux': 0,
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

# for i in range(0, len(data)):
    # for key, val in data[i]['tech_keyword_count'].items():
    #     technologies[key] += val

print(keywords)
