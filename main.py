
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

#time
import schedule
import time

# @st.cache(allow_output_mutation=True)
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

    return 'update_datetime.txt', 'vaccine_data_updated_ascending.csv', 'district_df.csv', 'cluster_df.csv', 'covid_data_updated_descending.csv', 'covid_data_updated_ascending.csv'

# def job():
#     scrape_kini_labs()
# try:
#     scrape_kini_labs()
# except Exception:
#     pass


chartdata_df = pd.read_csv('covid_data_updated_descending.csv')
chartdata_df2 = pd.read_csv('covid_data_updated_ascending.csv')
vax_malaysia_citf_df = pd.read_csv('https://raw.githubusercontent.com/CITF-Malaysia/citf-public/main/vaccination/vax_malaysia.csv')
vax_state_citf_df = pd.read_csv('https://raw.githubusercontent.com/CITF-Malaysia/citf-public/main/vaccination/vax_state.csv')
population_df = pd.read_csv('https://raw.githubusercontent.com/CITF-Malaysia/citf-public/main/static/population.csv')
vax_reg_malaysia = pd.read_csv('https://raw.githubusercontent.com/CITF-Malaysia/citf-public/main/registration/vaxreg_malaysia.csv')
vax_reg_state = pd.read_csv('https://raw.githubusercontent.com/CITF-Malaysia/citf-public/main/registration/vaxreg_state.csv')
vaccine_df = pd.read_csv('vaccine_data_updated_ascending.csv')

# def img_to_bytes(img_path):
#     img_bytes = Path(img_path).read_bytes()
#     encoded = base64.b64encode(img_bytes).decode()
#     return encoded
#
# header_html = "<img src='data:image/png;base64,{}' class='img-fluid'>".format(
#     img_to_bytes("header.png")
# )
# st.markdown(
#     header_html, unsafe_allow_html=True,
# )

# image = Image.open('coronavirus-image-iStock-628925532-1200px.jpg')
# st.image(image, width=None)


start_button = st.empty()
if start_button.button('Refresh', key='start'):
    start_button.empty()

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
    st.markdown(f"<h4 style='line-height: 30px; text-align: left; vertical-align: center'>{new_case_no}</h4>", unsafe_allow_html=True)
    st.markdown(f"<h5 style='line-height: 10px; text-align: left; vertical-align: center'>*total cases: {totalCase}</h5>",unsafe_allow_html=True)
    st.markdown(f"<h5 style='text-align: left;'>*new test: {int(total_test_conducted)}</h5>", unsafe_allow_html=True)
    st.markdown(f"<h5 style='text-align: left;'>*+ve rate: {positive_rate}%</h5>", unsafe_allow_html=True)
    st.text("")
    st.text("")
    st.text("")

with new_death:
    st.markdown(f"<h4 style='line-height: 6px; text-align: left; vertical-align: center'>New Deaths</h4>",unsafe_allow_html=True)
    st.markdown(f"<h4 style='line-height: 30px; text-align: left; vertical-align: center'>{newDeath}</h4>",unsafe_allow_html=True)
    st.markdown(f"<h5 style='line-height: 10px; text-align: left; vertical-align: center'>*total deaths: {totalDeath}</h5>",unsafe_allow_html=True)


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
    st.markdown(f"<h4 style='line-height: 30px; text-align: left; vertical-align: center'>{newIcu}</h4>", unsafe_allow_html=True)
    st.markdown(f"<h5 style='line-height: 0px; text-align: left; vertical-align: center'>*current Icu: {totalIcu}</h5>",unsafe_allow_html=True)
    st.markdown(f"<h5 style='line-height: 0px; text-align: left; vertical-align: center'>*intubated: {totalIntubated}</h5>", unsafe_allow_html=True)

with Discharge:
    st.markdown(f"<h4 style='line-height: 6px; text-align: left; vertical-align: center'>New Discharged</h4>",unsafe_allow_html=True)
    st.markdown(f"<h4 style='line-height: 30px; text-align: left; vertical-align: center'>{newDischarged}</h4>",unsafe_allow_html=True)
    st.markdown(f"<h5 style='line-height: 0px; text-align: left; vertical-align: center'>*total discharged: {totalDischarged}</h5>",unsafe_allow_html=True)
    st.markdown(f"<h5 style='line-height: 0px; text-align: left; vertical-align: center'>*cure rate: {cure_rate}%</h5>",unsafe_allow_html=True)

# st.write(chartdata_df)
# chartdata_df['Positivity rate'] = chartdata_df['Positivity rate'] .map('{:,.2f}'.format)
# column_list = chartdata_df.drop(['date','Positivity rate'], axis=1).columns.tolist()
# chartdata_df[column_list] = chartdata_df[column_list].fillna(0).astype(dtype=int)
# s = chartdata_df.style.format('{:,}', subset=column_list)
st.dataframe(chartdata_df.style.format('{:,}', subset=column_list))


#cummulative confirmed cases
graph = px.bar(chartdata_df2, x='date', y='totalCase',
               labels={
                   'date': '',
                   'totalCase':''
               },
               title='Cumulative confirmed cases')
st.plotly_chart(graph)

#daily confirmed cases
graph_daily = px.bar(chartdata_df2, x='date', y='newCase',
               labels={
                   'date': '',
                   'newCase':''
               },
               title='Daily new cases')
st.plotly_chart(graph_daily)

# positive rate
positive_rate_daily = px.bar(chartdata_df2, x='date', y='Positivity rate',
                       labels= {
                           "date": "",
                           "total_daily": "Positivity Rate (%)"
                       },
                       title='Daily Positivity Rate')

st.plotly_chart(positive_rate_daily)



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
data= {'type':['registered_ind','ind_1st_dose', 'ind_2nd_dose'],
       'total':[round(vax_reg_malaysia['total'].iloc[-1],2),
                round(vax_malaysia_citf_df['dose1_cumul'].iloc[-1],2),
                round(vax_malaysia_citf_df['dose2_cumul'].iloc[-1],2)]}
compare_df = pd.DataFrame(data=data)
target = px.bar(compare_df, x='total', y='type', orientation='h')

target.update_layout(yaxis_title='', xaxis_title='', showlegend=False, legend_title_text= '')
target.update_layout(title='Vaccination Target')
target.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.6)

st.plotly_chart(target)





print (compare_df)

#total population is estimated at 32.65 million
total_pop = population_df.iloc[0]['pop']
vaccine_df['total_cum/total_pop'] = vaccine_df['dose2_cumul']/ total_pop*100
vaccine_df['first/total_pop'] = vaccine_df['dose1_cumul']/ total_pop*100
vaccine_population = px.line(vaccine_df, x='date', y=['first/total_pop','total_cum/total_pop'],
                       labels={'first/total_pop': '1st dose',
                                'total_cum/total_pop': '2nd dose'},
                       title='Population vaccination progress',
                       template='simple_white',
                       color_discrete_map={'first/total_pop': '#009dc4',
                                            'total_cum/total_pop': '#a88905'}
                         )

def custom_legend_name(fig, new_names):
    for i, new_name in enumerate(new_names):
        fig.data[i].name = new_name

custom_legend_name(fig=vaccine_population, new_names=['received 1st dose', 'fully inoculated with 2nd dose'])

vaccine_population.update_yaxes( # the y-axis is in dollars
     ticksuffix='%',showgrid=True, showticklabels=True            #tickprefix=""
)

vaccine_population.update_layout(yaxis_title='', xaxis_title='', showlegend=True, legend_title_text= ''
                                 )

vaccine_population.add_scatter(x=[vaccine_df.iloc[-2]['date']],
                               y=[vaccine_df.iloc[-2]['total_cum/total_pop']],
                               text=[f"{round(vaccine_df.iloc[-2]['total_cum/total_pop'],2)}%"],
                               mode='markers+text',
                               marker=dict(color='#a88905', size=1),
                               # textfont=dict(color='', size=20),
                               textposition='middle left',
                               showlegend=False)

vaccine_population.add_scatter(x=[vaccine_df.iloc[-2]['date']],
                               y=[vaccine_df.iloc[-2]['first/total_pop']],
                               text=[f"{round(vaccine_df.iloc[-2]['first/total_pop'],2)}%"],
                               mode='markers+text',
                               marker=dict(color='#009dc4', size=1),
                               # textfont=dict(color='', size=20),
                               textposition='middle left',
                               showlegend=False)


#
# vaccine_population.add_annotation(x='2021-05-09', #[vaccine_df['date'].iloc[-1]]
#                                   y='10',  #[vaccine_df['total_cum/total_pop'].iloc[-1]]
#                                   textposition='bottom',
#                                   text='xxxxxxx',
#                                   showarrow=True,
#                                   arrowhead=1
#                                   )





st.plotly_chart(vaccine_population)



# daily vaccine
vaccine_daily = px.bar(vaccine_df, x='date', y=['dose1_daily','dose2_daily'],
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

# vaccine_daily.update_traces(marker_color=['green', 'blue'])
vaccine_daily.update_layout(yaxis_title=None, legend_title_text='')

custom_legend_name(fig=vaccine_daily,new_names=['1st dose', '2nd dose'])
# vaccine_daily.data[0].marker.line.color = ""


st.plotly_chart(vaccine_daily)


# daily vaccine


#average of xxx doses a day in the past 14 days
















# schedule.every().day.at('07:00').do(job)
# schedule.every().day.at('19:20').do(job)
# schedule.every().day.at('19:30').do(job)
# schedule.every().day.at('20:00').do(job)
# schedule.every(1).second.do(job)
# st.experimental_rerun()

# #
# while True:
#     schedule.run_pending()
#     time.sleep(1)