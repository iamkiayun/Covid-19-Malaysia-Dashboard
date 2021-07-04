
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

@st.cache(allow_output_mutation=True)
def load_data():
    url = "https://newslab.malaysiakini.com/covid-19/en"
    html = requests.get(url).text
    bs = BeautifulSoup(html, 'lxml')
    script = bs.find('script', id='__NEXT_DATA__')
    json_object = json.loads(script.contents[0])
    props = json_object['props']
    page_props= props['pageProps']
    chartdata= page_props['chartData']
    data=chartdata
    chartdata_df = pd.DataFrame.from_dict(data)
    chartdata_df['date'] = pd.to_datetime(chartdata_df['date'], utc=False)
    chartdata_df.sort_values(by=['date'], ascending=False, inplace=True)
    chartdata_df['date'] = chartdata_df['date'].dt.strftime('%d %b %y')
    chartdata_df['Positivity rate'] = pd.to_numeric(chartdata_df['Positivity rate'], errors='coerce')
    chartdata_df['Positivity rate'] = (chartdata_df['newCase']/chartdata_df['newTest'])*100
    chartdata_df['Positivity rate']= chartdata_df['Positivity rate'].round(2)
    chartdata_df['newTest']= chartdata_df['newTest'].replace(0, np.nan)
    return chartdata_df.to_csv('covid_data_updated_descending.csv')


def last_update():
    url = "https://newslab.malaysiakini.com/covid-19/en"
    html = requests.get(url).text
    bs = BeautifulSoup(html, 'lxml')
    updated_date = bs.find('div', class_='jsx-2630654232 uk-text-small uk-text-center')
    with open('update_datetime.txt', 'w') as f:
        f.write(updated_date.text)

def load_data2():
    url = "https://newslab.malaysiakini.com/covid-19/en"
    html = requests.get(url).text
    bs = BeautifulSoup(html, 'lxml')
    script = bs.find('script', id='__NEXT_DATA__')
    json_object = json.loads(script.contents[0])
    props = json_object['props']
    page_props= props['pageProps']
    chartdata= page_props['chartData']
    data=chartdata
    chartdata_df2 = pd.DataFrame.from_dict(data)
    chartdata_df2['date'] = pd.to_datetime(chartdata_df2['date'], utc=False)
    chartdata_df2.sort_values(by=['date'], ascending=True, inplace=True)
    chartdata_df2['date'] = chartdata_df2['date'].dt.strftime('%d %b %y')
    chartdata_df2['Positivity rate'] = pd.to_numeric(chartdata_df2['Positivity rate'], errors='coerce')
    chartdata_df2['Positivity rate'] = (chartdata_df2['newCase']/chartdata_df2['newTest'])*100
    chartdata_df2['Positivity rate']= chartdata_df2['Positivity rate'].round(2)
    chartdata_df2['newTest']= chartdata_df2['newTest'].replace(0, np.nan)
    return chartdata_df2.to_csv('covid_data_updated_ascending.csv')


def job():
    load_data()
    load_data2()
    last_update()

schedule.every().day.at('13:00').do(job)
schedule.every().day.at('15:00').do(job)
schedule.every().day.at('17:00').do(job)
schedule.every().day.at('20:00').do(job)
schedule.every().day.at('22:00').do(job)






chartdata_df = pd.read_csv('covid_data_updated_descending.csv')

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


st.write(chartdata_df)
# st.line_chart(chartdata_df)


chartdata_df2 = pd.read_csv('covid_data_updated_ascending.csv')
# chartdata_df2['date'] = pd.to_datetime(chartdata_df2['date'], format= '%d %b %Y')
# chartdata_df2 = chartdata_df2.sort_values('date')
# chartdata_df2['date'] = chartdata_df2['date'].dt.strftime('%d %b %y')
# chartdata_df2.sort_values(by=['date'], inplace=True)
graph = px.bar(chartdata_df2, x='date', y='totalCase')
st.plotly_chart(graph)


while True:
    schedule.run_pending()
    time.sleep(1)