import streamlit as st
from src.visualization.visualize import kde
from src.data.gcp_pull import get_accidents
from src.data.preprocess import get_dayofweek
import os
import dask.dataframe as dd
from dotenv import find_dotenv, load_dotenv
from pathlib import Path
import requests
import pandas as pd

load_dotenv(find_dotenv())


## FRONTEND ##
st.title("Accidents in the United States")
st.subheader("Visualize traffic safety in any neighborhood")

address = st.sidebar.text_input("Lookup your address", key="address")
radius = st.sidebar.text_input("Search radius", key="radius")


@st.cache
def get_lat_lon():
    placesapikey = os.getenv("API_KEY")
    url = (
        "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input="
        + st.session_state.address.replace(" ", "%2C")
        + "&inputtype=textquery&fields=formatted_address%2Cname%2Crating%2Copening_hours%2Cgeometry&key="
        + placesapikey
    )
    response = requests.request("GET", url, headers={}, data={})
    result = response.json()["candidates"][0]
    st.session_state["coords"] = {
        "lat": result["geometry"]["location"]["lat"],
        "lng": result["geometry"]["location"]["lng"],
    }
    st.session_state["accs"] = get_accidents(st.session_state["coords"], 1)


st.sidebar.button("Find Address", on_click=get_lat_lon)
## VISUALIZATION ##
if "accs" not in st.session_state:
    st.session_state["accs"] = pd.DataFrame()
if len(st.session_state["accs"]) > 0:
    st.plotly_chart(
        kde(get_dayofweek(st.session_state["accs"]), st.session_state["coords"])
    )
