import json
from azure_blob_storage import *

with open('env.json', 'r') as f:
    config = json.loads(f.read())['config']

handler = AzureBlobStorageHandler(config['account'], config['key'], config['conn_string'])
handler.create_blob_service()
handler.select_container('testcontainer')
handler.write_file('test.txt')
handler.read_file('test.txt')