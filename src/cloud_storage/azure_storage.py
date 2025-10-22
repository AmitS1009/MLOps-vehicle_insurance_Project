import os
import sys
import pickle
from io import StringIO
from typing import Union
from pandas import DataFrame, read_csv
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from src.logger import logging
from src.exception import MyException


class AzureBlobService:
    """
    A class for interacting with Azure Blob Storage, providing methods for file management,
    data uploads, and data retrieval in blob containers.
    """

    def __init__(self, connection_string: str = None):
        """
        Initializes the AzureBlobService instance with BlobServiceClient.

        Args:
            connection_string (str): Azure Storage connection string.
                                     If not provided, fetched from environment variable AZURE_STORAGE_CONNECTION_STRING.
        """
        try:
            if connection_string is None:
                connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING") or os.getenv("AZURE_CONNECTION_STRING")
                if not connection_string:
                    raise ValueError("Azure connection string not found in environment variables.")
            self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)
            logging.info("Connected to Azure Blob Storage successfully.")
        except Exception as e:
            raise MyException(e, sys) from e

    def container_exists(self, container_name: str) -> bool:
        """
        Check if a container exists.

        Args:
            container_name (str): Name of the container.

        Returns:
            bool: True if the container exists, False otherwise.
        """
        try:
            container_client = self.blob_service_client.get_container_client(container_name)
            return container_client.exists()
        except Exception as e:
            raise MyException(e, sys) from e

    def blob_exists(self, container_name: str, blob_name: str) -> bool:
        """
        Check if a blob exists in a container.

        Args:
            container_name (str): Name of the container.
            blob_name (str): Name of the blob.

        Returns:
            bool: True if blob exists, False otherwise.
        """
        try:
            blob_client = self.blob_service_client.get_blob_client(container_name, blob_name)
            return blob_client.exists()
        except Exception as e:
            raise MyException(e, sys) from e

    def create_container(self, container_name: str) -> None:
        """
        Create a new container if it doesn't exist.

        Args:
            container_name (str): Name of the container.
        """
        try:
            container_client = self.blob_service_client.get_container_client(container_name)
            if not container_client.exists():
                self.blob_service_client.create_container(container_name)
                logging.info(f"Created container: {container_name}")
        except Exception as e:
            raise MyException(e, sys) from e

    @staticmethod
    def _read_blob_data(blob_client: BlobClient, decode: bool = True, make_readable: bool = False) -> Union[StringIO, str, bytes]:
        """
        Read blob content with optional decoding.

        Args:
            blob_client (BlobClient): Blob client instance.
            decode (bool): Whether to decode bytes to string.
            make_readable (bool): Whether to return as StringIO for DataFrame.

        Returns:
            Union[StringIO, str, bytes]: Blob content.
        """
        try:
            data = blob_client.download_blob().readall()
            if decode:
                data = data.decode()
            if make_readable:
                data = StringIO(data)
            return data
        except Exception as e:
            raise MyException(e, sys) from e

    def upload_file(self, local_path: str = None, from_file: str = None, container_name: str = None, blob_name: str = None, remove: bool = True) -> None:
        """
        Uploads a file to Azure Blob Storage.

        Args:
            local_path (str): Local file path.
            from_file (str): Alternative to local_path for compatibility.
            container_name (str): Target container name.
            blob_name (str): Target blob name.
            remove (bool): Delete local file after upload.
        """
        try:
            # Use from_file if provided (for backward compatibility)
            if from_file is not None:
                local_path = from_file

            logging.info(f"Uploading file {local_path} to {container_name}/{blob_name}")
            blob_client = self.blob_service_client.get_blob_client(container_name, blob_name)
            with open(local_path, "rb") as data:
                blob_client.upload_blob(data, overwrite=True)
            logging.info(f"Uploaded {local_path} successfully to {blob_name}")

            if remove:
                os.remove(local_path)
                logging.info(f"Removed local file {local_path}")
        except Exception as e:
            raise MyException(e, sys) from e


    def download_blob(self, container_name: str, blob_name: str, download_path: str) -> None:
        """
        Download a blob from a container.

        Args:
            container_name (str): Name of the container.
            blob_name (str): Name of the blob.
            download_path (str): Local path to save the blob.
        """
        try:
            blob_client = self.blob_service_client.get_blob_client(container_name, blob_name)
            with open(download_path, "wb") as f:
                blob_data = blob_client.download_blob()
                f.write(blob_data.readall())
            logging.info(f"Blob {blob_name} downloaded successfully to {download_path}")
        except Exception as e:
            raise MyException(e, sys) from e

    def upload_dataframe_as_csv(self, df: DataFrame, container_name: str, blob_name: str, local_temp: str = "temp.csv") -> None:
        """
        Uploads a DataFrame as a CSV blob.

        Args:
            df (DataFrame): DataFrame to upload.
            container_name (str): Target container.
            blob_name (str): Blob name.
            local_temp (str): Temporary local filename.
        """
        try:
            df.to_csv(local_temp, index=False)
            self.upload_file(local_temp, container_name, blob_name)
            logging.info(f"DataFrame uploaded as CSV to {container_name}/{blob_name}")
        except Exception as e:
            raise MyException(e, sys) from e

    def read_csv(self, container_name: str, blob_name: str) -> DataFrame:
        """
        Reads a CSV blob and returns it as a DataFrame.

        Args:
            container_name (str): Container name.
            blob_name (str): Blob name.

        Returns:
            DataFrame: DataFrame from CSV.
        """
        try:
            blob_client = self.blob_service_client.get_blob_client(container_name, blob_name)
            content = self._read_blob_data(blob_client, decode=True, make_readable=True)
            df = read_csv(content)
            logging.info(f"CSV {blob_name} read successfully from {container_name}")
            return df
        except Exception as e:
            raise MyException(e, sys) from e

    def upload_model(self, model_object: object, container_name: str, blob_name: str) -> None:
        """
        Uploads a pickled model to Azure Blob Storage.

        Args:
            model_object (object): Trained model to upload.
            container_name (str): Container name.
            blob_name (str): Blob name.
        """
        try:
            blob_client = self.blob_service_client.get_blob_client(container_name, blob_name)
            serialized_model = pickle.dumps(model_object)
            blob_client.upload_blob(serialized_model, overwrite=True)
            logging.info(f"Model uploaded successfully to {container_name}/{blob_name}")
        except Exception as e:
            raise MyException(e, sys) from e

    def load_model(self, container_name: str, blob_name: str) -> object:
        """
        Downloads and loads a pickled model from Azure Blob Storage.

        Args:
            container_name (str): Container name.
            blob_name (str): Blob name.

        Returns:
            object: Deserialized model.
        """
        try:
            blob_client = self.blob_service_client.get_blob_client(container_name, blob_name)
            blob_data = blob_client.download_blob().readall()
            model = pickle.loads(blob_data)
            logging.info(f"Model loaded successfully from {container_name}/{blob_name}")
            return model
        except Exception as e:
            raise MyException(e, sys) from e
