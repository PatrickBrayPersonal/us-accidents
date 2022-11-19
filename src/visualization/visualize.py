import plotly.express as px


def get_center(accs):
    return dict(lat=accs.Start_Lat.mean(), lon=accs.Start_Lng.mean())

def kde(accs):
    print(accs)
    fig = px.density_mapbox(
        accs,
        lat="Start_Lat",
        lon="Start_Lng",
        radius=9,
        animation_frame="Start_DOW",
        category_orders={"Start_DOW": list(range(7))},
        center=get_center(accs),
        zoom=10.5,
        opacity=0.3,
        mapbox_style="stamen-terrain",
    )
    return fig
