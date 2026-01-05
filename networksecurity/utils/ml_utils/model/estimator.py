## to create the network data model pickle file,
## give all details related to model

from networksecurity.constant.training_pipeline import SAVED_MODEL_DIR,MODEL_FILE_NAME


import sys,os

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging


class NetworkModel:
    def __init__(self,preprocessor,model):
        try:
            self.preprocessor=preprocessor
            self.model=model
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def predict(self,x):
        try:
            x_transform=self.preprocessor.transform(x)    ##used to transform any new data and then transform
            y_hat=self.model.predict(x_transform)
            return y_hat
        except Exception as e:
            raise NetworkSecurityException(e,sys)