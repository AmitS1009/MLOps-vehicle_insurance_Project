import sys
from src.cloud_storage.azure_storage import AzureBlobService
from src.exception import MyException
from src.logger import logging
from src.entity.artifact_entity import ModelPusherArtifact, ModelEvaluationArtifact
from src.entity.config_entity import ModelPusherConfig
from src.entity.azure_estimator import Proj1AzureEstimator


class ModelPusher:
    """
    Pushes the trained model to Azure Blob Storage (production location).
    """

    def __init__(self, model_evaluation_artifact: ModelEvaluationArtifact,
                 model_pusher_config: ModelPusherConfig):
        """
        :param model_evaluation_artifact: Output reference from model evaluation stage.
        :param model_pusher_config: Configuration for model pushing.
        """
        self.azure_storage = AzureBlobService()
        self.model_evaluation_artifact = model_evaluation_artifact
        self.model_pusher_config = model_pusher_config
        self.proj1_estimator = Proj1AzureEstimator(
            container_name=model_pusher_config.container_name,
            blob_path=model_pusher_config.azure_model_blob_path
        )

    def initiate_model_pusher(self) -> ModelPusherArtifact:
        """
        Uploads the newly trained model to Azure Blob Storage.
        Returns a ModelPusherArtifact with blob info.
        """
        logging.info("Entered initiate_model_pusher method of ModelPusher class")

        try:
            print("--------------------------------------------------------------------------------")
            logging.info("Uploading trained model to Azure Blob Storage...")

            # Upload the model to Azure Blob
            self.proj1_estimator.save_model(
                from_file=self.model_evaluation_artifact.trained_model_path
            )

            # Create model pusher artifact
            model_pusher_artifact = ModelPusherArtifact(
                bucket_name=self.model_pusher_config.container_name,
                azure_model_path=self.model_pusher_config.azure_model_blob_path
            )

            logging.info("Model successfully uploaded to Azure Blob Storage.")
            logging.info(f"Model pusher artifact: [{model_pusher_artifact}]")
            logging.info("Exited initiate_model_pusher method of ModelPusher class")

            return model_pusher_artifact

        except Exception as e:
            raise MyException(e, sys) from e
