import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__

print("azure blob storage v: " + __version__)  # test it's imported

key = "DDLGr0r+lRnIYJv1YGRpWr0sS/IFg0avQzj6jX+FlqAtT62cESoUCjn99nOkXfmELZ8cH5u6UA1gKAdPXcLFXQ=="
acct_name = "flaskstorageaccount"
# this conn string was generated in Azure in the storage container settings.  it can be generated with code i think?
conn_string = "BlobEndpoint=https://flaskteststorage.blob.core.windows.net/;QueueEndpoint=https://flaskteststorage.queue.core.windows.net/;FileEndpoint=https://flaskteststorage.file.core.windows.net/;TableEndpoint=https://flaskteststorage.table.core.windows.net/;SharedAccessSignature=sv=2020-08-04&ss=bfqt&srt=sco&sp=rwdlacupitfx&se=2022-02-14T22:58:53Z&st=2022-02-14T14:58:53Z&spr=https,http&sig=wFIDyLUjnvMOI42O6jS3fq8juEVJ%2Bu8i5cvL1ahM4g8%3D"

try:
    blob_service_client = BlobServiceClient.from_connection_string(conn_string)  # create a client to interact with the blob service
    container_name = str(uuid.uuid4())  # create a uuid for a container
    # container_client = blob_service_client.create_container(container_name)  # creating new container
    local_file_name = "test.txt"

    container_client = blob_service_client.get_container_client('729c45f7-db98-4c12-ab37-ab59ece225a3')
    # blob_client = blob_service_client.get_blob_client(container_name, blob=local_file_name)

    # with open(local_file_name, "rb") as data:
    #     result = blob_client.upload_blob(data)

    blob_list = container_client.list_blobs()
    blobs = []
    for blob in blob_list:
        blobs.append(blob.name)
        print('\t' + blob.name)

    download_file_path = os.path.join('./', str.replace(local_file_name, '.txt', '.DOWNLOAD.txt'))
    with open(download_file_path, "wb") as download_file:
        download_file.write(container_client.download_blob(blobs[0]).readall())  # need to specify which blob to download... get the name from the list of blobs in the container client
except Exception as e:
    print(e)
