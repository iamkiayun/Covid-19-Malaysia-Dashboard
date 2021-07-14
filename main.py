
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
from view_script import *
from datetime import datetime
#scraping
import requests
from bs4 import BeautifulSoup
import json
from scraper_covid import scrape_kini_labs

#time
import schedule
import time

"""to activate back"""
# scrape_kini_labs()

chartdata_df = pd.read_csv('covid_data_updated_descending.csv')
chartdata_df2 = pd.read_csv('covid_data_updated_ascending.csv')
vax_malaysia_citf_df = pd.read_csv('https://raw.githubusercontent.com/CITF-Malaysia/citf-public/main/vaccination/vax_malaysia.csv')
vax_state_citf_df = pd.read_csv('https://raw.githubusercontent.com/CITF-Malaysia/citf-public/main/vaccination/vax_state.csv')
population_df = pd.read_csv('https://raw.githubusercontent.com/CITF-Malaysia/citf-public/main/static/population.csv')
vax_reg_malaysia = pd.read_csv('https://raw.githubusercontent.com/CITF-Malaysia/citf-public/main/registration/vaxreg_malaysia.csv')
vax_reg_state = pd.read_csv('https://raw.githubusercontent.com/CITF-Malaysia/citf-public/main/registration/vaxreg_state.csv')
vaccine_df = pd.read_csv('vaccine_data_updated_ascending.csv')

# start_button = st.empty()
# if start_button.button('Refresh', key='start'):
#     start_button.empty()

st.title('Covid-19 Malaysia')
update_date = open('update_datetime.txt', 'r')
st.text(f'{update_date.read()}')
st.markdown("""
This app performs simple visualization of covid-19 status in Malaysia
* **Data source:** 1. [KKM's daily report](https://t.me/cprckkm) 2. [Covid-19 Immunisation Task Force (CITF)](https://github.com/CITF-Malaysia/citf-public)
""")
st.text("")
st.text("")

states = ['Sabah', 'Selangor', 'Kuala Lumpur', 'Negeri Sembilan', 'Kedah', 'Pulau Pinang', 'labuan', 'Sarawak', 'Johor', 'Perak', 'Pahang', 'Melaka', 'Terengganu', 'Kelantan', 'Putrajaya', 'Perlis']
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
patient_status = ['confirmed cases', 'active cases', 'recovered cases', 'death cases']
st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(2020,2022))))
selected_month = st.sidebar.selectbox('Month', list(months))
visualization = st.sidebar.selectbox('Select a chart type', ('Bar Chart', 'Pie Chart', 'Line Chart'))
state_select = st.sidebar.selectbox('State', states)
status_select = st.sidebar.radio('Covid-19 patient status', patient_status)

# selected_state =


new_cases, new_death, total_Icu, Discharge = st.beta_columns(4)
with new_cases:
    new_case_card(chartdata_df)

    st.text("")
    st.text("")
    st.text("")

with new_death:
    new_death_card(chartdata_df)

with total_Icu:
    icu_card(chartdata_df)

with Discharge:
    discharge_card(chartdata_df=chartdata_df)



#dataframe
column_list = chartdata_df.drop(['date', 'Positivity rate'], axis=1).columns.tolist()
st.dataframe(chartdata_df.style.format('{:,}', subset=column_list))

#cummulative confirmed cases
st.plotly_chart(cumul_confirm_cases(chartdata_df2))

#daily confirmed cases
st.plotly_chart(daily_confirm_cases(chartdata_df2))

# positive rate
st.plotly_chart(daily_positive_rate(chartdata_df2))


st.title('National Vaccination Progress')
# st.header('National Vaccination Progress')

st.text(vaccine_updated_datetime(vax_malaysia_citf_df))

daily_doses, vaccination_progress, vaccinated_percent = st.beta_columns(3)

with daily_doses:
    daily_doses_card(vax_malaysia_citf_df)
    st.text("")
    st.text("")
    st.text("")

with vaccination_progress:
    vaccination_progress_card(vax_malaysia_citf_df)

with vaccinated_percent:
    vaccinated_percent_card(vax_malaysia_citf_df=vax_malaysia_citf_df, population_df=population_df)

#resitration, target population to be vaccinated
st.plotly_chart(vaccination_target(vax_malaysia_citf_df, vax_reg_malaysia, population_df))

#vaccination progress
st.plotly_chart(vaccination_progress_line(vax_malaysia_citf_df, population_df))

# daily vaccine
st.plotly_chart(vaccine_daily(vax_malaysia_citf_df))













