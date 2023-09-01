import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
import subprocess
import json
from urllib.request import urlopen
from scrapy.crawler import CrawlerProcess

import temp
from scrapy_spiders import spider_control 
from scrapy_spiders.scrapy_spiders.spiders.software_eng_spider import SoftwareEngineerSpider, SWEPostSpider
from scrapy_spiders.scrapy_spiders.spiders.data_analyst_spider import DataAnalystSpider, DAPostSpider



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
            col6, col7 = st.columns([6,7],gap='large')
            self.plot_experience_graph(col6)
            self.plot_education_graph(col7)


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
        with col:
            col.header('Technologies')
            # plotly chart
            y_label = [tech for tech in temp.keywords['technology'].keys()]
            import random
            x_label = [random.randint(0,20) for i in y_label]
            fig = go.Figure(go.Bar(
                y=y_label,
                text=x_label,
                textposition='auto',
                textangle=0,
                orientation='h'
            ))
            fig.update_layout(yaxis={'categoryorder': 'category ascending'},height=600,margin={'t':0,'b':.7})
            fig.update_xaxes(visible=False)
            st.plotly_chart(fig, theme='streamlit', use_container_width=True)

    def plot_framework_graph(self, col):
        with col:
            col.header('Frameworks')
            # plotly chart
            y_label = [tech for tech in temp.keywords['frameworks'].keys()]
            import random
            x_label = [random.randint(0,20) for i in y_label]
            fig = go.Figure(go.Bar(
                y=y_label,
                text=x_label,
                textposition='auto',
                textangle=0,
                orientation='h'
            ))
            fig.update_layout(yaxis={'categoryorder': 'category ascending'},height=600,margin={'t':0})
            fig.update_xaxes(visible=False)
            st.plotly_chart(fig, theme='streamlit', use_container_width=True)

    def plot_education_graph(self, col):
        with col:
            col.header('Education')
            # plotly
            # df = px.data.tips()
            pie_names = temp.keywords['education'].keys()
            pie_values = temp.keywords['education'].values()
            fig = px.pie(values=pie_values,names=pie_names)
            fig.update_layout(legend_title=False)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, theme='streamlit', use_container_width=True)

    def plot_experience_graph(self, col):
        with col:
            col.header('Experience')
            # plotly chart
            y_label = [tech for tech in temp.keywords['frameworks'].keys()]
            import random
            x_label = [random.randint(0,20) for i in y_label]
            fig = go.Figure(go.Bar(
                # x=x_label,
                y=y_label,
                text=x_label,
                textposition='auto',
                textangle=0,
                orientation='h'
            ))
            fig.update_layout(yaxis={'categoryorder': 'category ascending'},margin={'t':0})
            st.plotly_chart(fig, theme='streamlit', use_container_width=True)
