import os
import json
import subprocess
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
from scrapy.crawler import CrawlerProcess
from datetime import datetime

# from scrapy_spiders import spider_control 
from scrapy_spiders.scrapy_spiders.spiders.software_eng_spider import SoftwareEngineerSpider, SWEPostSpider
from scrapy_spiders.scrapy_spiders.spiders.data_analyst_spider import DataAnalystSpider, DAPostSpider


FILENAME = __file__
DIRECTORY_PATH = os.path.abspath(os.path.dirname(__file__))
DASH_DATA_TARGET_FILE = os.path.abspath(os.path.join(DIRECTORY_PATH, 'export_feed/dashboard_data/keyword_data.json'))


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

        location_option = st.sidebar.selectbox(
            'Location',
            ('Canada', 'USA')
        )

        year_option = st.sidebar.selectbox(
            'Year',
            ('2023',)
        )

        show_btn = st.sidebar.button('Show', use_container_width=True)


        # ############ Dashboard ############
        top_container = st.container()
        with top_container:
            self.plot_map()

        mid_container = st.container()
        with mid_container:
            col3, col4 = st.columns([3,4], gap='large')
            self.plot_technology_graph(col3)
            self.plot_framework_graph(col4)

        bottom_container = st.container()
        with bottom_container:
            col5, col6 = st.columns([5,6],gap='large')
            # self.plot_experience_graph(col5)
            self.plot_education_graph(col6)


        ############ Call Spider ############
        if show_btn:
            # run_spider.start_spider()
            # st.write('Why hello there')
            print('hello there')
            # pass
        #####################################

    def plot_map(self):
        st.map()

    def plot_technology_graph(self, col):
        year, month = self.get_date()
        # Load data
        with open(DASH_DATA_TARGET_FILE, 'r') as jsonFile:
            data = json.load(jsonFile)
        # plotly chart
        with col:
            col.header('Technologies')
            y_label = [key for key in data[year][month]['technology'].keys()]
            x_label = [val for val in data[year][month]['technology'].values()]
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
            fig.update_traces(marker_color='#ff1745')
            st.plotly_chart(fig, theme='streamlit', use_container_width=True)

    def plot_framework_graph(self, col):
        year, month = self.get_date()
        # load data
        with open(DASH_DATA_TARGET_FILE, 'r') as jsonFile:
            data = json.load(jsonFile)
        # plotly chart
        with col:
            col.header('Frameworks')
            y_label = [y_key for y_key in data[year][month]['frameworks'].keys()]
            x_label = [x_val for x_val in data[year][month]['frameworks'].values()]
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
            fig.update_traces(marker_color='#ff1745')
            st.plotly_chart(fig, theme='streamlit', use_container_width=True)

    def plot_education_graph(self, col):
        year, month = self.get_date()
        # load data
        with open(DASH_DATA_TARGET_FILE, 'r') as jsonFile:
            data = json.load(jsonFile)
        # plotly
        with col:
            col.header('Education')

            names = [keys for keys in data[year][month]['education'].keys()]
            values = [values for values in data[year][month]['education'].values()]
            fig = px.pie(values=values, names=names, color_discrete_sequence=px.colors.sequential.RdBu)
            fig.update_layout(legend_title=False)
            fig.update_traces(textposition='inside', textinfo='percent+label', showlegend=False)
            st.plotly_chart(fig, theme='streamlit', use_container_width=True)

    def plot_experience_graph(self, col):
        year, month = self.get_date()
        # load data
        with open(DASH_DATA_TARGET_FILE, 'r') as jsonFile:
            data = json.load(jsonFile)
        # plotly
        with col:
            col.header('Experience')
            y_key = [y_key for y_key in data[year][month]['experience'].keys()]
            x_val = [x_val for x_val in data[year][month]['experience'].values()]
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
            fig.update_traces(marker_color='#ff1745')
            st.plotly_chart(fig, theme='streamlit', use_container_width=True)

    def get_date(self):
        now = datetime.now()
        year = now.strftime('%Y')
        month = now.strftime('%m')
        return year, month
