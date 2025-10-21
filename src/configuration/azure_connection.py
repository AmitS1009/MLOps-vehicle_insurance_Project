import os
from azure.storage.blob import BlobServiceClient
from src.constants import AZURE_STORAGE_CONNECTION_STRING_ENV_KEY


class AzureClient:
    """
    This class establishes a connection to Azure Blob Storage using
    the connection string stored in environment variables.
    """

    blob_service_client = None

    def __init__(self):
        """
        Initializes the Azure Blob Service connection using the
        connection string from environment variables.
        Raises an exception if the environment variable is not set.
        """
        if AzureClient.blob_service_client is None:
            connection_string = os.getenv(AZURE_STORAGE_CONNECTION_STRING_ENV_KEY)

            if connection_string is None:
                raise Exception(
                    f"Environment variable '{AZURE_STORAGE_CONNECTION_STRING_ENV_KEY}' is not set."
                )

            AzureClient.blob_service_client = BlobServiceClient.from_connection_string(
                connection_string
            )

        self.blob_service_client = AzureClient.blob_service_client
