import os
from datetime import datetime, timedelta
from textwrap import dedent

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.decorators import dag, task

# from ..SkillQuery.src.src.spider_control import SpiderControl

DIRECTORY_PATH = os.path.abspath(os.path.dirname(__file__))
SPIDER_DIRECTORY_PATH = os.path.abspath(os.path.join(DIRECTORY_PATH, '../SkillQuery/src/src/scrapy_spiders/scrapy_spiders/spiders/'))
KEYWORD_PARSER_PATH = os.path.abspath(os.path.join(DIRECTORY_PATH, '../SkillQuery/src/src/'))

default_args = {
    "owner": "Lucas",
    "depends_on_past": False,
    "email": ["airflow@example.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 4,
    "retry_delay": timedelta(minutes=2),
}

# Software Engineer DAG
with DAG(
    dag_id="skill_query_software_engineer",
    default_args=default_args,
    description="Spiders for Skill Query",
    schedule=timedelta(days=1),
    start_date=datetime(2023, 9, 19),
    catchup=False,
) as dag:

    # TODO: Set python spiders
    # t1, t2 and t3 are examples of tasks created by instantiating operators
    t1 = BashOperator(
        task_id="swe_link_spider",
        bash_command=f"cd {SPIDER_DIRECTORY_PATH} && scrapy crawl software_engineer_link_spider",
    )

    t2 = BashOperator(
        task_id="swe_post_spider",
        depends_on_past=False,
        bash_command=f"cd {SPIDER_DIRECTORY_PATH} && scrapy crawl swe_post_spider",
    )

    t3 = BashOperator(
        task_id="keyword_spider",
        depends_on_past=False,
        bash_command=f"cd {KEYWORD_PARSER_PATH} && python keyword_parser.py software_eng",
    )

    # Task Dependencies
    t1 >> t2 >> t3

# Data Analyst DAG
with DAG(
    dag_id="skill_query_data_analyst",
    default_args=default_args,
    description="Spiders for Skill Query",
    schedule=timedelta(days=1),
    start_date=datetime(2023, 9, 19),
    catchup=False,
) as dag:

    # TODO: Set python spiders
    # t1, t2 and t3 are examples of tasks created by instantiating operators
    t1 = BashOperator(
        task_id="da_link_spider",
        bash_command=f"cd {SPIDER_DIRECTORY_PATH} && scrapy crawl data_analyst_link_spider",
    )

    t2 = BashOperator(
        task_id="da_post_spider",
        depends_on_past=False,
        bash_command=f"cd {SPIDER_DIRECTORY_PATH} && scrapy crawl da_post_spider",
    )

    t3 = BashOperator(
        task_id="keyword_spider",
        depends_on_past=False,
        bash_command=f"cd {KEYWORD_PARSER_PATH} && python keyword_parser.py data_analyst",
    )

    # Task Dependencies
    t1 >> t2 >> t3
