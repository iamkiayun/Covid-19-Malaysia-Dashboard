
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
# date = update_date.read()
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
    st.markdown(f"<h4 style='line-height: 6px; text-align: left; vertical-align: center'>New Cases</h4>",unsafe_allow_html=True)
    # st.markdown('**New Cases**')
    new_case_no = chartdata_df['newCase'].iloc[0]
    total_test_conducted = chartdata_df['newTest'].iloc[0]
    positive_rate = chartdata_df['Positivity rate'].iloc[0]
    totalCase = chartdata_df['totalCase'].iloc[0]
    newDeath = chartdata_df['newDeath'].iloc[0]
    totalDeath = chartdata_df['totalDeath'].iloc[0]
    # st.markdown("<h4 style='line-height: 10px; text-align: left; vertical-align: center'>num.toLocalString</h4>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='line-height: 30px; text-align: left; vertical-align: center'>{new_case_no:,}</h4>", unsafe_allow_html=True)
    st.markdown(f"<h5 style='line-height: 10px; text-align: left; vertical-align: center'>*total cases: {totalCase:,}</h5>",unsafe_allow_html=True)
    st.markdown(f"<h5 style='text-align: left;'>*new test: {int(total_test_conducted):,}</h5>", unsafe_allow_html=True)
    st.markdown(f"<h5 style='text-align: left;'>*+ve rate: {positive_rate:,}%</h5>", unsafe_allow_html=True)
    st.text("")
    st.text("")
    st.text("")

with new_death:
    st.markdown(f"<h4 style='line-height: 6px; text-align: left; vertical-align: center'>New Deaths</h4>",unsafe_allow_html=True)
    st.markdown(f"<h4 style='line-height: 30px; text-align: left; vertical-align: center'>{newDeath:,}</h4>",unsafe_allow_html=True)
    st.markdown(f"<h5 style='line-height: 10px; text-align: left; vertical-align: center'>*total deaths: {totalDeath:,}</h5>",unsafe_allow_html=True)


with total_Icu:
    chartdata_df['Positivity rate'] = chartdata_df['Positivity rate'].map('{:,.2f}'.format)
    column_list = chartdata_df.drop(['date', 'Positivity rate'], axis=1).columns.tolist()
    chartdata_df[column_list] = chartdata_df[column_list].fillna(0).astype(dtype=int)
    chartdata_df.style.format('{:,}', subset=column_list)
    totalIcu = chartdata_df['totalIcu'].iloc[0]
    totalIntubated = chartdata_df['intubated'].iloc[0]
    newIcu = chartdata_df['newIcu'].iloc[0]
    newDischarged = chartdata_df['newDischarged'].iloc[0]
    totalDischarged = chartdata_df['totalDischarged'].iloc[0]
    cure_rate = round(chartdata_df['totalDischarged'].iloc[0]/ chartdata_df['totalCase'].iloc[0]*100,2)
    st.markdown(f"<h4 style='line-height: 6px; text-align: left; vertical-align: center'>New ICU</h4>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='line-height: 30px; text-align: left; vertical-align: center'>{newIcu:,}</h4>", unsafe_allow_html=True)
    st.markdown(f"<h5 style='line-height: 0px; text-align: left; vertical-align: center'>*current Icu: {totalIcu:,}</h5>",unsafe_allow_html=True)
    st.markdown(f"<h5 style='line-height: 0px; text-align: left; vertical-align: center'>*intubated: {totalIntubated:,}</h5>", unsafe_allow_html=True)

with Discharge:
    st.markdown(f"<h4 style='line-height: 6px; text-align: left; vertical-align: center'>New Discharged</h4>",unsafe_allow_html=True)
    st.markdown(f"<h4 style='line-height: 30px; text-align: left; vertical-align: center'>{newDischarged:,}</h4>",unsafe_allow_html=True)
    st.markdown(f"<h5 style='line-height: 0px; font-size:12.5px; text-align: left; vertical-align: center'>*total discharged: {totalDischarged:,}</h5>",unsafe_allow_html=True)
    st.markdown(f"<h5 style='line-height: 0px; text-align: left; vertical-align: center'>*cure rate: {cure_rate:,}%</h5>",unsafe_allow_html=True)

# st.write(chartdata_df)
# chartdata_df['Positivity rate'] = chartdata_df['Positivity rate'] .map('{:,.2f}'.format)
# column_list = chartdata_df.drop(['date','Positivity rate'], axis=1).columns.tolist()
# chartdata_df[column_list] = chartdata_df[column_list].fillna(0).astype(dtype=int)
# s = chartdata_df.style.format('{:,}', subset=column_list)
st.dataframe(chartdata_df.style.format('{:,}', subset=column_list))


#cummulative confirmed cases
st.plotly_chart(cumul_confirm_cases(chartdata_df2))

#daily confirmed cases
st.plotly_chart(daily_confirm_cases(chartdata_df2))

# positive rate
st.plotly_chart(daily_positive_rate(chartdata_df2))

st.header('National Vaccination Progress')

daily_doses, vaccination_progress, vaccinated_percent = st.beta_columns(3)
# vax_malaysia_citf_df['total_daily']

with daily_doses:
    st.markdown(f"<h4 style='line-height: 6px; text-align: left; vertical-align: center'>New Doses </h4>",unsafe_allow_html=True)
    # st.markdown('**New Cases**')
    daily_total_jab = round(vax_malaysia_citf_df['total_daily'].iloc[-1]/1000,2)
    daily_1st_jab = round(vax_malaysia_citf_df['dose1_daily'].iloc[-1]/1000,2)
    daily_2nd_jab = round(vax_malaysia_citf_df['dose2_daily'].iloc[-1]/1000,2)

    # st.markdown("<h4 style='line-height: 10px; text-align: left; vertical-align: center'>num.toLocalString</h4>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='line-height: 30px; text-align: left; vertical-align: center'>{daily_total_jab}K</h4>", unsafe_allow_html=True)
    st.markdown(f"<h5 style='line-height: 10px; text-align: left; vertical-align: center'>*1st dose: {daily_1st_jab}K</h5>",unsafe_allow_html=True)
    st.markdown(f"<h5 style='text-align: left;'>*2nd dose: {int(daily_2nd_jab)}K</h5>", unsafe_allow_html=True)
    # st.markdown(f"<h5 style='text-align: left;'>*+ve rate: {positive_rate}%</h5>", unsafe_allow_html=True)
    st.text("")
    st.text("")
    st.text("")

with vaccination_progress:
    vax_total_cumul = round(vax_malaysia_citf_df['total_cumul'].iloc[-1]/1000000,2)
    vax_1st_cumul = round(vax_malaysia_citf_df['dose1_cumul'].iloc[-1]/1000000,2)
    vax_2nd_cumul = round(vax_malaysia_citf_df['dose2_cumul'].iloc[-1]/1000000,2)
    st.markdown(f"<h4 style='line-height: 6px; text-align: left; vertical-align: center'>Total Administered</h4>",unsafe_allow_html=True)
    st.markdown(f"<h4 style='line-height: 30px; text-align: left; vertical-align: center'>{vax_total_cumul}M</h4>",unsafe_allow_html=True)
    st.markdown(f"<h5 style='line-height: 10px; text-align: left; vertical-align: center'>*1st dose: {vax_1st_cumul}M</h5>",unsafe_allow_html=True)
    st.markdown(f"<h5 style='line-height: 10px; text-align: left; vertical-align: center'>*2nd dose: {vax_2nd_cumul}M</h5>",unsafe_allow_html=True)


with vaccinated_percent:
    population_1st = round(vax_malaysia_citf_df['dose1_cumul'].iloc[-1]/population_df['pop'].iloc[0]*100,2)
    population_2nd = round(vax_malaysia_citf_df['dose2_cumul'].iloc[-1] / population_df['pop'].iloc[0]*100, 2)
    st.markdown(f"<h4 style='line-height: 6px; text-align: left; vertical-align: center'>Vaccination Progress</h4>", unsafe_allow_html=True)
    st.text('')
    st.text('')
    st.text('')
    # st.markdown(f"<h4 style='line-height: 30px; text-align: left; vertical-align: center'>x</h4>", unsafe_allow_html=True)
    st.markdown(f"<h5 style='line-height: 0px; text-align: left; vertical-align: center'>*fully inoculated: {population_2nd}%</h5>",unsafe_allow_html=True)
    st.markdown(f"<h5 style='line-height: 0px; text-align: left; vertical-align: center'>*received 1 dose: {population_1st}%</h5>", unsafe_allow_html=True)


#resitration, target population to be vaccinated
st.plotly_chart(vaccination_target(vax_malaysia_citf_df, vax_reg_malaysia, population_df))

#vaccination progress
st.plotly_chart(vaccination_progress_line(vax_malaysia_citf_df, population_df))

# daily vaccine
st.plotly_chart(vaccine_daily(vax_malaysia_citf_df))













