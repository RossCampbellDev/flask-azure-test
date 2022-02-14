import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient


class AzureBlobStorageHandler():
    def __init__(self, account_name, key, connection_string):
        self.account_name = account_name
        self.key = key
        self.conn_string = connection_string
        self.container_name = None
        self.container_client = None
        self.blob_service_client = None

    def create_blob_service(self):
        self.blob_service_client = BlobServiceClient.from_connection_string(self.conn_string)

    # creates new if it doesn't exist
    def select_container(self, name):
        self.container_name = name
        self.container_client = self.blob_service_client.get_container_client(self.container_name)

    def write_file(self, filename):
        blob_client = self.blob_service_client.get_blob_client(self.container_name, blob=filename)
        with open(filename, "rb") as data:
            result = blob_client.upload_blob(data)

    def read_file(self, filename):
        blob_list = self.container_client.list_blobs()
        for blob in blob_list:
            if filename == blob.name:
                print("%s found, making a copy..." % filename)
                download_file_path = os.path.join('./', str.replace(filename, filename[-4], 'DOWNLOAD.' + filename))
                with open(download_file_path, "wb") as download_file:
                    download_file.write(self.container_client.download_blob(blob).readall())  # need to specify which blob to download... get the name from the list of blobs in the container client


a = "flaskstorageaccount"
k = "DDLGr0r+lRnIYJv1YGRpWr0sS/IFg0avQzj6jX+FlqAtT62cESoUCjn99nOkXfmELZ8cH5u6UA1gKAdPXcLFXQ=="
# this conn string was generated in Azure in the storage container settings.  it can be generated with code i think?
c = "BlobEndpoint=https://flaskteststorage.blob.core.windows.net/;QueueEndpoint=https://flaskteststorage.queue.core.windows.net/;FileEndpoint=https://flaskteststorage.file.core.windows.net/;TableEndpoint=https://flaskteststorage.table.core.windows.net/;SharedAccessSignature=sv=2020-08-04&ss=bfqt&srt=sco&sp=rwdlacupitfx&se=2022-02-14T22:58:53Z&st=2022-02-14T14:58:53Z&spr=https,http&sig=wFIDyLUjnvMOI42O6jS3fq8juEVJ%2Bu8i5cvL1ahM4g8%3D"
c_n = '729c45f7-db98-4c12-ab37-ab59ece225a3'

handler = AzureBlobStorageHandler(a, k, c)
handler.select_container('testcontainer')
handler.create_blob_service()
handler.write_file('test.txt')
handler.read_file('test.txt')

