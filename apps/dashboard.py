import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output, State
import plotly.validator_cache
import plotly.express as px
import json
import time
from plotly.subplots import make_subplots
from app import app
from app import india_geojson

layout = html.Div([
    html.P('*Select the above tabs.....', style={'text-align': 'right',
                                                 'color': 'Red'}),
    html.Div([
        html.H4('Covid19 Dashboard', style={'text-align': 'center', 'background-color': 'black',
                                            'border': '1px solid black',
                                            'padding': '5px',
                                            'margin': '5px',
                                            'border-radius': '10px',
                                            'box-shadow': '0 0 10px',
                                            'color': 'white'})
    ], className='row'),
    html.Div([
        html.Div([
            dcc.Dropdown(id='DailyCases', options=[{'label': 'Daily', 'value': 'daily'},
                                                   {'label': 'Cumulative', 'value': 'cumulative'}],
                         value='daily', style={'width': '720px',
                                               'border': '1px solid black',
                                               'padding': '1px',
                                               'margin': '1px',
                                               'border-radius': '5px',
                                               'box-shadow': '0 0 5px'
                                               }),
            dcc.Loading(children=[dcc.Graph(id="line-chart", style={'background-color': 'white', 'width': '720px',
                                                                    'border': '1px solid black',
                                                                    'padding': '5px',
                                                                    'margin': '5px',
                                                                    'border-radius': '10px',
                                                                    'box-shadow': '0 0 10px'
                                                                    })], color="#119DFF", type="bar", fullscreen=False)
        ], className='six columns'),
        html.Div([
            dcc.Loading(children=[
                dcc.Graph(id='Indicator', style={'background-color': 'white', 'width': '700px',
                                                 'border': '1px solid black',
                                                 'padding': '5px',
                                                 'margin': '5px',
                                                 'border-radius': '10px',
                                                 'box-shadow': '0 0 10px'
                                                 })
            ], color="#119DFF", type="bar", fullscreen=False),
        ], className='six columns')
    ], className='row'),
    html.Div([
        html.P('State-Wise Data'),
        html.Div([
            dcc.Loading([html.Div(id='content')], color="#119DFF", type="bar", fullscreen=False)
        ], className='six columns', style={'background-color': 'white',
                                           'width': '710px',
                                           'min-height': '200px',
                                           'border': '1px solid black',
                                           'padding': '5px',
                                           'margin': '5px',
                                           'border-radius': '10px',
                                           'box-shadow': '0 0 10px'
                                           }),
        html.Div([
            html.Div([
                dcc.Dropdown(id='cases', options=[{'label': 'Active cases', 'value': 'active'},
                                                  {'label': 'Deaths', 'value': 'deaths'},
                                                  {'label': 'Recovery', 'value': 'recovered'}],
                             value='active', style={'width': '720px',
                                                    'border': '1px solid black',
                                                    'padding': '1px',
                                                    'margin': '1px',
                                                    'border-radius': '5px',
                                                    'box-shadow': '0 0 5px'
                                                    })
            ]),
            dcc.Loading(children=[
                dcc.Graph(id='maps', style={'background-color': 'white', 'width': '700px',
                                            'border': '1px solid black',
                                            'padding': '5px',
                                            'margin': '5px',
                                            'border-radius': '10px',
                                            'box-shadow': '0 0 10px'
                                            })
            ], color="#119DFF", type="bar", fullscreen=False),

        ], className='six columns')
    ], className='row')
])


def generate_table(df):  # Dash table formation
    new = df[['state', 'confirmed', 'active', 'recovered', 'deaths',
              'deltaconfirmed', 'deltadeaths', 'deltarecovered']]
    new.rename(columns={'deltaconfirmed': 'Today Confirmed Cases',
                        'deltarecovered': 'Today Recovery', 'deltadeaths': 'Today Deaths'}, inplace=True)
    return html.Div([
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in new.columns],
            data=new.to_dict('records'),
            style_cell_conditional=[
                {'if': {'column_id': 'state'},
                 'width': '250px',
                 'textAlign': 'left'}],
            style_data_conditional=[{
                'if': {'column_id': 'recovered'},
                'backgroundColor': 'rgb(152, 215, 187)',
                'color': 'black'
            },
                {
                    'if': {'column_id': 'deaths'},
                    'backgroundColor': 'rgb(224, 123, 123)',
                    'color': 'black'
                },
                {
                    'if': {'column_id': 'active'},
                    'backgroundColor': 'rgb(161, 185, 215)',
                    'color': 'black'
                },
                {
                    'if': {
                        'column_id': 'Today Confirmed Cases',

                        'filter_query': '{{Today Confirmed Cases}} = {}'.format(new['Today Confirmed Cases'].max())
                    },
                    'backgroundColor': 'rgb(224, 123, 123)',
                    'color': 'white'
                },
                {
                    'if': {
                        'column_id': 'Today Recovery',

                        'filter_query': '{{Today Recovery}} = {}'.format(new['Today Recovery'].max())
                    },
                    'backgroundColor': 'rgb(152, 215, 187)',
                    'color': 'white'
                },
                {
                    'if': {
                        'column_id': 'Today Deaths',

                        'filter_query': '{{Today Deaths}} = {}'.format(new['Today Deaths'].max())
                    },
                    'backgroundColor': 'red',
                    'color': 'white'
                }
            ],
            fixed_columns={'headers': True, 'data': 1},
            page_action='none',
            style_table={'height': '750px', 'overflowY': 'auto', 'overflowX': 'auto',
                         'minWidth': '100%'},
            style_cell={
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
                'fontSize': 15, 'font-family': 'sans-serif',
                'minWidth': '80px', 'width': '150px', 'maxWidth': '120px'
            },

            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold'
            }
        )
    ]

    )


def cumulative(Country):  # line chart for cumulative data
    fig = go.Figure(
        go.Scatter(x=Country['dateymd'], y=Country['totalconfirmed'],
                   line=dict(color='Blue'), name="Total Confirmed", mode='lines+markers', marker=dict(size=5))
    )
    fig.add_trace(go.Scatter(x=Country['dateymd'], y=Country['totaldeceased'],
                             line=dict(color='red'), name="Total Deaths", mode='lines+markers',
                             marker=dict(size=5)))
    fig.add_trace(go.Scatter(x=Country['dateymd'], y=Country['totalrecovered'],
                             line=dict(color='green'), name="Total Recovered", mode='lines+markers',
                             marker=dict(size=5)))
    fig.update_layout(
        autosize=False,
        width=700,
        height=305,
        margin=dict(
            l=1,
            r=1,
            b=1,
            t=1,
            pad=1
        ),
        paper_bgcolor="white",
        plot_bgcolor='#DDE9F5',

        xaxis=dict(showline=False, showgrid=False),
        yaxis=dict(showline=False, showgrid=False)
    )
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )

    return fig


def daily(Country):  # line-chart for daily data
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=Country['dateymd'], y=Country['dailyconfirmed'],
        hoverinfo='x+y',
        mode='lines',
        name="Daily Confirmed Cases",
        line=dict(color='blue'),
        fill="tozeroy",
        fillcolor='rgb(161, 185, 215)'
        # stackgroup='one'  # define stack group
    ))
    fig.add_trace(go.Scatter(
        x=Country['dateymd'], y=Country['dailyrecovered'],
        hoverinfo='x+y',
        mode='lines',
        name="Daily Recovered",
        line=dict(color='green'),
        fill="tozeroy",
        fillcolor='rgb(152, 215, 187)'
        # stackgroup='one'
    ))
    fig.add_trace(go.Scatter(
        x=Country['dateymd'], y=Country['dailydeceased'],
        hoverinfo='x+y',
        mode='lines',
        name="Daily Deaths",
        line=dict(color='red'),
        fill="tozeroy",
        fillcolor='rgb(224, 123, 123)'
        # stackgroup='one'
    ))
    fig.update_layout(
        autosize=True,
        width=700,
        height=305,
        margin=dict(
            l=1,
            r=1,
            b=1,
            t=1,
            pad=1
        ),
        paper_bgcolor="white",
        plot_bgcolor='#DDE9F5',

        xaxis=dict(showline=False, showgrid=False),
        yaxis=dict(showline=False, showgrid=False)
    )
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )

    return fig


@app.callback([Output('line-chart', 'figure'),
               Output('content', 'children')],
              [Input('Store-Data', 'children'),
               Input('DailyCases', 'value')], [State('DailyCases', 'value')])
def left_panel(jsonified_cleaned_data, value, val):  # building the left panel of the dashboard
    try:
        datasets = json.loads(jsonified_cleaned_data)
        Country = pd.read_json(datasets['Country'], orient='split')
        state_wise = pd.read_json(datasets['state_wise'], orient='split')

        if value == 'cumulative':
            fig = cumulative(Country)
        else:
            fig = daily(Country)

        Table = generate_table(state_wise)
        return fig, Table
    except:
        time.sleep(5)
        datasets = json.loads(jsonified_cleaned_data)
        Country = pd.read_json(datasets['Country'], orient='split')
        state_wise = pd.read_json(datasets['state_wise'], orient='split')

        if value == 'cumulative':
            fig = cumulative(Country)
        else:
            fig = daily(Country)

        Table = generate_table(state_wise)
        return fig, Table


color_scale = {'active': 'Blues', 'recovered': 'greens', 'deaths': 'Reds'}


def map(state_wise, value):  # Function to build a Indian map Using plotly's CHOROPLETH

    fig = go.Figure(data=go.Choropleth(
        # geojson="https://kadatatlukishore.github.io/states_india.geojson",
        locations=state_wise['state'][1:-1],  # Spatial coordinates
        z=state_wise[value][1:-1],  # Data to be color-coded

        geojson=india_geojson,
        # set of locations match entries in `locations`
        locationmode='geojson-id',
        featureidkey='properties.st_nm',
        colorscale=color_scale[value],
    ))

    fig.update_geos(
        visible=False,
        projection=dict(
            type='conic conformal',
            parallels=[12.472944444, 35.172805555556]
        ),

        lonaxis={'range': [68, 98]},
        lataxis={'range': [6, 40]}
    )

    fig.update_layout(
        title=dict(
            text=f"COVID-19 {value} in India by State",
            xanchor='center',
            x=0.5,
            yref='paper',
            yanchor='bottom',
            y=1,
            pad={'b': 10}
        ),
        margin={'r': 0, 't': 0, 'l': 0, 'b': 0},
        height=720,
        width=720
    )
    fig.update_traces(showscale=True, colorbar=dict(len=0.5))
    return fig


@app.callback([Output('Indicator', 'figure'),
               Output('maps', 'figure')],
              [Input('Store-Data', 'children'),
               Input('cases', 'value')], [State('cases', 'value')])
def right_panel(jsonified_cleaned_data, value, val):  # building the left panel of the dashboard
    datasets = json.loads(jsonified_cleaned_data)
    Country = pd.read_json(datasets['Country'], orient='split')
    state_wise = pd.read_json(datasets['state_wise'], orient='split')
    LastUpdatedTime = state_wise['lastupdatedtime'][0]
    fig = make_subplots(rows=1, cols=3,
                        specs=[[{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}]])
    fig.add_trace(
        go.Indicator(
            value=state_wise['active'][0],
            mode="number+delta",
            delta={"reference": int(state_wise['active'][0] - state_wise['deltaconfirmed'][0]), "valueformat": ".0f"},
            title={'text': "Total Active cases"},
            delta_increasing_color='red',
            number_font_color='blue',
            number_valueformat="string"), row=1, col=1
    )
    fig.add_trace(go.Indicator(
        value=state_wise['recovered'][0],
        mode="number+delta",
        delta={"reference": int(state_wise['recovered'][0] - state_wise['deltarecovered'][0]), "valueformat": ".0f"},
        title={'text': "Total Recovered"},
        number_font_color='green'), row=1, col=2)
    fig.add_trace(go.Indicator(
        value=state_wise['deaths'][0],
        mode="number+delta",
        delta={"reference": int(state_wise['deaths'][0] - state_wise['deltadeaths'][0]),
               "valueformat": ".0f"},
        title={'text': "Total Deaths"},
        delta_increasing_color='black',
        number_font_color='red',
        number_valueformat="string"), row=1, col=3)
    fig.update_traces(number_font_size=30, title_font_size=15)
    fig.update_layout(height=350, width=700, title=f'Last Updated Time: {str(LastUpdatedTime)}')
    map_ = map(state_wise, value)   # calling function which gives us the choropleth map
    return fig, map_
