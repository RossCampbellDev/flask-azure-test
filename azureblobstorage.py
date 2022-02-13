import os,uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__

print("azure blob storage v: " + __version__) # test its imported

key = "CfoSroL5EhUF4UnSVSE5XbCD/0mi87Cwp+wh2F0W2dwVySf1SiWOWMAtA44Obf6s3T8zZeBiDrNcez4Azrzemw=="
acct_name = "flaskteststorage"
conn_string = "DefaultEndpointsProtocol=https;AccountName=flaskteststorage;AccountKey=CfoSroL5EhUF4UnSVSE5XbCD/0mi87Cwp+wh2F0W2dwVySf1SiWOWMAtA44Obf6s3T8zZeBiDrNcez4Azrzemw==;EndpointSuffix=core.windows.net"
# conn_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

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
