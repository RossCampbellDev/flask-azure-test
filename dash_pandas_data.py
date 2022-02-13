import dash
from dash.dependencies import Input, Output
from dash import dash_table, dcc, html
import plotly.express as px
import pandas as pd

from dash.dependencies import Output, Input

app = dash.Dash(__name__)  # flask
global dataset1

def get_df_from_json(json_data):
    # df = pd.Series(json_data) # df is shorthand for Data Frame
    df = pd.DataFrame(json_data)
    df.columns = ['num','src','dst','time','proto','len']
    df.to_json(orient='table')
    return df


def get_df_from_json2(json_data):
    return pd.read_json('pcapjson.json')


def create_graph(data, col):
    fig_bar = px.bar(data_frame=data, x=col)
    return fig_bar


def create_pie(data, col):
    fig_pie = px.pie(data_frame=data, names=col, values=col)
    fig_pie.show()

