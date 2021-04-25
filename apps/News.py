from GoogleNews import GoogleNews
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
from datetime import date, timedelta

from app import app   # should import for multi-page app

layout = html.Div([
    html.Div([
        html.H4('News', style={'text-align': 'center', 'background-color': 'black',
                               'border': '1px solid black',
                               'padding': '5px',
                               'margin': '5px',
                               'border-radius': '10px',
                               'box-shadow': '0 0 10px',
                               'color': 'white'})
    ], className='row'),
    html.Div([
        dcc.Loading(children=[html.Div(id="News")], color="#119DFF", type="bar", fullscreen=False)
    ], className='row', style={'background-color': 'white',
                               'border': '1px solid black',
                               'padding': '5px',
                               'margin': '5px',
                               'border-radius': '10px',
                               'box-shadow': '0 0 10px',
                               'min-height': '200px'
                               }),

    dcc.Dropdown(id="Hidden", style={'display': 'none'})
])


@app.callback(Output("News", 'children'),
              [Input("Hidden", 'value'), Input('intervals1', 'n_intervals')])
def news_data(value, n):
    try:  # For covid news in india
        # Using google news api get the news ...
        googlenews = GoogleNews(lang='en')
        googlenews.set_time_range(start=date.today() - timedelta(days=1), end=date.today())
        googlenews.get_news('Covid-India')
        data = pd.json_normalize(googlenews.results()[:5])
    except:  # For Country news if the above one fails
        googlenews = GoogleNews(lang='en')
        googlenews.set_time_range(start=date.today() - timedelta(days=1), end=date.today())
        googlenews.get_news('India')
        data = pd.json_normalize(googlenews.results()[:5])

    return html.Div([
        html.Div([
            html.H3(data['title'][0], style={'text-align': 'center', 'font-family': 'sans-serif', 'font-weight': 'bold'}),
            html.P(data['desc'][0]),
            html.P(data['date'][0], style={'float': 'left'}),

            html.A("Link to News ", href="https://"+data['link'][0], style={'float': 'right'}, target="_blank"),

        ], className='twelve columns', style={'background-color': 'white',
                                              'border': '1px solid black',
                                              'padding': '5px',
                                              'margin': '5px',
                                              'border-radius': '10px',
                                              'box-shadow': '0 0 10px'
                                              }),
        html.Div([
            html.H3(data['title'][1], style={'text-align': 'center', 'font-family': 'sans-serif', 'font-weight': 'bold'}),
            html.P(data['desc'][1]),
            html.P(data['date'][1], style={'float': 'left'}),
            html.A("Link to News ", href="https://"+data['link'][1], style={'float': 'right'}, target="_blank")
        ], className='twelve columns', style={'background-color': 'white',
                                              'border': '1px solid black',
                                              'padding': '5px',
                                              'margin': '5px',
                                              'border-radius': '10px',
                                              'box-shadow': '0 0 10px'
                                              }),
        html.Div([
            html.H3(data['title'][2], style={'text-align': 'center', 'font-family': 'sans-serif', 'font-weight': 'bold'}),
            html.P(data['desc'][2]),
            html.P(data['date'][2], style={'float': 'left'}),
            html.A("Link to News ", href="https://"+data['link'][2], style={'float': 'right'}, target="_blank")
        ], className='twelve columns', style={'background-color': 'white',
                                              'border': '1px solid black',
                                              'padding': '5px',
                                              'margin': '5px',
                                              'border-radius': '10px',
                                              'box-shadow': '0 0 10px'
                                              }),
        html.Div([
            html.H3(data['title'][3], style={'text-align': 'center', 'font-family': 'sans-serif', 'font-weight': 'bold'}),
            html.P(data['desc'][3]),
            html.P(data['date'][3], style={'float': 'left'}),
            html.A("Link to News ", href="https://"+data['link'][3], style={'float': 'right'}, target="_blank")
        ], className='twelve columns', style={'background-color': 'white',
                                              'border': '1px solid black',
                                              'padding': '5px',
                                              'margin': '5px',
                                              'border-radius': '10px',
                                              'box-shadow': '0 0 10px'
                                              }),
        html.Div([
            html.H3(data['title'][4], style={'text-align': 'center', 'font-family': 'sans-serif', 'font-weight': 'bold'}),
            html.P(data['desc'][4]),
            html.P(data['date'][4], style={'float': 'left'}),
            html.A("Link to News ", href="https://"+data['link'][4], style={'float': 'right'}, target="_blank")
        ], className='twelve columns', style={'background-color': 'white',
                                              'border': '1px solid black',
                                              'padding': '5px',
                                              'margin': '5px',
                                              'border-radius': '10px',
                                              'box-shadow': '0 0 10px',
                                              'Align': 'center'
                                              })

    ], className='row')
