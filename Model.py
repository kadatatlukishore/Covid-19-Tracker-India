import dash_html_components as html

import plotly.graph_objects as go
import pandas as pd
from datetime import date, timedelta, datetime
import numpy as np

import dash_table
from pmdarima import auto_arima
import warnings

warnings.filterwarnings('ignore')


def table(new):
    return html.Div([
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in new.columns],
            data=new.to_dict('records'),
            style_table={'height': '80px', 'overflowY': 'auto', 'overflowX': 'auto',
                         'minWidth': '100%'},
            style_cell={'overflow': 'hidden',
                        'textOverflow': 'ellipsis',
                        'fontSize': 15, 'font-family': 'sans-serif',
                        'minWidth': '80px', 'width': '150px', 'maxWidth': '120px'
                        },
            fixed_rows={'headers': True},
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold'
            }
        )
    ])


def mean_absolute_percentage_error(y_true, y_pred):  # to calculate the "error"
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100


def auto_arima_model(df):  # training and predicting values("Cases&Deaths")
    train, test = df[-32:-2], df[-2:]
    test_index = test.index
    # trained only last month's data
    model = auto_arima(train, start_p=1, start_q=1,
                       max_p=3, max_q=3, stepwise=False,
                       random=True, trace=False, error_action='ignore',
                       suppress_warnings=True)

    result = model.fit(train)
    test_predict = pd.DataFrame(result.predict(n_periods=2), index=test_index,
                                columns=['Prediction cases'])
    evaluation_metrics = mean_absolute_percentage_error(test_predict, test)
    evaluation_metrics = float("{:.2f}".format(evaluation_metrics))
    index = pd.date_range(date.today(), periods=5)  # to get the dates for the next 5 Days including Today
    index.strftime('%Y-%m-%d')
    prediction = pd.DataFrame(result.predict(n_periods=7)[2:], index=index,
                              columns=['Prediction_cases'])
    prediction['Prediction_cases'] = prediction['Prediction_cases'].astype(int)

    return prediction, evaluation_metrics


def model_and_graphs(data, value):
    colors = {'dailyconfirmed': 'red', 'dailydeceased': 'black'}
    Title = {'dailyconfirmed': 'Prediction of Cases for the next 5 days',
             'dailydeceased': 'Prediction of Deaths for the next 5 days'}
    df = data[['dateymd', value]]
    df.set_index('dateymd', inplace=True)
    predict, metrics = auto_arima_model(df)
    fig = go.Figure(
        go.Scatter(x=predict.index, y=predict['Prediction_cases'],
                   line=dict(color=colors[value]), name='Cases&Deaths', mode='lines+markers',
                   marker=dict(size=5, color='black'))
    )
    fig.update_layout(
        autosize=False,
        width=1480,
        height=500,
        title=Title[value],
        paper_bgcolor="white",
        plot_bgcolor='#DDE9F5',
        xaxis=dict(showline=False, showgrid=False),
        yaxis=dict(showline=False, showgrid=False)
    )

    Metrics = {"Mean Absolute Percentage Error": metrics}
    Metrics = table(pd.DataFrame(Metrics.items(), columns=['Metric', 'Value']))  # create a dash table for the metrics

    return fig, Metrics


