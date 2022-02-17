# use pyshark to open a capture file and then generate Pkt objects for further use
from packet_class import Pkt
from dash_pandas_data import *
from dash.dependencies import Input, Output, State
from dash import dash_table, dcc, html
import pyshark


def read_capture(pcap_file):
    all_pkts = []
    all_pkts_json = []
    capture_file = pyshark.FileCapture(pcap_file, only_summaries=True)
    for p in capture_file:
        all_pkts.append(Pkt(p))
        all_pkts_json.append(Pkt(p).get_as_json())
    capture_file.close()
    return all_pkts, all_pkts_json


# TESTING ==============================================================================================================
all_pkts = read_capture('test.pcap')
dataset = get_df_from_json2(all_pkts[1])
# create_graph(dataset, 'protocol')
# create_pie(dataset, 'protocol')


app.layout = html.Div([
    html.H1(id='t1', children='pcap breakdown'),
    dcc.Dropdown(id='column_select',
                 options=[{'label': x, 'value': x} for x in sorted(dataset.columns.unique())],
                 value='source'
                 ),
    html.Button(id='button1', n_clicks=0, children='show chart'),  # n_clicks counts number of clicks... its a property
    dcc.RadioItems(id='radio1', value="test1", options=['hotpink', 'green']),
    html.Div(id='chart', className="charts", style={}),  # render the bar charts
    html.Div(id='chart2', className="charts"),
    dcc.Graph(id='graph-output', figure={})
])


@app.callback(
    [Output(component_id='chart2', component_property='children'),
     Output(component_id='t1', component_property='children'),
     Output(component_id='t1', component_property='style')],  # component_property says which part to update.  if its a dcc.Graph then the component will be 'figure'
    [State(component_id='column_select', component_property='value'),
     State(component_id='radio1', component_property='value')],  # states do not trigger the callback function, so we can change the dropdown but nothing happens until we click the button
    [Input(component_id='button1', component_property='n_clicks')],
    prevent_initial_call=True  # stops it calling the callback on page load
)
def change_graph(value_column, radio, n):
    print(n)
    df = dataset[value_column]
    print(df)

    if 1 == 2:  # this is how we would avoid it doing anything, for whatever reasons
        return dash.no_update, dash.no_update, null

    if value_column == "source":
        graph = dcc.Graph(id='chart_bar', figure=px.bar(data_frame=df, x=value_column))  # names=value_column, values=value_column))
    else:
        graph = dcc.Graph(id='chart_pie', figure=px.pie(data_frame=df, names=value_column, values=value_column))

    title = radio
    # return dash.no_update, title  # this lets us do nothing with 1 of the outputs, if we so choose
    return graph, title, {"background-color": radio}  # return each of the defined Outputs


app.run_server(debug=True)
