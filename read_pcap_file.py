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
dataset = get_df_from_json(all_pkts[1])

# create_pie(dataset)

# for p in dataset:
#   print("%s - %s" % (p.num, p.src))

# tbl = build_table(dataset)