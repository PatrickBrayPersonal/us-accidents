import plotly.express as px
from src.data.cfg import days_of_week


def kde(accs, coords):
    coords["lon"] = coords["lng"]
    del coords["lng"]
    fig = px.density_mapbox(
        accs,
        lat="Start_Lat",
        lon="Start_Lng",
        radius=9,
        animation_frame="Day of Week",
        category_orders={"Day of Week": days_of_week},
        center=coords,
        zoom=10.5,
        opacity=0.3,
        mapbox_style="stamen-terrain",
    )
    return fig
