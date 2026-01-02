##to testing
import sys
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig



# for data validation
from networksecurity.components.data_validation import DataValidation

# for data tranformation
from networksecurity.components.data_transformation import DataTransformation



if __name__=="__main__":
    try:
        trainingpipelineconfig=TrainingPipelineConfig()
        data_ingestion_config=DataIngestionConfig(trainingpipelineconfig)
        dataingestion=DataIngestion(data_ingestion_config)
        logging.info('Initiate the data ingestion')
        ## lets call the fun from data_ingestion.py
        dataIngestionArtifacts=dataingestion.initiate_data_ingestion()
        logging.info("Data Initition completed")
        print(dataIngestionArtifacts)


        ## start with data validation
        data_validation_config=DataValidationConfig(trainingpipelineconfig)
        datavalidation=DataValidation(dataIngestionArtifacts,data_validation_config)
        logging.info("initiate Data Validation")
        data_validation_artifacts=datavalidation.initiate_data_validation()
        logging.info("Data Validation completed")
        print(data_validation_artifacts)
        ## when this executed, it creted articats and logs folder, right now we will delete it


        ## for data Transformation 
        data_transformation_config=DataTransformationConfig(trainingpipelineconfig)
        datatranformation=DataTransformation(data_validation_artifacts,data_transformation_config)
        logging.info("initiate Data Transformation")
        data_transformation_artifacts=datatranformation.initiate_data_transformation()
        logging.info("Data tranformation completed")
        print(data_transformation_artifacts)

    except Exception as e:
        raise NetworkSecurityException(e,sys)
    