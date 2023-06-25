import streamlit as st


class Dashboard:
    def __init__(self):
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
            col1, col2 = st.columns([1,3])
            with col1:
                col1.header('Education')
                st.write("""
                    col1
                """)

            with col2:
                col2.header('Map Distribution')
                st.write("""
                   col2 
                """)

        bottom_container = st.container()
        bottom_container.write('container 2')
        with bottom_container:
            col3, col4, col5 = st.columns(3)
            with col3:
                col3.header('Hard Skills')
            with col4:
                col4.header('Technologies')
            with col5:
                col5.header('Experience')
