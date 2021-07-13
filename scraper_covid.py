#visualization
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st
from PIL import Image
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
#scraping
import requests
from bs4 import BeautifulSoup
import json





def scrape_kini_labs():
    url = "https://newslab.malaysiakini.com/covid-19/en"
    html = requests.get(url).text
    bs = BeautifulSoup(html, 'lxml')
    script = bs.find('script', id='__NEXT_DATA__')
    json_object = json.loads(script.contents[0])
    props = json_object['props']
    page_props = props['pageProps']
    chartdata = page_props['chartData']
    data = chartdata

    # descending df
    chartdata_df = pd.DataFrame.from_dict(data)
    chartdata_df['date'] = pd.to_datetime(chartdata_df['date'], utc=False)
    chartdata_df.sort_values(by=['date'], ascending=False, inplace=True)
    chartdata_df['date'] = chartdata_df['date'].dt.strftime('%d %b %y')
    chartdata_df['Positivity rate'] = pd.to_numeric(chartdata_df['Positivity rate'], errors='coerce')
    chartdata_df['Positivity rate'] = (chartdata_df['newCase'] / chartdata_df['newTest']) * 100
    chartdata_df['Positivity rate'] = chartdata_df['Positivity rate'].round(2)
    chartdata_df['newTest'] = chartdata_df['newTest'].replace(0, np.nan)
    chartdata_df.to_csv('covid_data_updated_descending.csv', index=False)

    # ascending df
    chartdata_df2 = pd.DataFrame.from_dict(data)
    chartdata_df2['date'] = pd.to_datetime(chartdata_df2['date'], utc=False)
    chartdata_df2.sort_values(by=['date'], ascending=True, inplace=True)
    chartdata_df2['date'] = chartdata_df2['date'].dt.strftime('%d %b %y')
    chartdata_df2['Positivity rate'] = pd.to_numeric(chartdata_df2['Positivity rate'], errors='coerce')
    chartdata_df2['Positivity rate'] = (chartdata_df2['newCase'] / chartdata_df2['newTest']) * 100
    chartdata_df2['Positivity rate'] = chartdata_df2['Positivity rate'].round(2)
    chartdata_df2['newTest'] = chartdata_df2['newTest'].replace(0, np.nan)
    chartdata_df2.to_csv('covid_data_updated_ascending.csv', index=False)

    # updated text
    updated_date = bs.find('div', class_='jsx-2630654232 uk-text-small uk-text-center')
    with open('update_datetime.txt', 'w') as f:
        f.write(updated_date.text)

    # vaccine data
    vaccinedata = page_props['vaccineData']
    vaccine_df = pd.DataFrame.from_dict(vaccinedata)
    vaccine_df.to_csv('vaccine_data_updated_ascending.csv', index=False)

    # districts
    districtsdata = page_props['districtsData']
    district_df = pd.DataFrame.from_dict(districtsdata)
    district_df.to_csv('district_df.csv', index=False)

    # cluster
    clusterdata = page_props['clustersData']
    cluster_df = pd.DataFrame.from_dict(clusterdata)
    cluster_df.to_csv('cluster_df.csv', index=False)

    return 'update_datetime.txt', 'vaccine_data_updated_ascending.csv', 'district_df.csv', \
           'cluster_df.csv', 'covid_data_updated_descending.csv', 'covid_data_updated_ascending.csv'


if __name__=='__main__':
    scrape_kini_labs()