import plotly.express as px
from src.data.cfg import days_of_week
from src.data.preprocess import split_by
import copy


def kde(accs, coords, split):
    # modify coords
    coords = copy.copy(coords)
    coords["lon"] = coords["lng"]
    del coords["lng"]

    accs, orders = split_by(accs, split)
    fig = px.density_mapbox(
        accs,
        lat="Start_Lat",
        lon="Start_Lng",
        z="weight",
        radius=9,
        animation_frame=split,
        category_orders=orders,
        center=coords,
        zoom=10.5,
        opacity=0.3,
        mapbox_style="stamen-terrain",
    )
    return fig
