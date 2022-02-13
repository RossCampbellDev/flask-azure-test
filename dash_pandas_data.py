import dash
from dash.dependencies import Input, Output
from dash import dash_table, dcc, html
import plotly.express as px
import pandas as pd

def get_df_from_json(json_data):
    # df = pd.Series(json_data) # df is shorthand for Data Frame
    df = pd.DataFrame(json_data)
    df.columns = ['num','src','dst','time','proto','len']
    df.to_json(orient='table')
    return df

def create_pie(data):
    fig_bar = px.bar(data_frame=data, x='proto')
    # fig_bar.show()
