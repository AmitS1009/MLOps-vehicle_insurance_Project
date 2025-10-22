from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    trained_file_path: str
    test_file_path: str

    

class DataValidationArtifact:
    def __init__(self, validation_status: bool, message: str, validation_report_file_path: str):
        self.validation_status = validation_status
        self.message = message
        self.validation_report_file_path = validation_report_file_path

    def __repr__(self):
        return f"DataValidationArtifact(validation_status={self.validation_status}, message={self.message}, validation_report_file_path={self.validation_report_file_path})"


@dataclass
class DataTransformationArtifact:
    transformed_object_file_path:str 
    transformed_train_file_path:str
    transformed_test_file_path:str


@dataclass
class ClassificationMetricArtifact:
    f1_score:float
    precision_score:float
    recall_score:float


    
@dataclass
class ModelTrainerArtifact:
    trained_model_file_path:str 
    metric_artifact:ClassificationMetricArtifact


@dataclass
class ModelEvaluationArtifact:
    is_model_accepted:bool
    changed_accuracy:float
    azure_model_path:str 
    trained_model_path:str

@dataclass
class ModelPusherArtifact:
    bucket_name:str
    azure_model_path:str


