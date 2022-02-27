import ipaddress

def cidr_convert(cidr):
    cidr = int(cidr)
    mask = (0xffffffff >> (32 - cidr)) << (32 - cidr)
    return (str((0xff000000 & mask) >> 24) + '.' +
          str((0x00ff0000 & mask) >> 16) + '.' +
          str((0x0000ff00 & mask) >> 8) + '.' +
          str((0x000000ff & mask)))


# check if an IP is valid against the subnet mask
def cidr_check(IP, mask):
    return ipaddress.ip_address(IP) in ipaddress.ip_network(mask)

# print(cidr_check('192.168.0.0', '192.168.0.0/16'))
# print(cidr_check('192.168.255.255', '192.168.0.0/16'))
