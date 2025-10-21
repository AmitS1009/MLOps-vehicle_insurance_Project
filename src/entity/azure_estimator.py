from src.cloud_storage.azure_storage import AzureBlobService
from src.exception import MyException
from src.entity.estimator import MyModel
import sys
from pandas import DataFrame


class Proj1AzureEstimator:
    """
    This class is used to save and retrieve the model from Azure Blob Storage and perform predictions.
    """

    def __init__(self, container_name, blob_path, model_name="model.pkl"):
        """
        :param container_name: Name of your Azure Blob container
        :param blob_path: Path of your model blob inside the container
        :param model_name: Name of model file to save in Azure
        """
        self.container_name = container_name
        self.azure_storage = AzureBlobService()
        self.blob_path = blob_path
        self.model_name = model_name
        self.loaded_model: MyModel = None

    def is_model_present(self, blob_path):
        try:
            return self.azure_storage.blob_exists(container_name=self.container_name, blob_name=blob_path)
        except MyException as e:
            print(e)
            return False

    def load_model(self) -> MyModel:
        """
        Load the model from Azure Blob Storage.
        :return: Loaded model
        """
        try:
            return self.azure_storage.load_model(
                blob_name=self.blob_path,
                container_name=self.container_name
            )
        except Exception as e:
            raise MyException(e, sys)

    def save_model(self, from_file, to_file=None, remove=False):
        """
        Save trained model to Azure Blob Storage.
        """
        try:
            self.azure_storage.upload_file(
                local_path=from_file,             # ✅ correct argument name
                container_name=self.container_name,
                blob_name=self.model_name,
                remove=remove
            )

        except Exception as e:
            raise MyException(e, sys)

    def predict(self, dataframe: DataFrame):
        """
        Perform prediction using the loaded model.
        :param dataframe: Input DataFrame
        :return: Prediction results
        """
        try:
            if self.loaded_model is None:
                self.loaded_model = self.load_model()
            return self.loaded_model.predict(dataframe=dataframe)
        except Exception as e:
            raise MyException(e, sys)
