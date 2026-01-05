## This is used to do prediction

import os
import sys

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer


## lets call for config entity
from networksecurity.entity.config_entity import(
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig,
)


## lets call for artifacts
from networksecurity.entity.artifacts_entity import (
    DataIngestionArtifacts,
    DataValidationArtifact,
    DataTransformationArtifacts,
    ModelTrainerArtifact,
)

## now we have to run this all file/pipeline
class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config=TrainingPipelineConfig()
    
    def start_data_ingestion(self)->DataIngestionArtifacts:
        try:
            self.data_ingestion_config=DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("start data Ingestion")
            data_ingestion=DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifacst=data_ingestion.initiate_data_ingestion()
            logging.info(f"Data ingestion completed and artifcsts: {data_ingestion_artifacst}")
            return data_ingestion_artifacst
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifacts)->DataValidationArtifact:
        try:
            data_validation_config=DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            data_validation=DataValidation(data_ingestion_artifact=data_ingestion_artifact,data_validation_config=data_validation_config)
            logging.info("Initiate the data Validation")
            data_validation_artifact=data_validation.initiate_data_validation()
            logging.info("Data validation completed and artifcsts")
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_data_transformation(self,data_validation_artifact:DataValidationArtifact)->DataTransformationArtifacts:
        try:
            data_transformation_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            data_transformation = DataTransformation(data_validation_artifact,data_transformation_config)
            logging.info("Initiate the data transformation")
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info("Data transformtion completed and artifcsts")
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_model_trainer(self,data_transformation_artifact:DataTransformationArtifacts):
        try:
            model_trainer_config= ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)

            model_trainer = ModelTrainer(
                model_trainer_config=model_trainer_config,
                data_transformation_artifact=data_transformation_artifact
            )


            model_trainer_artifact = model_trainer.initiate_model_trainer()

            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        



    ## to run the pipeline
    def run_pipeline(self):
            try:
                logging.info('RUNNING THE RUN PIPE LINE FUCNTION')
                data_ingestion_artifact=self.start_data_ingestion()
                data_validation_artifact=self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
                data_transformation_artifact=self.start_data_transformation(data_validation_artifact=data_validation_artifact)
                model_trainer_artifact=self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
                
                logging.info('RUN PIPELINE FUNCTION EXITED SUCCESSFULLY!')
                return model_trainer_artifact

            except Exception as e:
                raise NetworkSecurityException(e,sys)
            

# if __name__=="__main__":
#     traning=TrainingPipeline()
#     traning.run_pipeline()
            
