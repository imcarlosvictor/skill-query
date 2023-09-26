import requests
import pandas as pd

geoJSON_data = requests.get('https://raw.githubusercontent.com/python-visualization/folium-example-data/main/world_countries.json').json()

df = pd.DataFrame(geoJSON_data)
print(df.head())


# print(type(df['features'][0]['properties']))
for i in range(1, len(df)):
    print(df['features'][i]['properties']['name'])
