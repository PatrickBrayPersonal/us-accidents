import plotly.express as px


def kde(df):
    fig = px.density_mapbox(
        df.compute(),
        lat="Start_Lat",
        lon="Start_Lng",
        radius=10,
        center=dict(lat=38.9, lon=-77),
        zoom=13,
        opacity=0.3,
        mapbox_style="stamen-terrain",
    )
    return fig
