import os
import dask.dataframe as dd
from dotenv import find_dotenv, load_dotenv
from pathlib import Path
import plotly.express as px

load_dotenv(find_dotenv())
project_dir = Path(os.getenv("WORKSPACE"))

accs = dd.read_parquet(
    project_dir / "data/processed" / Path(os.getenv("PROC_NAME")),
    parse_dates=["Start_Time", "End_Time"],
)

accs = accs[accs["State"] == "DC"]

fig = px.density_mapbox(
    accs.compute(),
    lat="Start_Lat",
    lon="Start_Lng",
    radius=10,
    center=dict(lat=38.9, lon=-77),
    zoom=13,
    opacity=0.3,
    mapbox_style="stamen-terrain",
)
fig.show()
