import dash
import plotly.validator_cache
import json


# meta_tags are required for the app layout to be mobile responsive

external_stylesheets = ['assets/bWLwgP.css', 'assets/styles.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5'}],
                )

server = app.server

try:
    india_geojson = "https://kadatatlukishore.github.io/states_india.geojson"
except:
    india_geojson = json.load(open("states_india.geojson", "r"))



