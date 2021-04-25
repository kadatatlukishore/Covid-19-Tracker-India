import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import json
from dash.dependencies import Input, Output, State
from app import app
from Model import model_and_graphs
# import time

try:
    layout = html.Div([
        html.Div([
            html.H4(' Cases & Deaths Prediction', style={'text-align': 'center', 'background-color': 'black',
                                                         'border': '1px solid black',
                                                         'padding': '5px',
                                                         'margin': '5px',
                                                         'border-radius': '10px',
                                                         'box-shadow': '0 0 10px',
                                                         'color': 'white'})
        ], className='row'),
        html.P('Model Training takes 15-30sec please wait.....', style={'text-align': 'right',
                                                                        'color': 'Red'}),
        html.Div([
            dcc.Dropdown(id='Cases-and-Deaths', options=[{'label': 'Cases', 'value': 'dailyconfirmed'},
                                                         {'label': 'Deaths', 'value': 'dailydeceased'}],
                         value='dailyconfirmed', style={'width': '720px',
                                                        'border': '1px solid black',
                                                        'padding': '1px',
                                                        'margin': '1px',
                                                        'border-radius': '5px',
                                                        'box-shadow': '0 0 5px'
                                                        }),
            dcc.Loading(children=[dcc.Graph(id='figure1')], color="#119DFF", type="bar", fullscreen=False)

        ], className='row', style={'background-color': 'white', 'width': '1480px',
                                   'border': '1px solid black',
                                   'padding': '5px',
                                   'margin': '5px',
                                   'border-radius': '10px',
                                   'box-shadow': '0 0 10px'
                                   }),
        html.Div([
            html.Div([
                html.H6('Model Summary', style={'text-align': 'center', 'background-color': 'black',
                                                'border': '1px solid black',
                                                'padding': '5px',
                                                'margin': '5px',
                                                'border-radius': '10px',
                                                'box-shadow': '0 0 10px',
                                                'color': 'white'}, className='six columns')
            ], className='row'),
            html.Div([
                dcc.Loading(children=[html.Div(id='table1')], color="#119DFF", type="bar", fullscreen=False),
                # dcc.Loading(children=[html.Div(id='table2')], color="#119DFF", type="bar", fullscreen=False)

            ], className='six columns', style={'background-color': 'white', 'width': '730px',
                                               'height': '100px',
                                               'border': '1px solid black',
                                               'padding': '5px',
                                               'margin': '5px',
                                               'border-radius': '10px',
                                               'box-shadow': '0 0 10px'
                                               })

        ], className='row'),
        html.Div([
            html.P("*Predictions may not be accurate....", style={
                'color': 'red', 'text-align': 'center'
            })
        ])
    ])


    @app.callback([Output('figure1', 'figure'),
                   Output('table1', 'children')],
                  [Input('Store-Data', 'children'), Input('Cases-and-Deaths', 'value')],
                  [State('Cases-and-Deaths', 'value')])
    def model_data(jsonified_cleaned_data, value, val):
        # begin = time.time()
        datasets = json.loads(jsonified_cleaned_data)
        data = pd.read_json(datasets['Country'], orient='split')
        data['dateymd'] = pd.to_datetime(data['dateymd'], format="%Y-%m-%d")

        fig, table_1 = model_and_graphs(data, value)
        # end = time.time()
        # print('Total time taken', end-begin)
        return fig, table_1

except:

    layout = html.Div([
        html.P("Error Occurred... Please visit the dashboard page...", style={
            'color': 'red', 'text-align': 'center'
        })
    ])
