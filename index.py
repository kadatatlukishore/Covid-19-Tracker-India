import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.validator_cache
import pandas as pd
import requests
import json

from datetime import datetime
# Connect to main app.py file
from app import app
from app import server
from apps import dashboard, predictions, News

app.title = 'Covid-19'


def load_data():  # Function used to Request API and cleaning the data
    response = requests.get("https://api.covid19india.org/data.json")
    content = json.loads(response.text)
    Country = pd.DataFrame(content['cases_time_series'],
                           columns=['dailyconfirmed', 'dailydeceased', 'dailyrecovered', 'dateymd', 'totalconfirmed',
                                    'totaldeceased',
                                    'totalrecovered'])

    state_wise = pd.DataFrame(content['statewise'],
                              columns=['active', 'confirmed', 'deaths', 'deltaconfirmed', 'deltadeaths',
                                       'deltarecovered', 'lastupdatedtime',
                                       'recovered', 'state', 'statecode'])
    Country[['dailyconfirmed', 'dailydeceased', 'dailyrecovered', 'totalconfirmed', 'totaldeceased',
             'totalrecovered']] = Country[
        ['dailyconfirmed', 'dailydeceased', 'dailyrecovered', 'totalconfirmed', 'totaldeceased',
         'totalrecovered']].apply(pd.to_numeric)
    Country['dateymd'] = pd.to_datetime(Country['dateymd'])

    state_wise[['active', 'confirmed', 'deaths', 'deltaconfirmed', 'deltadeaths', 'deltarecovered',
                'recovered']] = state_wise[
        ['active', 'confirmed', 'deaths', 'deltaconfirmed', 'deltadeaths', 'deltarecovered',
         'recovered']].apply(pd.to_numeric)
    state_wise['lastupdatedtime'] = pd.to_datetime(state_wise['lastupdatedtime'])
    states = []
    for state in state_wise['state']:
        if state == 'Jammu and Kashmir':
            states.append('Jammu & Kashmir')
        elif state == "Delhi":
            states.append("NCT of Delhi")
        else:
            states.append(state)  # Choropleth using Indian state names doesn't contain 'Jammu and Kashmir' but 'Jammu & Kashmir'

    state_wise['state'] = states
    # print(Country.head(), state_wise.head())
    return Country, state_wise


def bottom1():
    return html.Div([
        html.Div([
            html.H6('')
        ], className='five columns'),
        html.Div([
            html.A("LinkedIn", href='https://www.linkedin.com/in/kadatatlukishore/', target="_blank",
                   style={'background-color': '#B2CDEC', 'height': '70px',
                          'border': '1px solid black',
                          'padding': '5px',
                          'margin': '5px',
                          'border-radius': '2px',
                          'box-shadow': '0 0 10px',
                          'text-align': 'center',
                          'color': 'black'
                          }
                   )
        ], className='one column'),
        html.Div([
            html.A("GitHub", href='https://github.com/kadatatlukishore', target="_blank",
                   style={'background-color': '#B2CDEC', 'height': '70px',
                          'border': '1px solid black',
                          'padding': '5px',
                          'margin': '5px',
                          'border-radius': '2px',
                          'box-shadow': '0 0 10px',
                          'text-align': 'center',
                          'color': 'black'
                          })
        ], className='one column'),
        html.Div([
            html.H6('')
        ], className='six columns')
    ], className='row')


# THIS IS FRONT-END LAYOUT

app.layout = html.Div([
    html.Div([
        html.Img(
            src="../assets/sars-cov-19.jpg",
            style={
                'height': '50px',
                'float': 'right',
                'width': '50px',
                'background-color': 'black',
                'border': '1px solid white',
                'border-radius': '50%',
                'display': 'inline',
                'box-shadow': '0 0 5px'
            }
        ),
        html.H1(children='Covid-19 India Tracker', style={'text-align': 'center',
                                                          'color': 'white'}),
        html.P("(INDIA will fight against COVID-19)", style={'text-align': 'center',
                                                             'color': 'white'})
    ], className='row', style={'background-color': 'black', 'width': '1480px',
                               'border': '1px solid black',
                               'padding': '5px',
                               'margin': '5px',
                               'border-radius': '10px',
                               'box-shadow': '0 10px 15px grey'
                               }),
    dcc.Dropdown(id='data', style={'display': 'none'}),
    # Hidden div inside the app that stores the intermediate value
    html.Div(id='Store-Data', style={'display': 'none'}),
    dcc.Location(id='url', refresh=True),

    html.Div([
        html.Div([
            dcc.Link("DASHBOARD", href='/apps/dashboard', style={'text-align': 'center',
                                                                 'fontSize': 20,
                                                                 'font-family': 'sans-serif',
                                                                 'background-color': '#B2CDEC',
                                                                 'height': '50px',
                                                                 'width': '320px',
                                                                 'border': '1px solid black',
                                                                 'padding': '5px',
                                                                 'margin': '5px',
                                                                 'border-radius': '5px',
                                                                 'box-shadow': '0 0 10px grey',
                                                                 'color': 'black'
                                                                 }, className='three columns'),
            dcc.Link("PREDICTIONS", href='/apps/predictions', style={'text-align': 'center',
                                                                     'fontSize': 20,
                                                                     'font-family': 'sans-serif',
                                                                     'background-color': '#B2CDEC',
                                                                     'height': '50px',
                                                                     'width': '320px',
                                                                     'border': '1px solid black',
                                                                     'padding': '5px',
                                                                     'margin': '5px',
                                                                     'border-radius': '5px',
                                                                     'box-shadow': '0 0 10px grey',
                                                                     'Align': 'center',
                                                                     'color': 'black'
                                                                     }, className='three columns'),
            dcc.Link("NEWS", href='/apps/News', style={'text-align': 'center',
                                                       'fontSize': 20,
                                                       'font-family': 'sans-serif',
                                                       'background-color': '#B2CDEC',
                                                       'height': '50px',
                                                       'width': '320px',
                                                       'border': '1px solid black',
                                                       'padding': '5px',
                                                       'margin': '5px',
                                                       'border-radius': '5px',
                                                       'box-shadow': '0 0 10px grey',
                                                       'Align': 'center',
                                                       'color': 'black'
                                                       }, className='three columns'),
            html.A("COVID-RESOURCES TO HELP PEOPLE", href='http://nixxer.in/covid', target="_blank",
                   style={'background-color': '#377D43', 'height': '50px',
                          'width': '320px',
                          'fontSize': 15,
                          'font-family': 'sans-serif',
                          'Align': 'center',
                          'border': '1px solid black',
                          'padding': '5px',
                          'margin': '5px',
                          'border-radius': '5px',
                          'box-shadow': '0 0 10px',
                          'text-align': 'center',
                          'color': 'white'
                          }, className="two columns"),
            html.A("MORE RESOURCES", href='https://kadatatlukishore.github.io/covid-resources.html', target="_blank",
                   style={'background-color': '#377D43', 'height': '50px',
                          'width': '160px',
                          'fontSize': 15,
                          'font-family': 'sans-serif',
                          'Align': 'center',
                          'border': '1px solid black',
                          'padding': '5px',
                          'margin': '5px',
                          'border-radius': '5px',
                          'box-shadow': '0 0 10px',
                          'text-align': 'center',
                          'color': 'white'
                          }, className="one column")
        ], className='row'),

    ]),
    # The page-content will show up here....
    html.Div(id='page-content', children=[]),

    html.Div([
        html.Div([
            html.H5('Wear Masks, Use Sanitizers and Stay Safe !!',
                    style={'text-align': 'center', 'background-color': '#377D43',
                           'border': '1px solid black',
                           'padding': '5px',
                           'margin': '5px',
                           'border-radius': '5px',
                           'box-shadow': '0 0 10px',
                           'color': 'white'})
        ], className='row'),
        html.Div([
            html.H6('Data Source & References', style={'text-align': 'center', 'background-color': 'black',
                                                       'border': '1px solid black',
                                                       'padding': '5px',
                                                       'margin': '5px',
                                                       'border-radius': '5px',
                                                       'box-shadow': '0 0 10px',
                                                       'color': 'white'})
        ], className='row'),
        html.Div([
            html.P("     API :  https://api.covid19india.org/data.json",
                   style={'text-align': 'center'}),
            html.P("Dash :  https://dash.plotly.com/",
                   style={'text-align': 'center'}),
            html.H6('Reach me', style={'text-align': 'center', 'background-color': 'black',
                                       'border': '1px solid black',
                                       'padding': '5px',
                                       'margin': '5px',
                                       'border-radius': '5px',
                                       'box-shadow': '0 0 10px',
                                       'color': 'white'})
        ], className='row'),

        bottom1(),

    ], style={'background-color': 'white', 'width': '1480px',
              'border': '1px solid black',
              'padding': '5px',
              'margin': '5px',
              'border-radius': '10px',
              'box-shadow': '0 0 10px'
              }),
    dcc.Interval(
        id='intervals1',
        interval=7200 * 1000,  # update after every two hours
        n_intervals=0
    )
])


# This Callback helps to store the data in the hidden div (Concept: sharing data between callback, Refer: Dash documentation)


@app.callback(
    Output('Store-Data', 'children'),
    [Input('data', 'value'), Input('intervals1', 'n_intervals')])
def cleaned_data(value, n):
    Country, state_wise = load_data()

    datasets = {
        'Country': Country.to_json(orient='split', date_format='iso'),
        'state_wise': state_wise.to_json(orient='split', date_format='iso')
    }

    return json.dumps(datasets)  # storing data in json format


# This callback helps to switch between the tabs(pages)


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/dashboard':
        return dashboard.layout
    elif pathname == '/apps/predictions':
        return predictions.layout  # returning prediction page layout
    elif pathname == '/apps/News':
        return News.layout
    else:
        return dashboard.layout  # Dashboard stays as a default layout


if __name__ == '__main__':
    app.run_server(debug=False)
