from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

## call Config file for Data Ingestion cofig
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig

## this is for output of dataIngestion Components
from networksecurity.entity.artifacts_entity import DataIngestionArtifacts

import os
import sys
import pandas as pd
import numpy as np
import pymongo
from sklearn.model_selection import train_test_split



## read from mongoDB
from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL=os.getenv("MONGODB_URL")   ## fetch value of "MONGODB_URL" from .env


class DataIngestion:  
    def  __init__(self,data_ingestion_config:DataIngestionConfig):  ## we have to know all configuration
        try:
            ## we will define entire data ingestion config from this DataIngestionConfig class
            self.data_ingestion_config=data_ingestion_config    ## this LHS variable will have all access of RHS class obj values
        except Exception as e:
            raise NetworkSecurityException(e,sys)


    # from momgoDB collection export data as Dataframe
    def export_collection_as_dataframe(self):
        '''
        This function will read data from MOngoDB
        '''
        try:
            database_name=self.data_ingestion_config.database_name   ## from config_entity file
            collection_name=self.data_ingestion_config.collection_name
            
            ##lets create mongo clienta and read the data and store in collection
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            collection=self.mongo_client[database_name][collection_name]

            ##convert it into datframe
            df=pd.DataFrame(list(collection.find()))
            
            ##when we read data from mongoDB , it add "_id" column in it
            if "_id" in df.columns.to_list():
                df=df.drop(columns=["_id"],axis=1)


            df.replace({"na":np.nan},inplace=True)

            return df

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    ##export this data to feature store(raw data here)
    def export_data_into_feature_store(self, dataframe:pd.DataFrame):
        try:
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path
            #creating folder
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    

    ## Now we will split this data in train and test data
    def split_data_as_train_test(self,dataframe:pd.DataFrame):
        try:
            train_set, test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio
            )
            logging.info("Performed train test split on the dataframe")
            logging.info("Exited split_data_as_train_test method")
            
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)
            logging.info(f"Exporting train and test file path")
            train_set.to_csv(
                self.data_ingestion_config.training_file_path, index=False, header=True
            )
            test_set.to_csv(
                self.data_ingestion_config.testing_file_path, index=False, header=True
            )
            logging.info(f"Exported train and test file path")
        except Exception as e:
            raise NetworkSecurityException(e,sys)





    def initiate_data_ingestion(self):
        try:
            ## we will read from mongoDB
            dataframe=self.export_collection_as_dataframe()
            # ## store this raw data in local (feature store)
            dataframe=self.export_data_into_feature_store(dataframe)
            # ## now split the data 
            self.split_data_as_train_test(dataframe)


            # ##for output of this DataIngestionComponents
            dataingestionartifacts=DataIngestionArtifacts(train_file_path=self.data_ingestion_config.training_file_path,
                                                          test_file_path=self.data_ingestion_config.testing_file_path)
            
            return dataingestionartifacts  ## this is final output of DataIngestion
            # print(dataframe)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
## After this we have to get the output of DataIngestion and that output is train_file_path and test_path file
## and this path will get in entity->artifacts_entity.py


# if __name__=="__main__":
#     train_pipe=TrainingPipelineConfig()
#     dataconfig=DataIngestionConfig(train_pipe)
#     exporcollection=DataIngestion(dataconfig)
    