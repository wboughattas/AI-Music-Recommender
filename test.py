from dash import Dash, html, dcc, Output, Input, State
from dash.exceptions import PreventUpdate
import json
import pandas as pd
import plotly.express as px

with open('data/geojson-counties-usa.csv') as data:
    geojson = json.load(data)

df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
                 dtype={"fips": str})

fig = px.choropleth_mapbox(df, geojson=geojson, locations='fips', color='unemp',
                           color_continuous_scale="Viridis",
                           range_color=(0, 12),
                           mapbox_style="carto-positron",
                           zoom=3, center={"lat": 37.0902, "lon": -95.7129},
                           opacity=0.5,
                           labels={'unemp': 'unemployment rate'}
                           )

fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

app = Dash(__name__)
app.layout = html.Div([
    dcc.Graph(id='graph', figure=fig),
    html.Div(id='textarea', style={'whiteSpace': 'pre-line'})
])


@app.callback(
    Output('textarea', 'children'),
    Input('graph', 'selectedData')
)
def get_highlighted_counties(selectedData):
    print(selectedData)
    return selectedData


if __name__ == '__main__':
    app.run_server(debug=True)
