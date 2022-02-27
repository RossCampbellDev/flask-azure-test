from cidr import *
import pyshark
from packet_class import Pkt

pkt_data = []
capture_file = pyshark.FileCapture('big_test.pcap', only_summaries=True)
for p in capture_file:
    pkt_data.append(Pkt(p))

for p in pkt_data:
    print(p.src + " " + p.dst)