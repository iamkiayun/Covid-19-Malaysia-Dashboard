
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
* **Data source:** [KKM's daily report](https://t.me/cprckkm)
""")

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

new_cases, new_death, total_case, total_Icu,  = st.beta_columns(4)
with new_cases:
    st.markdown('**New Cases**')
    new_case_no = chartdata_df['newCase'].iloc[0]
    total_test_conducted = chartdata_df['newTest'].iloc[0]
    positive_rate = chartdata_df['Positivity rate'].iloc[0]
    st.markdown(f"<h3 style='text-align: left;'>{new_case_no}</h3>", unsafe_allow_html=True)
    st.markdown(f"<h5 style='text-align: left;'>test: {int(total_test_conducted)}</h5>", unsafe_allow_html=True)
    st.markdown(f"<h5 style='text-align: left;'>+ve rate: {positive_rate}%</h5>", unsafe_allow_html=True)


with new_death:
    st.markdown('**New Deaths**')

with total_case:
    st.markdown('**Total Cases**')

with total_Icu:
    st.markdown('**Current ICU**')


# st.write(chartdata_df)
chartdata_df['Positivity rate'] = chartdata_df['Positivity rate'] .map('{:,.2f}'.format)
column_list = chartdata_df.drop(['date','Positivity rate'], axis=1).columns.tolist()
chartdata_df[column_list] = chartdata_df[column_list].fillna(0).astype(dtype=int)
s = chartdata_df.style.format('{:,}', subset=column_list)
st.dataframe(s)


#cummulative confirmed cases
graph = px.bar(chartdata_df2, x='date', y='totalCase',
               labels={
                   'date': '',
                   'totalCase':''
               },
               title='Confirmed cases')
st.plotly_chart(graph)

# positive rate
positive_rate_daily = px.bar(chartdata_df2, x='date', y='Positivity rate',
                       labels= {
                           "date": "",
                           "total_daily": "Positivity Rate (%)"
                       },
                       title='Daily Positivity Rate')

st.plotly_chart(positive_rate_daily)



st.header('National Vaccination Progress')


#cummulative vaccine

# vaccine_cumul = px.bar(vaccine_df, x='date', y='total_cumul',
#                        labels={
#                            "date": "",
#                            "total_cumul": "Total cumulative"
#                        },
#                        title='Total cummulative vaccine doses administered (1st dose + 2nd dose)')
# st.plotly_chart(vaccine_cumul)
#total population is estimated at 32.65 million
total_pop = population_df.iloc[0]['pop']
vaccine_df['total_cum/total_pop'] = vaccine_df['dose2_cumul']/ total_pop*100
vaccine_population = px.line(vaccine_df, x='date', y='total_cum/total_pop',
                       labels={
                           "date": "",
                           "total_cum/total_pop": "Total 2nd Dose / Total Population (%)"
                       },
                       title='Population fully vaccinated (completed 1st & 2nd dose)')
st.plotly_chart(vaccine_population)




# daily vaccine
vaccine_daily = px.bar(vaccine_df, x='date', y='total_daily',
                       labels= {
                           "date": "",
                           "total_daily": ""
                       },
                       title='Daily vaccine doses administered (1st dose + 2nd dose)')
# vaccine_daily.update_layout()
st.plotly_chart(vaccine_daily)

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