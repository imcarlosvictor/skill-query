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
        top_container.write('---------------------------------------------')
        with top_container:
            col1, col2 = st.columns([1,2],gap='large')
            with col1:
                col1.header('Technologies')
                # TEMPORARY CHART 
                chart_data = pd.DataFrame(
                    np.random.randn(20, 3),
                    columns=['a', 'b', 'c'])

                c = alt.Chart(chart_data).mark_circle().encode(
                    x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c'])

                st.altair_chart(c, use_container_width=True)

            with col2:
                col2.header('Job Opening Distribution')
                # self.PlotMapData()

        bottom_container = st.container()
        bottom_container.write('---------------------------------------------')
        with bottom_container:
            col3, col4, col5 = st.columns(3,gap='large')
            with col3:
                col3.header('Libraries')
                # TEMPORARY CHART 
                chart_data = pd.DataFrame(
                    np.random.randn(20, 3),
                    columns=['a', 'b', 'c'])

                c = alt.Chart(chart_data).mark_circle().encode(
                    x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c'])

                st.altair_chart(c, use_container_width=True)
            with col4:
                col4.header('Education')
                # TEMPORARY CHART 
                chart_data = pd.DataFrame(
                    np.random.randn(20, 3),
                    columns=['a', 'b', 'c'])

                c = alt.Chart(chart_data).mark_circle().encode(
                    x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c'])

                st.altair_chart(c, use_container_width=True)
            with col5:
                col5.header('Experience')
                # TEMPORARY CHART 
                chart_data = pd.DataFrame(
                    np.random.randn(20, 3),
                    columns=['a', 'b', 'c'])

                c = alt.Chart(chart_data).mark_circle().encode(
                    x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c'])

                st.altair_chart(c, use_container_width=True)

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

    def plot_map(self):
        # implement pydeck map
        st.map() 

