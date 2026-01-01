## This will have all the configuration details, and basic configuraton
from datetime import datetime
import os
from networksecurity.constant import training_pipeline


print(training_pipeline.PIPELINE_NAME)
print(training_pipeline.DATA_INGESTION_COLLECTION_NAME)


class TrainingPipelineConfig:  ##when we talk about TrainigPipelineCOnfig, we need to have this basic info
    def __init__(self,timestamp=datetime.now()):
        timestamp=timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name=training_pipeline.PIPELINE_NAME   ## this all are coming from constent -> training_pipeline -> __init__.py
        self.artifact_name=training_pipeline.ARTIFACT_DIR      
        self.artifact_dir=os.path.join(self.artifact_name, timestamp)
        self.timestamp:str = timestamp
        pass

## Lets creta data_ingestion_config(see the pdf in notebook)
class DataIngestionConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):

        ## we are initlising dataIngestion Directory to "training_pipeline.DATA_INGESTION_DIR_NAME" to this perticular values
        self.data_ingestion_dir:str=os.path.join(
            training_pipeline_config.artifact_dir,training_pipeline.DATA_INGESTION_DIR_NAME
        )

        self.feature_store_file_path: str = os.path.join(
                self.data_ingestion_dir, 
                training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR, 
                training_pipeline.FILE_NAME
            )
        
        self.training_file_path: str = os.path.join(
                self.data_ingestion_dir, 
                training_pipeline.DATA_INGESTION_INGESTED_DIR, 
                training_pipeline.TRAIN_FILE_NAME
            )
        
        self.testing_file_path: str = os.path.join(
                self.data_ingestion_dir, 
                training_pipeline.DATA_INGESTION_INGESTED_DIR, 
                training_pipeline.TEST_FILE_NAME
            )
        
        self.train_test_split_ratio: float = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        self.collection_name: str = training_pipeline.DATA_INGESTION_COLLECTION_NAME
        self.database_name: str = training_pipeline.DATA_INGESTION_DATABASE_NAME
        pass