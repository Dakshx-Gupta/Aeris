import os
import polars
import streamlit as sl
import requests
from streamlit_lottie import st_lottie

url = 'https://api.data.gov.in/resource/3b01bcb8-0b14-4abf-b6f2-c1bfd384ba69?api-key=579b464db66ec23bdd000001afe11a655d104e004ee570abee8915a3&format=csv'
response = requests.get(url)
path = os.path.join(os.getcwd(), "aqi_data.csv")
df = polars.read_csv("aqi_data.csv", ignore_errors=True, columns=["state", "city","pollutant_id","pollutant_min","pollutant_max","pollutant_avg", "latitude", "longitude"])
df = df.with_columns([
    polars.col("pollutant_avg").cast(polars.Int64, strict=False),
    polars.col("pollutant_max").cast(polars.Int64, strict=False)
])
df = df.filter(
    polars.col("latitude").is_not_null() & polars.col("longitude").is_not_null()
)

result = (
    df.group_by("state")
    .agg(([
        polars.col("pollutant_avg").mean().round(0).alias("State Average AQI"),
        polars.col("pollutant_max").max().alias("State Max AQI"),
        polars.col("pollutant_min").min().alias("State Min AQI"),
        polars.col("pollutant_avg").median().alias("State Median AQI"),
        polars.col("pollutant_id").mode().first().alias("State dominant pollutant"),
        polars.col("latitude").unique().first().alias("lat"),
        polars.col("longitude").unique().first().alias("lon")
    ])).sort("state")
)

result = result.with_columns(polars.col("state").str.replace_all("_", " "))
result.write_csv(r"aqi_clean_state.csv")
df1 = polars.read_csv("aqi_clean_state.csv", columns=['state', 'State Average AQI', 'State Max AQI', 'State Min AQI', 'State Median AQI','State dominant pollutant', 'lat', 'lon'])

# Streamlit settings

sl.set_page_config(page_title="Aeris", page_icon=r"C:\Users\tempe\OneDrive\Documents\Air quality project\Aeris.png")
url = "https://lottie.host/33b98c8d-fd24-479b-b90b-69500521c9e9/tdpfxEpkDZ.json"
response = requests.get(url)
animation_json = response.json()
st_lottie(animation_json, height=300, key="lottie1")

sl.logo("Aeris.png", size='large')
sl.title(":red[Aeris]")
sl.link_button("Github", url="https://github.com/Dakshx-Gupta", icon="🐙")
sl.link_button("LinkedIN", url="https://www.linkedin.com/in/daksh-gupta-a0942a27b/", icon="💼")


state_input = sl.selectbox("Select a State:", sorted(df1["state"]))
if state_input:
    result = df1.filter(polars.col("state") == state_input)
    sl.subheader(f"Air Quality in {state_input}")
    sl.metric("Average AQI", result["State Average AQI"], border=True, width= 225)
    pollutant = result["State dominant pollutant"].item()

    # Other metrics in 3 columns
    col1, col2, col3 = sl.columns(3)
    with col1:
        sl.metric("Median AQI", result["State Median AQI"], border=True)
        
    with col2:
        sl.metric("Max AQI", result["State Max AQI"], border=True)
        
    with col3:
        sl.metric("Min AQI", result["State Min AQI"], border=True)

    # Dominant pollutant
    sl.metric("Dominant Pollutant", pollutant, border=True, width=225)
