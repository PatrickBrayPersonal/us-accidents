import streamlit as st
from src.visualization.visualize import kde
import os
import dask.dataframe as dd
from dotenv import find_dotenv, load_dotenv
from pathlib import Path
import plotly.express as px

load_dotenv(find_dotenv())
project_dir = Path(os.getenv("WORKSPACE"))

accs = dd.read_parquet(
    "data/processed/us-accidents.parquet",
    parse_dates=["Start_Time", "End_Time"],
)

accs = accs[accs["State"] == "DC"]
st.plotly_chart(kde(accs))