import streamlit as sl
import polars as pl
from streamlit_lottie import st_lottie
import requests
df1 = pl.read_csv("aqi_clean_state.csv")

sl.set_page_config(page_title="Aeris", page_icon=r"C:\Users\tempe\OneDrive\Documents\Air quality project\Aeris.png")
url = "https://lottie.host/53587c86-e5ba-45b2-bed3-5aeb93a73da5/uBfVjhmifJ.json"
response = requests.get(url)
animation_json = response.json()
st_lottie(animation_json, height=300, key="lottie2")

sl.title("📊 AQI Charts")
sl.bar_chart(df1['State Average AQI', 'state'], x = 'state', y = 'State Average AQI', x_label= "State")
sl.bar_chart(df1['State Median AQI', 'state'], x = 'state', y = 'State Median AQI', x_label= "State")
sl.bar_chart(df1['State Max AQI', 'state'], x = 'state', y ='State Max AQI', x_label="State")
sl.scatter_chart(df1['State dominant pollutant', 'state'], x = 'state', y = 'State dominant pollutant', x_label= "State")
