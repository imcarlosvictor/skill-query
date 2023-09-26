import os
import json
import pandas as pd

DASHBOARD_DIR = os.path.abspath(os.path.dirname(__file__))
WORLD_POLY_FILE = os.path.abspath(os.path.join(DASHBOARD_DIR, '../src/export_feed/dashboard_data/world_countries.json'))
KEYWORD_FILE = os.path.abspath(os.path.join(DASHBOARD_DIR, '../src/export_feed/dashboard_data/keyword_data.json'))
SEARCH_POOL_FILE = os.path.abspath(os.path.join(DASHBOARD_DIR, '../src/keyword_search_pool.json'))


geo_data = pd.read_json(WORLD_POLY_FILE)
# print(geo_data)
keyword_data = pd.read_json(KEYWORD_FILE)
# print(keyword_data)


# # for i in range(0, len(geo_data)):
#     # print(geo_data['country_polygon'][i]['properties']['name'].lower())

# # for j in range(0, len(keyword_data)):
# #     print(keyword_data['software_engineer'][2023]['09']['location'].keys())

# geo_country =  [ geo_data['country_polygon'][i]['properties']['name'].lower() for i in range(0, len(geo_data))]
# # print(geo_country)

# geo_polygon_val = [ geo_data['country_polygon'][i]['geometry']['coordinates'] for i in range(0, len(geo_data)) ]
# # print(geo_polygon_val)

# # keyword_country = [ country for country in keyword_data['software_engineer'][2023]['09']['location'].keys() ]
# # print(keyword_country)

# # TODO: replace countries from search pool with world_country countries, paired with its coordinates. Create another item with count and INT as the key and value, respectively.

# zipped = dict(zip(geo_country, geo_polygon_val))
# # print(zipped)

# location = {}
# for country, poly in zipped.items():
#     location[country] = {'polygon': poly, 'keyword_count': 0}
# print(location.items())

# # location = zipped
# # print(location['afghanistan'])
# # for country in location.items():
#     # country.update({'keyword_count': 0})
#     # loc = {geo_country[i]: geo_polygon_val[i], 'count': 0}
#     # location.append(loc)

# # print(location)
# # print(len(location))

# geo_data = ('http://geojson.xyz/naturalearth-3.3.0/ne_50m_admin_0_countries.geojson')


import requests

# response = requests.get('http://geojson.xyz/naturalearth-3.3.0/ne_50m_admin_0_countries.geojson')
# geo_data = response.json()

geoJSON_data = requests.get('https://raw.githubusercontent.com/python-visualization/folium-example-data/main/world_countries.json').json()

df = pd.DataFrame(geoJSON_data)
# print(df.head())


# print(type(df['features'][0]['properties']))
for i in range(0, len(df)):
    print(df['features'][i]['properties']['name'])

locations = {}
for i in range(0, len(df['features'])):
    country = df['features'][i]['properties']['name']
    locations[country] = {'keyword_count': 0}

print(locations)

with open(SEARCH_POOL_FILE, 'r') as jsonFile:
    keywords = json.load(jsonFile)

keywords['location'] = locations
print(len(keywords['location'].keys()))

with open(SEARCH_POOL_FILE, 'w') as jsonFile:
    json.dump(keywords, jsonFile)





