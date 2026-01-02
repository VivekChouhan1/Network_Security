## input of data validation come from data ingestion artifacts
from networksecurity.entity.artifacts_entity import DataIngestionArtifacts,DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig,TrainingPipelineConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

## for data drift
from scipy.stats import ks_2samp   ##check drift chnage in 2 samples
import pandas as pd
import os,sys

## for read_yaml_file fn
from networksecurity.utils.main_utils.utils import read_yaml_file



#to write report in yaml file
from networksecurity.utils.main_utils.utils import write_yaml_file


## To check the datatype, type for validation, we should havethe schema of dataset we used for train.
## so that schema is present in (data_schema->schema.yaml)
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
## Now we have to read that schema and then we compare


class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifacts,  ##data_ingestion_artifact is input of this
                  data_validation_config:DataValidationConfig):  ##data_validation_config is output
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self._schema_config=read_yaml_file(SCHEMA_FILE_PATH)   ##and this read_yaml_file code will be written in utils folder
        except Exception as e:
            raise NetworkSecurityException(e,sys)



    ## now we have to read the data file only onces, so we can create it as static method, so we do not have to make object of it also
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys) 
        
    def validate_no_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns=len(self._schema_config)
            logging.info(f"required number of columns:{number_of_columns}")
            logging.info(f"Data frame has column {len(dataframe.columns)}")
            if len(dataframe.columns)==number_of_columns:
                return True
            return False
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    def validate_no_of_numerical_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            number_of_num_columns=len(self._schema_config.get('numerical_columns'))
            logging.info(f"required number of columns:{number_of_num_columns}")
            logging.info(f"Data frame has column {len(dataframe.columns)}")
            if len(dataframe.columns==number_of_num_columns):
                return True
            return False
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        


    def detect_dataset_drift(self,base_df,current_df,threshold=0.05)->bool:
        try:
            status=True
            report={}
            for column in base_df.columns:
                d1=base_df[column]
                d2=current_df[column]
                is_sample_dist_same_or_not=ks_2samp(d1,d2) ## threshold is 0.05
                if threshold<=is_sample_dist_same_or_not.pvalue:
                    is_found=False
                else:  ## chnage in distribution
                    is_found=True
                    status=False
                
                report.update({column:{"p_value":float(is_sample_dist_same_or_not.pvalue),
                                       "drift_status":is_found}})
                
            #create directory
            drift_report_file_path=self.data_validation_config.drift_report_file_path
            dir_path=os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)

            ## after this we have to write our yaml file, fn present in utils.py
            write_yaml_file(file_path=drift_report_file_path, content=report)
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        



    def initiate_data_validation(self)->DataIngestionArtifacts:
        try:
            # first we get train_file and test file from data_ingestion comopnents
            train_file_path=self.data_ingestion_artifact.train_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path

            ## read the data from train and test
            train_dataframe=DataValidation.read_data(train_file_path)
            test_dataframe=DataValidation.read_data(test_file_path)

            ## now we have to validate the data with our schema
            status=self.validate_no_of_columns(dataframe=train_dataframe)
            if not status:
                error_message=f"Train dataframe does not contain all columns. \n"

            status=self.validate_no_of_columns(dataframe=test_dataframe)
            if not status:
                error_message=f"Test dataframe does not contain all columns. \n"


            ## now lets check for numerical columns
            status=self.validate_no_of_numerical_columns(dataframe=train_dataframe)
            if not status:
                error_message=f"Train dataframe does not contain all numerical columns. \n"
            status=self.validate_no_of_numerical_columns(dataframe=test_dataframe)
            if not status:
                error_message=f"Test dataframe does not contain all numerical columns. \n"

            ## now after this all, we have to check data Drift:
            status=self.detect_dataset_drift(base_df=train_dataframe,current_df=test_dataframe)
            dir_path=os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)


            ##if status is True, we just make
            train_dataframe.to_csv(
                self.data_validation_config.valid_train_file_path,index=False,header=True
            )

            test_dataframe.to_csv(
                self.data_validation_config.valid_test_file_path,index=False,header=True
            )


            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.train_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_test_file_path=None,
                invalid_train_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )


            return data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)