import os
import json
import subprocess
import folium
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
from streamlit_folium import st_folium
from urllib.request import urlopen
from scrapy.crawler import CrawlerProcess
from datetime import datetime

# from scrapy_spiders import spider_control 
from scrapy_spiders.scrapy_spiders.spiders.software_eng_spider import SoftwareEngineerSpider
from scrapy_spiders.scrapy_spiders.spiders.data_analyst_spider import DataAnalystSpider
from scrapy_spiders.scrapy_spiders.spiders.swe_post_spider import SoftwareEngineerPostSpider
from scrapy_spiders.scrapy_spiders.spiders.da_post_spider import DataAnalystPostSpider


FILENAME = __file__
DIRECTORY_PATH = os.path.abspath(os.path.dirname(__file__))
DASH_DATA_TARGET_FILE = os.path.abspath(os.path.join(DIRECTORY_PATH, 'export_feed/dashboard_data/keyword_data.json'))
GEO_DATA_TARGET_FILE = os.path.abspath(os.path.join(DIRECTORY_PATH, 'export_feed/dashboard_data/world_countries.json'))


class Dashboard:
    def __init__(self):
        # Increase the layout to span the entire screen
        st.set_page_config(page_title='Skill Query',layout='wide')
        self.URL = ''
        self.create_layout()

    def create_layout(self):
        # ############ Sidebar ############
        st.sidebar.title('Skill Query')

        job_role_option = st.sidebar.selectbox(
            'Job Role',
            ('Software Engineer', 'Data Analyst')
        )

        # location_option = st.sidebar.selectbox(
        #     'Location',
        #     ('Canada', 'USA')
        # )

        year_option = st.sidebar.selectbox(
            'Year',
            ('2023',)
        )

        # show_btn = st.sidebar.button('Show', use_container_width=True)


        # ############ Dashboard ############
        role = ''
        if job_role_option == 'Software Engineer':
            role = 'software_engineer'
        elif job_role_option == 'Data Analyst':
            role = 'data_analyst'

        top_container = st.container()
        with top_container:
            self.plot_map()

        mid_container = st.container()
        with mid_container:
            col3, col4 = st.columns([3,4], gap='large')
            self.plot_technology_graph(col3, role)
            self.plot_framework_graph(col4, role)

        bottom_container = st.container()
        with bottom_container:
            col5, col6 = st.columns([5,6],gap='large')
            # self.plot_experience_graph(col5)
            self.plot_education_graph(col6, role)

    def plot_map(self):
        year, month = self.get_date()

        # Plot polygons on folium map
        geo_data = ('http://geojson.xyz/naturalearth-3.3.0/ne_50m_admin_0_countries.geojson')
        # Plot data
        keyword_data_df= pd.read_json(DASH_DATA_TARGET_FILE)
        countries_pd = list(keyword_data_df['software_engineer'][int(year)][month]['location'].keys())
        countries_pd = [ country.capitalize() for country in countries_pd ]
        country_keyword_count_pd = []
        for country in countries_pd:
            country_keyword_count_pd.append(keyword_data_df['software_engineer'][int(year)][month]['location'][country.lower()]['keyword_count'])

        zip_countries_keywordcount = list(zip(countries_pd, country_keyword_count_pd))
        for c,k in zip_countries_keywordcount:
            print(f'{c} || {k}')
        # print(zip_countries_keywordcount)
        # print(type(zip_countries_keywordcount))
        # print(country_keyword_count_pd)
        # print(zip_countries_keywordcount)

        # data = {'countries': countries_pd , 'values': country_keyword_count_pd}
        # print(type(countries_pd))
        # print(type(country_keyword_count_pd))

        # for key,val in data.items():
        #     for v in data[key]:
        #         if pd.isnull(v):
        #             print('True')
        #     for v in data[val]:
        #         if pd.isnull(v):
        #             print('True')

        m = folium.Map(location=[40,80], control_scale=True, zoom_start=2)
        folium.Choropleth(
            geo_data=geo_data,
            # data=data,
            column=[countries_pd, country_keyword_count_pd],
            key_on='feature.properties.name',
            fill_color='OrRd',
            line_color='#0000',
            name='Job Posting Distribution',
            legend_name='Job Openings',
        ).add_to(m)
        st_data = st_folium(m, width=1900)

    def plot_technology_graph(self, col, job_role):
        with col:
            col.header('Technologies')
            y_label, x_label = self.get_data(job_role, 'technology')
            y_label = y_label
            x_label = x_label
            fig = go.Figure(go.Bar(
                x=x_label,
                y=y_label,
                text=x_label,
                textposition='auto',
                textangle=0,
                orientation='h'
            ))
            fig.update_xaxes(visible=False)
            fig.update_yaxes(categoryorder='total ascending')
            fig.update_layout(height=600,margin={'t':0,'b':.7})
            fig.update_traces(marker_color='#ff0044')
            st.plotly_chart(fig, theme='streamlit', use_container_width=True)

    def plot_framework_graph(self, col, job_role):
        with col:
            col.header('Frameworks')
            y_label, x_label = self.get_data(job_role, 'frameworks')
            y_label = y_label
            x_label = x_label
            fig = go.Figure(go.Bar(
                x=x_label,
                y=y_label,
                text=x_label,
                textposition='auto',
                textangle=0,
                orientation='h'
            ))
            fig.update_xaxes(visible=False)
            fig.update_yaxes(categoryorder='total ascending')
            fig.update_layout(height=600,margin={'t':0})
            fig.update_traces(marker_color='#ff0044')
            st.plotly_chart(fig, theme='streamlit', use_container_width=True)

    # TODO:
    def plot_education_graph(self, col, job_role):
        with col:
            col.header('Education')
            y_label, x_label = self.get_data(job_role, 'education')
            names = y_label
            values = x_label
            fig = px.pie(values=values, names=names, color_discrete_sequence=px.colors.sequential.RdBu)
            fig.update_layout(legend_title=False)
            fig.update_traces(textposition='inside', textinfo='percent+label', showlegend=False)
            st.plotly_chart(fig, theme='streamlit', use_container_width=True)

    # TODO: Plot heatmap
    def plot_experience_graph(self, col, job_role):
        with col:
            col.header('Experience')
            y_label, x_label = self.get_data(job_role, 'experience')
            y_key = y_label
            x_val = x_label
            fig = go.Figure(go.Bar(
                # x=x_label,
                y=y_label,
                text=x_label,
                textposition='auto',
                textangle=0,
                orientation='h'
            ))
            fig.update_xaxes(visible=False)
            fig.update_yaxes(categoryorder='total ascending')
            fig.update_layout(height=600,margin={'t':0})
            fig.update_traces(marker_color='#ff0044')
            st.plotly_chart(fig, theme='streamlit', use_container_width=True)

    def get_date(self):
        now = datetime.now()
        year = now.strftime('%Y')
        month = now.strftime('%m')
        return year, month

    def get_data(self, job_role: str, data_field: str):
        year, month = self.get_date()
        # Load data
        with open(DASH_DATA_TARGET_FILE, 'r') as jsonFile:
            data = json.load(jsonFile)

        y_label = [key for key in data[job_role][year][month][data_field].keys()]
        x_label = [val for val in data[job_role][year][month][data_field].values()]

        return y_label, x_label

