# use pyshark to open a capture file and then generate Pkt objects for further use
from packet_class import Pkt
from dash_pandas_data import *
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


# testing
all_pkts = read_capture('test.pcap')
dataset = get_df_from_json2(all_pkts[1])
# create_graph(dataset, 'protocol')
# create_pie(dataset, 'protocol')

# testing interactive graphing
# dash documentation for how to create the page layout

app.layout = html.Div([
    html.H1('pcap breakdown'),
    dcc.Dropdown(id='column_select',
                 options=[{'label': x, 'value': x} for x in sorted(dataset.columns.unique())],
                 value='source'
                 ),
    dcc.Graph(id='bar_chart', figure=px.bar(data_frame=dataset, x='source'))
])

# input changes based on the dropdown, output changes the graph
@app.callback(
    Output(component_id='bar_chart', component_property='figure'),
    Input(component_id='column_select', component_property='value')
)
def interactive_graphing(value_column):
    print(value_column)
    df = dataset[dataset[value_column]]
    return px.bar(data_frame=df, x=value_column)

app.run_server()
