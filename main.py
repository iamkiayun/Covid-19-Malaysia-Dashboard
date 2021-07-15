
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



# patient_status = ['confirmed cases', 'active cases', 'recovered cases', 'death cases']
st.sidebar.header('Select')
# selected_year = st.sidebar.selectbox('Year', list(reversed(range(2020,2022))))
selected_month = st.sidebar.selectbox('Month', months())
visualization = st.sidebar.selectbox('Select', ('Covid-19 Status','Vaccination Status'))
state_select = st.sidebar.selectbox('State', states())
# status_select = st.sidebar.radio('Covid-19 patient status', patient_status)

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


#daily state vaccination status



#state vaccination progress
# vax_state_citf_df
# vax_reg_state
# population_df

vax_progress_by_state_df = vax_state_citf_df.set_index('state').reset_index()
vax_2 = vax_progress_by_state_df.groupby(['state']).last().reset_index()
vax_2['date'] = pd.to_datetime(vax_2['date'], format='%Y-%m-%d')
vax_2['date'] = vax_2['date'].dt.strftime("%d %b %Y")


#vaccination administration dataframe

column_list_to_amend = vax_2.drop(['date', 'state'], axis=1).columns.tolist()
st.dataframe(vax_2.style.format('{:,}', subset=column_list_to_amend))
vax_2_with_pop = pd.merge(vax_2, population_df, on='state', how='left')
new_vax_reg_state =vax_reg_state.groupby(['state']).last().reset_index()
vax_2_with_pop_reg = pd.merge(vax_2_with_pop, new_vax_reg_state, on='state', how='left')

#vaccination by state
graph = px.bar(vax_2, x=['dose1_daily', 'dose2_daily'], y='state',
               title="Daily vaccine administered by state",
               color_discrete_sequence=['#009dc4','#a88905']
               )

graph.update_xaxes(  # the y-axis is in dollars
    ticksuffix='', showgrid=False, showticklabels=True  # tickprefix=""
)

graph.update_layout(yaxis_title='', xaxis_title='', showlegend=True, legend_title_text=''
                                 )


def custom_legend_name(fig, new_names):
    for i, new_name in enumerate(new_names):
        fig.data[i].name = new_name


custom_legend_name(fig=graph, new_names=['1st dose', '2nd dose'])


st.plotly_chart(graph)


#vaccination progress by state based on doses, registration

graph_x = px.bar(vax_2_with_pop_reg,
                 x=['total', 'dose1_cumul', 'dose2_cumul'] ,
                 y='state'
                )

st.plotly_chart(graph_x)

#vaccination progress by state based on percentage
dose1_percent = vax_2_with_pop_reg['dose1_cumul']/vax_2_with_pop_reg['pop']*100
dose2_percent = vax_2_with_pop_reg['dose2_cumul']/vax_2_with_pop_reg['pop']*100
reg_percent = vax_2_with_pop_reg['total']/vax_2_with_pop_reg['pop']*100


fig = go.Figure()
anchos = [0.3]* 16

fig.add_trace((go.Bar(x=reg_percent,
                      y=vax_2_with_pop_reg['state'],
                      width= anchos, name='registration',
                      text= reg_percent,
                      orientation='h',
                      offset=0,
                      marker_color='#5a7d9f' #004a6a #94a6bb #d0cac0
                      )))

fig.add_trace((go.Bar(x=dose1_percent,
                      y=vax_2_with_pop_reg['state'],
                      width= anchos, name='1st dose',
                      text= dose1_percent,
                      orientation='h',
                      offset=-0.15,
                      marker_color='#009dc4'
                      )))
fig.add_trace((go.Bar(x=dose2_percent,
                      y=vax_2_with_pop_reg['state'],
                      width= anchos, name='2nd dose',
                      text= dose2_percent,
                      orientation='h',
                      offset=-0.3,
                      marker_color='#a88905'
                      )))


fig.update_layout(title = "Vaccination Progress by States",
                  barmode = 'overlay',title_font_size = 40,
                  width = 800, height = 600
                  )
fig.update_traces( marker_line_color='rgb(8,48,107)',#marker_color='rgb(158,202,225)',
                  marker_line_width=0, opacity=0.9)

fig.update_xaxes(showgrid=False, ticksuffix='%')
fig.add_vline(x=80, line_width=3, line_dash="dash", line_color="red",  # population_df['pop'].iloc[0]
                 annotation_text="target:  <br>(80% population<br> to be vaccinated)",
                 annotation_position='left')

st.plotly_chart(fig)

