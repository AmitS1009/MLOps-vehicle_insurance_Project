from src.configuration.azure_connection import AzureClient

azure_client = AzureClient()
blob_service_client = azure_client.blob_service_client

# Now you can use it with your AzureBlobService class
container_client = blob_service_client.get_container_client("my-container")
print("Connected to container:", container_client.container_name)
