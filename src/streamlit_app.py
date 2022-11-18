import streamlit as st
from src.visualization.visualize import kde
import os
import dask.dataframe as dd
from dotenv import find_dotenv, load_dotenv
from pathlib import Path
import requests



## FRONTEND ##
st.title("Accidents in the United States")
st.subheader("Visualize traffic safety in any neighborhood")

address = st.sidebar.text_input('Lookup your address', key='address')
radius = st.sidebar.text_input('Search radius', key='radius')

def get_lat_lon():
    placesapikey = os.getenv("API_KEY")
    url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=" + st.session_state.address.replace(" ", "%2C" ) + "&inputtype=textquery&fields=formatted_address%2Cname%2Crating%2Copening_hours%2Cgeometry&key=" + placesapikey
    response = requests.request("GET", url, headers={}, data={})
    result = response.json()['candidates'][0]
    print(result)
    return result['geometry']['location']['lat'], result['geometry']['location']['lng']
lat_lon = st.sidebar.button('Find Address', on_click=get_lat_lon)



## VISUALIZATION ##
load_dotenv(find_dotenv())
project_dir = Path(os.getenv("WORKSPACE"))

accs = dd.read_parquet(
    "data/processed/us-accidents.parquet",
    parse_dates=["Start_Time", "End_Time"],
)

accs = accs[accs["State"] == "DC"]
st.plotly_chart(kde(accs))
