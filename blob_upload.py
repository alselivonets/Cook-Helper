from azure.storage.blob import BlobServiceClient

CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=dataset012021;AccountKey=PHl18JxjCkbzDWNohp20JnIqhvfUVShy360Jd7AjZH0Zwvfr0TZY8uc054IpUKscYIu0fbXbHXBfCNJ+HG3r7A==;EndpointSuffix=core.windows.net"

def upload_to_storage(data):

    try:
        blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
        
        blob_client = blob_service_client.get_blob_client(container="uploaded", blob=data)

        blob_client.upload_blob(data)
    except Exception as ex:

        print(ex.args)