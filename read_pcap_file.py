# use pyshark to open a capture file and then generate Pkt objects for further use
from packet_class import Pkt
from dash_pandas_data import *
from dash.dependencies import Input, Output, State
from dash import dash_table, dcc, html
import pyshark
from cidr import cidr_check
from collections import Counter


def read_capture(pcap_file):
    all_pkts = []
    all_pkts_json = []
    capture_file = pyshark.FileCapture(pcap_file, only_summaries=True)
    for p in capture_file:
        p_tmp = Pkt(p)
        all_pkts.append(p_tmp)
        all_pkts_json.append(p_tmp.get_as_json())
    capture_file.close()
    return all_pkts, all_pkts_json


# TESTING ==============================================================================================================
all_pkts, all_pkts_json = read_capture('big_test.pcap')
dataset = get_df_from_json(all_pkts_json)  # all_pkts[1])
dataset.set_index('number', inplace=False, drop=False)

app.title = 'PCAP Analysis Test'
app.layout = html.Div([
    html.H1(id='t1', children='pcap breakdown'),
    html.Div([
        dash_table.DataTable(
            id='datatable-interactivity',
            columns=[                                   # establish column headers and interactivity
                {"name": c, "id": c, "deletable": True, "selectable": True, "hideable": True}
                for c in dataset.columns
            ],
            data=dataset.to_dict('records'),            # set our data source
            editable=True,                              # edit text in cell
            filter_action="native",                     # filter data by user.  can be native or none.  user can type a filter in
            sort_action="native",                       # native or none again.  sort by column
            sort_mode="single",                         # single or multi (columns)
            column_selectable="multi",                  # user can sellect multiple or 'single' columns
            row_selectable="multi",
            row_deletable=True,
            selected_columns=[],                        # IDs of columns that user selects
            selected_rows=[],
            page_action="native",                       # data passed to the table up front or not ('none')
            page_current=0,                             # start on page 0 obviously
            page_size=10,
            style_cell={
                'minWidth': 90, 'maxWidth': 100, 'width': 90
            },
            style_cell_conditional=[
                {
                    'if': {'column_id': c},
                    'textAlign': 'left'
                } for c in ['source','destination']
            ],
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto'
            }
        )
    ]),
    html.Br(),
    html.Div(id="chaintest", className="charts", children="this div demonstrates chaining of callbacks.  whatever shows here will trigger the callback on the radio buttons"),
    html.Br(),
    dcc.Dropdown(id='column_select', options=["number", "source", "destination", "time", "protocol", "length"], value='source'),
    html.Button(id='button1', n_clicks=0, children='show chart'),  # n_clicks counts number of clicks... its a property
    html.Div(id='chart', className="charts", style={'padding-bottom': '30px;'}),  # render the bar charts,
    html.Br(),
    dcc.RadioItems(id='radio2', value="ip analysis", options=['source', 'destination']),
    html.Div(id='ioc', className="charts", style={}, children=[])
])
# dcc.Graph(id='graph-output', figure={})
# html.Div(id='chart2', className="charts"),


@app.callback(
    Output('chaintest', 'children'),
    Input('datatable-interactivity', 'active_cell'),
    prevent_initial_call=True
)
def tbl_cell(selected_cell):
    x=selected_cell["row"]
    y=selected_cell["column"]
    print(dataset.iloc[x, y])  # data in selected cell

    return dataset.columns[y]


@app.callback(
    Output('radio2', 'value'),
    Input('chaintest', 'children'),
    prevent_initial_call=True
)
def chaintest(col):
    print("col %s" % col)
    return col  # dcc.RadioItems(id='radio2', options=['source', 'destination'], value=col)



@app.callback(
    [Output(component_id='ioc', component_property='children'),
     Input(component_id='radio2', component_property='value')],
    prevent_initial_call=True  # stops it calling the callback on page load
)
def ip_analysis(value):
    count = Counter(p[value] for p in all_pkts_json if p.get(value))
    # print("%s - %d" % (src, n) for src, n in count.most_common(5))
    tbl = html.Table(
        [html.Tr([html.Th(value), html.Th('count')])] +
        [html.Tr([
            html.Td(src),
            html.Td(n)
        ]) for src, n in count.most_common(5)]
    )
    # for src, n in count.most_common(5):
    #     # result += "%s\t%d" % (src, n)
    #     para = html.P(children="%s - %d" % (src, n))
    #     result.append(para)
    # print(type(result))
    # return [html.P(id='p1', children=result)]
    return [tbl]


# State(component_id='radio1', component_property='value')],  # states do not trigger the callback function, so we can change the dropdown but nothing happens until we click the button
# Output(component_id='t1', component_property='style')],  # component_property says which part to update.  if its a dcc.Graph then the component will be 'figure'
@app.callback(
    [Output(component_id='chart', component_property='children'),
     Output(component_id='t1', component_property='children')],
    [State(component_id='column_select', component_property='value')],
    [Input(component_id='button1', component_property='n_clicks')],
    prevent_initial_call=True  # stops it calling the callback on page load
)
def change_graph(value_column, n):
    df = dataset[value_column]
    df = dataset
    print(dataset[value_column].value_counts())

    # return dash.no_update, dash.no_update, None # this is how we would avoid it doing anything, for whatever reasons

    if value_column in ["sour1ce", "destination"]:
        graph = dcc.Graph(id='chart_bar', figure=px.bar(data_frame=df, x=value_column, template='presentation'))  # names=value_column, values=value_column))
    elif value_column in ["protocol", "source", "length"]:
        graph = dcc.Graph(id='chart_pie', figure=px.pie(data_frame=df, names=dataset[value_column].unique(), values=dataset[value_column].value_counts(), template='presentation'))  # .value_counts(ascending=True)
    else:
        return dash.no_update, dash.no_update

    title = value_column

    #title = radio
    # return dash.no_update, title  # this lets us do nothing with 1 of the outputs, if we so choose
    return graph, title  # , {"background-color": radio}  # return each of the defined Outputs


app.run_server(debug=True)
