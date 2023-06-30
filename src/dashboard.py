import streamlit as st

from urllib.request import urlopen
import pandas as pd
import numpy as np
import altair as alt
import json


class Dashboard:
    def __init__(self):
        # Increase the layout to span the entire screen
        st.set_page_config(page_title='Skill Query',layout='wide') 
        self.create_layout()
        self.URL = ''

    def create_layout(self):
        # Streamlit sidebar
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


        # Dashboard
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
            # Format inputs for URL construction
            user_inputs = [input.lower() for input in [job_role_input, experience_input, location_input]]
            # EXP input
            user_inputs[0] = user_inputs[0].replace(' ', '-')
            # Location input
            user_inputs[2] = user_inputs[2].replace(' ', '').replace(',','-')

            # Create custom URL
            if job_role_input:
                self.URL = f'https://www.linkedin.com/jobs/{user_inputs[0]}'
                if experience_input:
                    self.URL = f'https://www.linkedin.com/jobs/{user_inputs[1]}-{user_inputs[0]}'
                if location_input:
                    self.URL += '-' + user_inputs[2]
                self.URL += '-jobs'
            print(self.URL)

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

    def get_URL(self):
        return self.URL

