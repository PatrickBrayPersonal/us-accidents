import plotly.express as px


def kde(accs):
    fig = px.density_mapbox(
        accs.compute(),
        lat="Start_Lat",
        lon="Start_Lng",
        radius=9,
        animation_frame="Start_DOW",
        category_orders={"Start_DOW": list(range(7))},
        center=dict(lat=38.9, lon=-77),
        zoom=10.5,
        opacity=0.3,
        mapbox_style="stamen-terrain",
    )
    return fig
