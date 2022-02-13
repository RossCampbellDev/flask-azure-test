class Pkt():
    def __init__(self, packet_in):
        self.num = packet_in.no
        self.src = packet_in.source
        self.dst = packet_in.destination
        self.time = packet_in.time
        self.proto = packet_in.protocol
        self.len = packet_in.length

    def get_as_json(self):
        return {
            "number":       self.num,
            "source":       self.src,
            "destination":  self.dst,
            "time":         self.time,
            "protocol":     self.proto,
            "length":       self.len
        }
        print