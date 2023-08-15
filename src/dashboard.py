import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import json

from urllib.request import urlopen
from scrapy.crawler import CrawlerProcess
from scrapy_spiders.scrapy_spiders.spiders.linkedin_spider import LinkedinSpider

import spider


class Dashboard:
    def __init__(self):
        # Increase the layout to span the entire screen
        st.set_page_config(page_title='Skill Query',layout='wide')
        self.URL = ''
        self.create_layout()

    def create_layout(self):
        # ------------ Sidebar ------------
        st.sidebar.title('Skill Query')
        # User inputs
        job_role_input = st.sidebar.text_input(
            'Job Role',
            key='0',
            placeholder='Software Engineer, Data Analyst',
        )
        experience_input = st.sidebar.text_input(
            'Experience Level',
            key='1',
            placeholder='Junior, Mid-Senior, Senior',
        )
        location_input = st.sidebar.text_input(
            'Location',
            key='2',
            placeholder='City, state, or Zip code',
        )
        # Search Button
        apply_search_btn = st.sidebar.button('Apply')


        # ------------ Dashboard ------------
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

        # Create custom linkedin URL based on user inputs
        if apply_search_btn:
            # Role input
            job_role_input = job_role_input.replace(' ', '+')
            # EXP input
            experience_input = experience_input.replace(' ', '+')
            # Location input
            location_input = location_input.replace(' ', '')
            # Format inputs for URL construction
            user_inputs = [input.lower() for input in [experience_input, job_role_input, location_input]]

            # Create custom URL
            if job_role_input:
                self.URL = f'https://ca.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={user_inputs[1]}'
                if experience_input:
                    self.URL = f'https://ca.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={user_inputs[0]}+{user_inputs[1]}'
                if location_input:
                    self.URL = f'https://ca.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={user_inputs[0]}+{user_inputs[1]}&location={user_inputs[2]}'
                self.URL += '&geoId=100761630&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum='

            # update url in linkedin spider
            spider.crawl_linkedin(self.URL)

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
