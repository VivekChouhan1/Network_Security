##to testing
import sys
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig


if __name__=="__main__":
    try:
        trainingpipelineconfig=TrainingPipelineConfig()
        data_ingestion_config=DataIngestionConfig(trainingpipelineconfig)
        dataingestion=DataIngestion(data_ingestion_config)
        logging.info('Initiate the data ingestion')

        ## lets call the fun from data_ingestion.py
        dataIngestionArtifacts=dataingestion.initiate_data_ingestion()
        print(dataIngestionArtifacts)
    except Exception as e:
        raise NetworkSecurityException(e,sys)