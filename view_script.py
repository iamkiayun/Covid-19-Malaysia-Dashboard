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
from datetime import datetime
#scraping
import requests
from bs4 import BeautifulSoup
import json
from scraper_covid import scrape_kini_labs

#time
import schedule
import time


""" 
Cummulative Confirmed Cases
"""
def cumul_confirm_cases(chartdata_df2):
    graph = px.bar(chartdata_df2, x='date', y='totalCase',
                   labels={
                       'date': '',
                       'totalCase':''
                   },
                   title='Cumulative confirmed cases')
    cumul_case = chartdata_df2['totalCase'].iloc[-1]
    # convert from string time to normal time UTC
    last_date = datetime.strptime(chartdata_df2['date'].iloc[-1], "%d %b %y")
    # convet from UTC time to string time
    date_date = last_date.strftime("%d %b %Y")
    # last_date = pd.to_datetime(chartdata_df2['date'].iloc[-1])
    # positive_rate_daily.update_yaxes(ticksuffix= '%')
    # positive_rate_daily.update_layout(yaxis_title="")
    graph.add_hline(y=cumul_case, line_width=3, line_dash="dash", line_color="red",
                          # population_df['pop'].iloc[0]
                          # annotation_text=f"{total_dose_daily:,} doses <br> ( 1st dose: {dose_1_daily:,} doses <br>2nd dose: {dose_2_daily:,}doses) <br><br>", #(80% population<br> to be vaccinated)
                          # annotation_position='bottom'
                          )
    graph.update_yaxes(showgrid=False)

    graph.add_annotation(dict(xref='paper', yref='y', x=0.4, y=cumul_case,
                                    xanchor='center', yanchor='top',
                                    text=f"{cumul_case:,} cases <br>as of {date_date}",
                                    # font=dict(#family='Arial',
                                    #           size=12,
                                    #           color='rgb(150,150,150)'),
                                    showarrow=False,
                                    align='left'
                                    ))
    return graph


"""
#daily confirmed cases
"""
def daily_confirm_cases(chartdata_df2):
    graph_daily = px.bar(chartdata_df2, x='date', y='newCase',
               labels={
                   'date': '',
                   'newCase':''
               },
               title='Daily new cases')
    last_new_case = chartdata_df2['newCase'].iloc[-1]
    #convert from string time to normal time UTC
    last_date = datetime.strptime(chartdata_df2['date'].iloc[-1], "%d %b %y")
    #convet from UTC time to string time
    date_date = last_date.strftime("%d %b %Y")
    # last_date = pd.to_datetime(chartdata_df2['date'].iloc[-1])
    # positive_rate_daily.update_yaxes(ticksuffix= '%')
    # positive_rate_daily.update_layout(yaxis_title="")
    graph_daily.add_hline(y=last_new_case, line_width=3, line_dash="dash", line_color="red",#population_df['pop'].iloc[0]
                     # annotation_text=f"{total_dose_daily:,} doses <br> ( 1st dose: {dose_1_daily:,} doses <br>2nd dose: {dose_2_daily:,}doses) <br><br>", #(80% population<br> to be vaccinated)
                     # annotation_position='bottom'
                            )
    graph_daily.update_yaxes(showgrid=False)

    graph_daily.add_annotation(dict(xref='paper', yref='y', x=0.4, y=last_new_case,
                                  xanchor='center', yanchor='top',
                                  text=f"{last_new_case:,} new cases <br>on {date_date}",
                                  # font=dict(#family='Arial',
                                  #           size=12,
                                  #           color='rgb(150,150,150)'),
                                  showarrow=False,
                                  align='left'
                                    ))
    return graph_daily

"""
# positive rate
"""
def daily_positive_rate(chartdata_df2):
    positive_rate_daily = px.bar(chartdata_df2, x='date', y='Positivity rate',
                       labels= {
                           "date": "",
                           "total_daily": "Positivity Rate (%)"
                       },
                       title='Daily positivity rate')
    last_positivity_rate = chartdata_df2['Positivity rate'].iloc[-1]
    #convert from string time to normal time UTC
    last_date = datetime.strptime(chartdata_df2['date'].iloc[-1], "%d %b %y")
    #convet from UTC time to string time
    date_date = last_date.strftime("%d %b %Y")
    # last_date = pd.to_datetime(chartdata_df2['date'].iloc[-1])
    positive_rate_daily.update_yaxes(ticksuffix= '%')
    positive_rate_daily.update_layout(yaxis_title="")
    positive_rate_daily.add_hline(y=last_positivity_rate, line_width=3, line_dash="dash", line_color="red",#population_df['pop'].iloc[0]
                     # annotation_text=f"{total_dose_daily:,} doses <br> ( 1st dose: {dose_1_daily:,} doses <br>2nd dose: {dose_2_daily:,}doses) <br><br>", #(80% population<br> to be vaccinated)
                     # annotation_position='bottom'
                            )
    positive_rate_daily.update_yaxes(showgrid=False)

    positive_rate_daily.add_annotation(dict(xref='paper', yref='y', x=0.4, y=last_positivity_rate,
                                  xanchor='center', yanchor='top',
                                  text=f"{last_positivity_rate}% on<br>{date_date}",
                                  # font=dict(#family='Arial',
                                  #           size=12,
                                  #           color='rgb(150,150,150)'),
                                  showarrow=False,
                                  align='left'
                                    ))
    return positive_rate_daily

"""
# vaccine daily
"""
def vaccine_daily(vax_malaysia_citf_df):
    vaccine_daily = px.bar(vax_malaysia_citf_df, x='date', y=['dose1_daily','dose2_daily'],
                           template='simple_white',
                           labels= {
                               "date": "",
                               "dose1_daily": "1st dose",
                               "dose2_daily": "2nd dose"
                           },
                           title='Daily vaccine doses administered',
                           #color_discrete_sequence=px.colors.sequential.Plasma_r
                           color_discrete_map={'dose1_daily':'#009dc4',    #rgba(255,0,0,0.4)      #FFA15A    #46039F      #3EB489
                                                'dose2_daily':'#a88905'}   #E1AD01

                           )
    vaccine_daily.update_yaxes( # the y-axis is in dollars
        tickprefix="", showgrid=True, showticklabels=True
    )
    vaccine_daily.update_xaxes( # the y-axis is in dollars
        tickprefix="", showgrid=False
    )
    vaccine_daily.update_traces( #marker_line_color='#009dc4',       ##009dc4 #a88905
                      marker_line_width=0, opacity=1)
    # vaccine_daily.update_traces(marker_color=['green', 'blue'])
    vaccine_daily.update_layout(yaxis_title=None, legend_title_text='')

    #add horizontal line
    dose_1_daily = vax_malaysia_citf_df['dose1_daily'].iloc[-1]
    dose_2_daily = vax_malaysia_citf_df['dose2_daily'].iloc[-1]
    total_dose_daily = dose_1_daily + dose_2_daily
    update_date = pd.to_datetime(vax_malaysia_citf_df['date'].iloc[-1]).strftime("%d %b %Y")

    vaccine_daily.add_hline(y=total_dose_daily, line_width=3, line_dash="dash", line_color="red",#population_df['pop'].iloc[0]
                     # annotation_text=f"{total_dose_daily:,} doses <br> ( 1st dose: {dose_1_daily:,} doses <br>2nd dose: {dose_2_daily:,}doses) <br><br>", #(80% population<br> to be vaccinated)
                     # annotation_position='bottom'
                            )
    vaccine_daily.update_yaxes(showgrid=False)

    vaccine_daily.add_annotation(dict(xref='paper', yref='y', x=0.69, y=total_dose_daily,
                                  xanchor='center', yanchor='top',
                                  text=f"total: {total_dose_daily:,} doses <br>(1st dose: {dose_1_daily:,} doses <br> 2nd dose: {dose_2_daily:,}doses)<br>administered on {update_date}",
                                  # font=dict(#family='Arial',
                                  # #           size=12,
                                  # #           color='rgb(150,150,150)'),
                                  showarrow=False,
                                  align='left'
                                    ))


    def custom_legend_name(fig, new_names):
        for i, new_name in enumerate(new_names):
            fig.data[i].name = new_name

    custom_legend_name(fig=vaccine_daily,new_names=['1st dose', '2nd dose'])



    return vaccine_daily

"""
#resitration, target population to be vaccinated
"""

def vaccination_target(vax_malaysia_citf_df, vax_reg_malaysia,population_df):
    data= {'type':['individual with 2nd_dose','individual with 1st_dose', 'registered individuals'],
           'total':[round(vax_malaysia_citf_df['dose2_cumul'].iloc[-1],2),
                    round(vax_malaysia_citf_df['dose1_cumul'].iloc[-1],2),
                    round(vax_reg_malaysia['total'].iloc[-1],2)
                    ]}
    compare_df = pd.DataFrame(data=data)
    target = px.bar(compare_df, x='total', y='type', orientation='h')

    target.update_layout(yaxis_title='', xaxis_title='', showlegend=False, legend_title_text= '')
    target.update_layout(title='Vaccination target')
    target.update_xaxes(range=[0,30000000], showgrid=False)
    target.update_yaxes(showticklabels=False)
    colors = ['#0c3953']*3    #f67e7d #843b62 #0c3953
    colors[1] = '#009dc4'  #1st dose
    colors[0] = '#a88905'  #2nd dose
    target.update_traces(marker_color=colors, #marker_line_color='#009dc4',       ##009dc4 #a88905
                      marker_line_width=0, opacity=1, width=0.4)
    # Source
    target.add_annotation(dict(xref='paper', yref='paper', x=0.5, y=-0.1,
                                  xanchor='center', yanchor='top',
                                  text='Source: Covid-19 Immunisation Task Force (CITF)',
                                  font=dict(#family='Arial',
                                  #           size=12,
                                            color='rgb(150,150,150)'),
                                  showarrow=False))
    target.add_vline(x=26130000, line_width=3, line_dash="dash", line_color="red", #population_df['pop'].iloc[0]
                     annotation_text="target: 26.13 million <br>(80% population<br> to be vaccinated)",
                     annotation_position='left')

    target.add_annotation(dict(xref='paper', yref='paper', x=0.07, y=0.61,
                                  xanchor='left', yanchor='auto',
                                  text=f"population with at least 1 dose: {round(vax_malaysia_citf_df['dose1_cumul'].iloc[-1]/1000000,2)} mil " #population with at least 1 dose
                                       f"({round(vax_malaysia_citf_df['dose1_cumul'].iloc[-1]/population_df['pop'].iloc[0]*100,2)}%)",
                                  showarrow=False,
                                  #font=dict(family='Arial',
                                            #size=12,
                                            # color='rgb(150,150,150)'
                               ))
    target.add_annotation(dict(xref='paper', yref='paper', x=0.07, y=0.24,
                                  xanchor='left', yanchor='auto',
                                  text= f"fully inoculated: {round(vax_malaysia_citf_df['dose2_cumul'].iloc[-1]/1000000,2)} mil "
                                        f"({round(vax_malaysia_citf_df['dose2_cumul'].iloc[-1]/population_df['pop'].iloc[0]*100,2)}%)",
                                  showarrow=False
                                  #font=dict(family='Arial',
                                            #size=12,
                                            # color='rgb(150,150,150)'
                                ))

    target.add_annotation(dict(xref='paper', yref='paper', x=0.07, y=0.97,
                                  xanchor='left', yanchor='auto',
                                  text=f"registration: {round(vax_reg_malaysia['total'].iloc[-1]/1000000,2)} mil "
                                       f"({round(vax_reg_malaysia['total'].iloc[-1]/population_df['pop'].iloc[0]*100,2)}%)",
                                  showarrow=False
                                  #font=dict(family='Arial',
                                            #size=12,
                                            # color='rgb(150,150,150)'
                               ))

    target.add_annotation(dict(xref='paper', yref='paper', x=-0.081, y=1.08,
                               xanchor='left', yanchor='auto',
                               text=f"* total population is estimated at {round(population_df['pop'].iloc[0]/1000000,2)} mil",
                               font=dict(color='rgb(150,150,150)'),
                               showarrow=False
                               ))

    return target

"""
#vaccination progress
"""
def vaccination_progress_line(vax_malaysia_citf_df, population_df):
    #total population is estimated at 32.66 million
    total_pop = population_df.iloc[0]['pop']
    # vaccine_df['total_cum/total_pop'] = vaccine_df['dose2_cumul']/ total_pop*100                      #vaccine_df['total_cum/total_pop']     #vaccine_df['dose2_cumul']
    # vaccine_df['first/total_pop'] = vaccine_df['dose1_cumul']/ total_pop**100                         #vaccine_df['first/total_pop']         #vaccine_df['dose1_cumul']
    second_cumul_percent = vax_malaysia_citf_df['dose2_cumul']/total_pop*100
    first_cumul_percent = vax_malaysia_citf_df['dose1_cumul']/total_pop*100
    vaccine_population = px.line(vax_malaysia_citf_df, x='date', y=[first_cumul_percent,second_cumul_percent],
                           title='Population vaccination progress',
                           template='simple_white',
                           color_discrete_sequence=['#009dc4','#a88905']
                           # color_discrete_map={'first_cumul_percent': '#009dc4',
                           #                      'second_cumul_percent': '#a88905'}
                             )

    def custom_legend_name(fig, new_names):
        for i, new_name in enumerate(new_names):
            fig.data[i].name = new_name

    custom_legend_name(fig=vaccine_population, new_names=['received 1st dose only', 'fully inoculated with 2nd dose'])

    vaccine_population.update_yaxes( # the y-axis is in dollars
         ticksuffix='%',showgrid=True, showticklabels=True            #tickprefix=""
    )

    vaccine_population.update_layout(yaxis_title='', xaxis_title='', showlegend=True, legend_title_text= ''
                                     )

    vaccine_population.add_scatter(x=[vax_malaysia_citf_df.iloc[-1]['date']],
                                   y=[second_cumul_percent.iloc[-1]],
                                   text=[f"{round(second_cumul_percent.iloc[-1],2)}%"],
                                   mode='markers+text',
                                   marker=dict(color='#a88905', size=1),
                                   # textfont=dict(color='', size=20),
                                   textposition='middle left',
                                   showlegend=False)

    vaccine_population.add_scatter(x=[vax_malaysia_citf_df.iloc[-1]['date']],
                                   y=[first_cumul_percent.iloc[-1]],
                                   text=[f"{round(first_cumul_percent.iloc[-1],2)}%"],
                                   mode='markers+text',
                                   marker=dict(color='#009dc4', size=1),
                                   # textfont=dict(color='', size=20),
                                   textposition='middle left',
                                   showlegend=False)
    return vaccine_population


def vaccine_updated_datetime(vax_malaysia_citf_df):
    vax_date_update_ori = pd.to_datetime(vax_malaysia_citf_df['date'].iloc[-1], format='%Y-%m-%d')
    vax_date_update_converted = vax_date_update_ori.strftime("%b %d, %Y")
    update_time = datetime.now().strftime("%I:%M %p")
    statement = f"Updated: {vax_date_update_converted} {update_time}"
    return statement


def new_case_card(chartdata_df):
    st.markdown(f"<h4 style='line-height: 6px; text-align: left; vertical-align: center'>New Cases</h4>",unsafe_allow_html=True)
    # st.markdown('**New Cases**')
    new_case_no = chartdata_df['newCase'].iloc[0]
    total_test_conducted = chartdata_df['newTest'].iloc[0]
    positive_rate = chartdata_df['Positivity rate'].iloc[0]
    totalCase = chartdata_df['totalCase'].iloc[0]

    # st.markdown("<h4 style='line-height: 10px; text-align: left; vertical-align: center'>num.toLocalString</h4>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='line-height: 30px; text-align: left; vertical-align: center'>{new_case_no:,}</h4>", unsafe_allow_html=True)
    st.markdown(f"<h5 style='line-height: 10px; text-align: left; vertical-align: center'>*total cases: {totalCase:,}</h5>",unsafe_allow_html=True)
    st.markdown(f"<h5 style='text-align: left;'>*new test: {int(total_test_conducted):,}</h5>", unsafe_allow_html=True)
    st.markdown(f"<h5 style='text-align: left;'>*+ve rate: {positive_rate:,}%</h5>", unsafe_allow_html=True)


def new_death_card(chartdata_df):
    newDeath = chartdata_df['newDeath'].iloc[0]
    totalDeath = chartdata_df['totalDeath'].iloc[0]
    st.markdown(f"<h4 style='line-height: 6px; text-align: left; vertical-align: center'>New Deaths</h4>",unsafe_allow_html=True)
    st.markdown(f"<h4 style='line-height: 30px; text-align: left; vertical-align: center'>{newDeath:,}</h4>",unsafe_allow_html=True)
    st.markdown(f"<h5 style='line-height: 10px; text-align: left; vertical-align: center'>*total deaths: {totalDeath:,}</h5>",unsafe_allow_html=True)


def icu_card(chartdata_df):
    chartdata_df['Positivity rate'] = chartdata_df['Positivity rate'].map('{:,.2f}'.format)
    column_list = chartdata_df.drop(['date', 'Positivity rate'], axis=1).columns.tolist()
    chartdata_df[column_list] = chartdata_df[column_list].fillna(0).astype(dtype=int)
    chartdata_df.style.format('{:,}', subset=column_list)
    newIcu = chartdata_df['newIcu'].iloc[0]
    totalIcu = chartdata_df['totalIcu'].iloc[0]
    totalIntubated = chartdata_df['intubated'].iloc[0]

    st.markdown(f"<h4 style='line-height: 6px; text-align: left; vertical-align: center'>New ICU</h4>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='line-height: 30px; text-align: left; vertical-align: center'>{newIcu:,}</h4>", unsafe_allow_html=True)
    st.markdown(f"<h5 style='line-height: 0px; text-align: left; vertical-align: center'>*current Icu: {totalIcu:,}</h5>",unsafe_allow_html=True)
    st.markdown(f"<h5 style='line-height: 0px; text-align: left; vertical-align: center'>*intubated: {totalIntubated:,}</h5>", unsafe_allow_html=True)


def discharge_card(chartdata_df):
    newDischarged = chartdata_df['newDischarged'].iloc[0]
    totalDischarged = chartdata_df['totalDischarged'].iloc[0]
    cure_rate = round(chartdata_df['totalDischarged'].iloc[0]/ chartdata_df['totalCase'].iloc[0]*100,2)
    st.markdown(f"<h4 style='line-height: 6px; text-align: left; vertical-align: center'>New Discharged</h4>",unsafe_allow_html=True)
    st.markdown(f"<h4 style='line-height: 30px; text-align: left; vertical-align: center'>{newDischarged:,}</h4>",unsafe_allow_html=True)
    st.markdown(f"<h5 style='line-height: 0px; font-size:12.5px; text-align: left; vertical-align: center'>*total discharged: {totalDischarged:,}</h5>",unsafe_allow_html=True)
    st.markdown(f"<h5 style='line-height: 0px; text-align: left; vertical-align: center'>*cure rate: {cure_rate:,}%</h5>",unsafe_allow_html=True)


def daily_doses_card(vax_malaysia_citf_df):
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


def vaccination_progress_card(vax_malaysia_citf_df):
    vax_total_cumul = round(vax_malaysia_citf_df['total_cumul'].iloc[-1]/1000000,2)
    vax_1st_cumul = round(vax_malaysia_citf_df['dose1_cumul'].iloc[-1]/1000000,2)
    vax_2nd_cumul = round(vax_malaysia_citf_df['dose2_cumul'].iloc[-1]/1000000,2)
    st.markdown(f"<h4 style='line-height: 6px; text-align: left; vertical-align: center'>Total Administered</h4>",unsafe_allow_html=True)
    st.markdown(f"<h4 style='line-height: 30px; text-align: left; vertical-align: center'>{vax_total_cumul}M</h4>",unsafe_allow_html=True)
    st.markdown(f"<h5 style='line-height: 10px; text-align: left; vertical-align: center'>*1st dose: {vax_1st_cumul}M</h5>",unsafe_allow_html=True)
    st.markdown(f"<h5 style='line-height: 10px; text-align: left; vertical-align: center'>*2nd dose: {vax_2nd_cumul}M</h5>",unsafe_allow_html=True)


def vaccinated_percent_card(vax_malaysia_citf_df, population_df):
    population_1st = round(vax_malaysia_citf_df['dose1_cumul'].iloc[-1]/population_df['pop'].iloc[0]*100,2)
    population_2nd = round(vax_malaysia_citf_df['dose2_cumul'].iloc[-1] / population_df['pop'].iloc[0]*100, 2)
    st.markdown(f"<h4 style='line-height: 6px; text-align: left; vertical-align: center'>Vaccination Progress</h4>", unsafe_allow_html=True)
    st.text('')
    st.text('')
    st.text('')
    # st.markdown(f"<h4 style='line-height: 30px; text-align: left; vertical-align: center'>x</h4>", unsafe_allow_html=True)
    st.markdown(f"<h5 style='line-height: 0px; text-align: left; vertical-align: center'>*fully inoculated: {population_2nd}%</h5>",unsafe_allow_html=True)
    st.markdown(f"<h5 style='line-height: 0px; text-align: left; vertical-align: center'>*received 1 dose: {population_1st}%</h5>", unsafe_allow_html=True)

def states():
    states = ['Sabah', 'Selangor', 'Kuala Lumpur', 'Negeri Sembilan', 'Kedah', 'Pulau Pinang', 'labuan', 'Sarawak',
              'Johor', 'Perak', 'Pahang', 'Melaka', 'Terengganu', 'Kelantan', 'Putrajaya', 'Perlis']

    return states


def months():
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    return months

if __name__ == '__main__':
    cumul_confirm_cases(chartdata_df2)
    daily_confirm_cases(chartdata_df2)
    daily_positive_rate(chartdata_df2)
    vaccine_daily(vax_malaysia_citf_df)
    vaccination_target(vax_malaysia_citf_df, vax_reg_malaysia, population_df)
    vaccination_progress_line(vax_malaysia_citf_df, population_df)
    vaccine_updated_datetime(vax_malaysia_citf_df)
    new_case_card(chartdata_df)
    new_death_card(chartdata_df)
    icu_card(chartdata_df)
    discharge_card(chartdata_df)
    daily_doses_card(vax_malaysia_citf_df)
    vaccination_progress_card(vax_malaysia_citf_df)
    vaccinated_percent_card(vax_malaysia_citf_df)
    states()
    months()