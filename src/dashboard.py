import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import subprocess
import json
from urllib.request import urlopen
from scrapy.crawler import CrawlerProcess

from scrapy_spiders import run_spider
from scrapy_spiders.scrapy_spiders.spiders.linkedin_spider import SoftwareEngineerSpider, DataAnalystSpider



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

        search_btn = st.sidebar.button('Show', use_container_width=True)


        # ############ Dashboard ############
        top_container = st.container()
        with top_container:
            col1, col2 = st.columns([1,2],gap='large')
            self.plot_technology_graph(col1)
            self.plot_map(col2)

        bottom_container = st.container()
        with bottom_container:
            col3, col4, col5 = st.columns(3,gap='large')
            self.plot_library_graph(col3)
            self.plot_education_graph(col4)
            self.plot_experience_graph(col5)


        ############ Call Spider ############
        # run_spider.start_spider()
        #####################################

    def plot_map(self, col):
        with col:
            col.header('Job Opening Distribution')
            # implement pydeck map
            st.map()

    def plot_technology_graph(self, col):
        with col:
            col.header('Technologies')
            # TEMPORARY CHART 
            chart_data = pd.DataFrame(
                np.random.randn(20, 3),
                columns=['a', 'b', 'c'])

            c = alt.Chart(chart_data).mark_circle().encode(
                x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c'])

            st.altair_chart(c, use_container_width=True)

    def plot_library_graph(self, col):
        with col:
            col.header('Libraries')
            # TEMPORARY CHART 
            chart_data = pd.DataFrame(
                np.random.randn(20, 3),
                columns=['a', 'b', 'c'])

            c = alt.Chart(chart_data).mark_circle().encode(
                x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c'])

            st.altair_chart(c, use_container_width=True)

    def plot_education_graph(self, col):
        with col:
            col.header('Education')
            # TEMPORARY CHART 
            chart_data = pd.DataFrame(
                np.random.randn(20, 3),
                columns=['a', 'b', 'c'])

            c = alt.Chart(chart_data).mark_circle().encode(
                x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c'])

            st.altair_chart(c, use_container_width=True)

    def plot_experience_graph(self, col):
        with col:
            col.header('Experience')
            # TEMPORARY CHART 
            chart_data = pd.DataFrame(
                np.random.randn(20, 3),
                columns=['a', 'b', 'c'])

            c = alt.Chart(chart_data).mark_circle().encode(
                x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c'])

            st.altair_chart(c, use_container_width=True)
