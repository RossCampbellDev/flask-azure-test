import os,uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__

print("azure blob storage v: " + __version__) # test its imported

# server 1
# key = "CfoSroL5EhUF4UnSVSE5XbCD/0mi87Cwp+wh2F0W2dwVySf1SiWOWMAtA44Obf6s3T8zZeBiDrNcez4Azrzemw=="
# conn_string = "DefaultEndpointsProtocol=https;AccountName=flaskteststorage;AccountKey=CfoSroL5EhUF4UnSVSE5XbCD/0mi87Cwp+wh2F0W2dwVySf1SiWOWMAtA44Obf6s3T8zZeBiDrNcez4Azrzemw==;EndpointSuffix=core.windows.net"
# acct_name = "flaskteststorage"

# server 2
key = "DDLGr0r+lRnIYJv1YGRpWr0sS/IFg0avQzj6jX+FlqAtT62cESoUCjn99nOkXfmELZ8cH5u6UA1gKAdPXcLFXQ=="
acct_name = "flaskstorageaccount"
# conn_string = "DefaultEndpointsProtocol=https;AccountName=flaskstorageaccount;AccountKey=DDLGr0r+lRnIYJv1YGRpWr0sS/IFg0avQzj6jX+FlqAtT62cESoUCjn99nOkXfmELZ8cH5u6UA1gKAdPXcLFXQ==;EndpointSuffix=core.windows.net"
conn_string = "BlobEndpoint=https://flaskteststorage.blob.core.windows.net/;QueueEndpoint=https://flaskteststorage.queue.core.windows.net/;FileEndpoint=https://flaskteststorage.file.core.windows.net/;TableEndpoint=https://flaskteststorage.table.core.windows.net/;SharedAccessSignature=sv=2020-08-04&ss=bfqt&srt=sco&sp=rwdlacupitfx&se=2022-02-14T22:58:53Z&st=2022-02-14T14:58:53Z&spr=https,http&sig=wFIDyLUjnvMOI42O6jS3fq8juEVJ%2Bu8i5cvL1ahM4g8%3D"

try:
    blob_service_client = BlobServiceClient.from_connection_string(conn_string)  # create a client to interact with the blob service
    container_name = str(uuid.uuid4())  # create a uuid for a container
    container_client = blob_service_client.create_container(container_name)

    local_file_name = "./test.txt"

    blob_client = blob_service_client.get_blob_client(container_name, blob=local_file_name)
    with open(local_file_name, "rb") as data:
        blob_client.upload_blob(data)
except Exception as e:
    print(e)
