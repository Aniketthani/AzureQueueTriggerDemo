import logging
import azure.functions as func

from ..utils import storage_helpers
from ..utils import processing
import os


def main(msg: func.QueueMessage) -> None:
    
    file_name = ""

    try:

        file_name = msg.get_body().decode('utf-8')
        logging.info(f"Processing queue item: {file_name}...")

        # Getting settings
        STORAGE_CONNECTION_STRING = os.getenv("QueueConnectionString")
        CONTAINER_NAME =os.getenv("STORAGE_CONTAINER_NAME")

        # Getting file from storage
        file_path = storage_helpers.download_blob(CONTAINER_NAME, file_name, STORAGE_CONNECTION_STRING)

        if file_path != None:
            # Processing file
            processed_doc = processing.process_doc(file_path)
            # Saving processed file to storage
            if processed_doc != None:
                new_file_name = 'processed_' + file_name
                storage_helpers.upload_blob(CONTAINER_NAME, new_file_name, processed_doc, STORAGE_CONNECTION_STRING)
                # Deleting local copy
                os.remove(file_path)
                logging.info(f"Done processing {file_name}.")
        
        else:
            logging.info(f"Did not perform any operation as there was an issue.")

    except Exception as e:
        logging.error(f"Error getting file name from msg: {e}")