import plotly.express as px
from src.data.cfg import days_of_week


def get_center(accs):
    return dict(lat=accs.Start_Lat.mean(), lon=accs.Start_Lng.mean())


def kde(accs):
    fig = px.density_mapbox(
        accs,
        lat="Start_Lat",
        lon="Start_Lng",
        radius=9,
        animation_frame="Day of Week",
        category_orders={"Day of Week": days_of_week},
        center=get_center(accs),
        zoom=10.5,
        opacity=0.3,
        mapbox_style="stamen-terrain",
    )
    return fig
