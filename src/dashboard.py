import streamlit as st

from urllib.request import urlopen
import pandas as pd
import numpy as np
import altair as alt
import json


class Dashboard:
    def __init__(self):
        # Increase the layout to span the entire screen
        st.set_page_config(layout='wide') 
        self.CreateLayout()

    def CreateLayout(self):
        # Streamlit sidebar
        st.sidebar.title('Skill Query')
        # User inputs
        job_role_input = st.sidebar.text_input(
            'Job Role',
            key='0',
            placeholder='e.g. Software Engineer, Data Analyst, etc.',
        )
        country_input = st.sidebar.text_input(
            'Country',
            key='1',
            placeholder='City, state, or Zip code',
        )
        region_input = st.sidebar.text_input(
            'Region',
            key='2',
        )
        # Search Button
        st.sidebar.button('Apply')

        # Dashboard
        top_container = st.container()
        top_container.write('container 1')
        with top_container:
            col1, col2 = st.columns([1,2],gap='large')
            with col1:
                col1.header('Hard SKills')
                # TEMPORARY CHART 
                chart_data = pd.DataFrame(
                    np.random.randn(20, 3),
                    columns=['a', 'b', 'c'])

                c = alt.Chart(chart_data).mark_circle().encode(
                    x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c'])

                st.altair_chart(c, use_container_width=True)

            with col2:
                col2.header('Map Distribution')
                self.PlotMapData()

        bottom_container = st.container()
        bottom_container.write('container 2')
        with bottom_container:
            col3, col4, col5 = st.columns(3,gap='large')
            with col3:
                col3.header('Technologies')
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

    def PlotMapData(self):
        # implement pydeck map
        st.map() 

