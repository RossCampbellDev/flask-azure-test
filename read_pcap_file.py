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


# TESTING ==============================================================================================================
all_pkts = read_capture('test.pcap')
dataset = get_df_from_json2(all_pkts[1])
# create_graph(dataset, 'protocol')
# create_pie(dataset, 'protocol')

app.layout = html.Div([
    html.H1('pcap breakdown'),
    dcc.Dropdown(id='column_select',
                 options=[{'label': x, 'value': x} for x in sorted(dataset.columns.unique())],
                 value='source'
                 ),
    html.Div(id='chart', className="charts"),  # render the bar charts
    html.Div(id='chart2', className="charts")
])


@app.callback(
    Output(component_id='chart', component_property='children'),
    Input(component_id='column_select', component_property='value')
)
def change_graph(value_column):
    df = dataset[value_column]
    return dcc.Graph(id='bar_chart', figure=px.bar(data_frame=df, x=value_column))


@app.callback(
    Output(component_id='chart2', component_property='children'),
    Input(component_id='chart', component_property='selected_cells')
)
def select_ip(ip):
    print(ip)
    return html.Div()

app.run_server(debug=True)
