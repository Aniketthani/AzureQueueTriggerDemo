import logging
import os
from azure.storage.blob import BlobServiceClient

# Creates a blob service client
def create_blob_service_client(connection_string):
    blob_service_client = None
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        logging.info("Created blob service client.")
    except Exception as e:
        logging.error(f"Could not create blob service client: {e}")
    return blob_service_client

# Downloads the specified blob
def download_blob(container_name, blob_name, connection_string):
    blob_service_client = create_blob_service_client(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    try:
        if blob_client.exists():
            downloads_folder = "tmp_files"
            local_path = downloads_folder + '/' + blob_name
            if not os.path.exists(downloads_folder):
                os.makedirs(downloads_folder)
            with open(local_path, "wb") as f:
                stream = blob_client.download_blob()
                f.write(stream.readall())
            return local_path
        else:
            logging.error(f"Blob {blob_name} doesn't exist.")
    except Exception as e:
        logging.error(f"The blob {blob_name} was not found. error : {e}")
    return None


# Creates a blob in blob storage from bytes
def upload_blob(container_name, blob_name, data, connection_string):
    blob_service_client = create_blob_service_client(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    try:
        blob_client.upload_blob(data=data)
        logging.info(f"Created blob {blob_name} successfully.")
        return True
    except Exception:
        try:
            blob_client.delete_blob()
            blob_client.upload_blob(data=data)
            logging.warning(f"Blob {blob_name} already exists, deleted it.")
            logging.info(f"Created blob {blob_name} successfully.")
            return True
        except Exception as e:
            logging.error(f"Error creating blob {blob_name}: {e}")
    return False