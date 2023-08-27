import os
import json


FILENAME = __file__
DIRECTORY_PATH = os.path.abspath(os.path.dirname(__file__))
target_file = os.path.abspath(os.path.join(DIRECTORY_PATH, './2023-08-27T06-09-20.json'))


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

for i in range(0, len(data)):
    for key, val in data[i]['keyword_count'].items():
        technologies[key] += val

print(technologies)
