## this constent is used to store all file path and all constant values
import os
import sys
import numpy as np
import pandas as pd

"""
Lets define some common constent 
variable for training pipeline
"""

TARGET_COLUMN = "Result"
PIPELINE_NAME:str = "NetworkSecurity"
ARTIFACT_DIR: str = "Artifacts"
FILE_NAME: str = "phishingData.csv"


TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"
SCHEMA_FILE_PATH = os.path.join("data_schema", "schema.yaml")

SAVED_MODEL_DIR =os.path.join("saved_models")
MODEL_FILE_NAME = "model.pkl"



"""
DATA INGESTION RELATED CONSTANT START WITH DATA_INGESTION VAR NAME
"""
DATA_INGESTION_COLLECTION_NAME: str = "Network data"
DATA_INGESTION_DATABASE_NAME: str = "VIVEKAI"  ##same name which used while ETL pipeline
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "Ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float = 0.2