## This store the output of componetent file

from dataclasses import dataclass
## act as decoretor and create variable for empty class

##for data Ingestion componenents output
@dataclass
class DataIngestionArtifacts:
    train_file_path:str
    test_file_path:str


##for data validation componenets output
@dataclass
class DataValidationArtifact:
    validation_status:bool
    valid_train_file_path:str
    valid_test_file_path:str
    invalid_train_file_path:str
    invalid_test_file_path:str
    drift_report_file_path:str


## for data transformation componenets output
@dataclass
class DataTransformationArtifacts:
    transformed_object_file_path:str   ##transfromed object file path
    transformed_train_file_path:str
    transformed_test_file_path:str


