from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import sys,os
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer  ## for missing values
from sklearn.pipeline import Pipeline


##to remove target column from dataset
from networksecurity.constant.training_pipeline import TARGET_COLUMN
from networksecurity.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS ## use inside knnimputer


##to get input from data validation artifacts
from networksecurity.entity.artifacts_entity import (
    DataTransformationArtifacts,    ##this is the final output of data tranformation components
    DataValidationArtifact
)

##we also require configuration file
from networksecurity.entity.config_entity import DataTransformationConfig


'''
now to save the npy file and preprocessor object file(output of this components), we have to create a
function for it, and this fn are in utils.py
'''
from networksecurity.utils.main_utils.utils import save_numpy_array_data,save_object


class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,   ##entire pipeline is given of previous stage
                 data_transfromation_config:DataTransformationConfig):
        try:
            self.data_validation_artifacts=data_validation_artifact
            self.data_transformation_config=data_transfromation_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    ## for reading train and test data
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    # function to initlaise knn imputer
    def get_data_tranformer_object(cls)->Pipeline:
        
        """
        It initialises a KNN imputer object with the parameters specified in the training_pipeline.py file
        and returns a pipeline object with the KNN imputer object as the first step
        
        Args:
        cls: DataTransfomtion

        Return:
        A pipeline object 
        """
        logging.info("Entered get_data_tranformer_object method of DataTransfomation class")
        
        try:
            imputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS) ##** means whaterver I am giving here ,will considered as key values pair
            logging.info(f"Initilised KNNImputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS}")

            processor:Pipeline=Pipeline(
                steps=[
                    ("Imputer",imputer)
                ]
            )

            return processor



        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def initiate_data_transformation(self)->DataTransformationArtifacts:
        logging.info("Entered initiate_data_transformation method of DataTransformation class")
        try:
            logging.info("starting data Tranformation")

            # read train and test data, we can create a static methods and this paths are coming from data validation artifacts
            train_df=DataTransformation.read_data(self.data_validation_artifacts.valid_train_file_path)
            test_df=DataTransformation.read_data(self.data_validation_artifacts.valid_test_file_path)


            ## first remove the target column amd then apply knn imputer
            ## and this is classification preoblem, so lets convert target as 1 amd 0
            input_feture_train_df=train_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df=train_df[TARGET_COLUMN]
            target_feature_train_df=target_feature_train_df.replace(-1,0)

            input_feature_test_df=test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df=test_df[TARGET_COLUMN]
            target_feature_test_df=target_feature_test_df.replace(-1,0)

            ## we have to implement the KNN imputer
            preprocessor=self.get_data_tranformer_object()
            preprocessor_object=preprocessor.fit(input_feture_train_df)

            tranformed_input_train_feature=preprocessor_object.transform(input_feture_train_df)
            tranformed_input_test_feature=preprocessor_object.transform(input_feature_test_df)

            ## now we will combine this data with target
            train_arr=np.c_[tranformed_input_train_feature,np.array(target_feature_train_df)]
            test_arr=np.c_[tranformed_input_test_feature,np.array(target_feature_test_df)]

            ##now we will save this numpy array and pickle file of preprocessor
            save_numpy_array_data( self.data_transformation_config.transformed_train_file_path, array=train_arr, )
            save_numpy_array_data( self.data_transformation_config.transformed_test_file_path, array=test_arr, )
            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor_object,)


            ## Preparing artifacts
            data_transformation_artifacts=DataTransformationArtifacts(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )

            return data_transformation_artifacts
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        