import os
import sys


import numpy as np
import pandas as pd
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.artifacts_entity import DataTransformationArtifacts, ModelTrainerArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig


## to save the pickle file of the model
from networksecurity.utils.main_utils.utils import save_object,load_object   # this load_object is to read pickle file
from networksecurity.utils.main_utils.utils import load_numpy_array_data,evaluate_models

from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.ml_utils.metric.classification_metric import get_classfication_report  ## used for calculate metric of model


from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)
import mlflow

class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,data_tranformation_artifact:DataTransformationArtifacts):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifacts=data_tranformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def track_mlflow(self,best_model,classificationmetric):
        with mlflow.start_run():
            f1_score=classificationmetric.f1_score
            precision_score=classificationmetric.precision_score
            recall_score=classificationmetric.recall_score

            ##log in local system
            mlflow.log_metric("f1_score",f1_score)
            mlflow.log_metric("Precision_score",precision_score)
            mlflow.log_metric("recall_score",recall_score)
            mlflow.sklearn.log_model(best_model,'model')



    def train_model(self,x_train,y_train,x_test,y_test):
        try:

            models = {
                    "Random Forest": RandomForestClassifier(verbose=1),  #verbose=1 , to see the details during training
                    "Decision Tree": DecisionTreeClassifier(),
                    "Gradient Boosting": GradientBoostingClassifier(verbose=1),
                    "Logistic Regression": LogisticRegression(verbose=1),
                    "AdaBoost": AdaBoostClassifier(),
                }
            
            ##for hyper parameter tuning
            params={
                "Decision Tree": {
                    'criterion':['gini', 'entropy', 'log_loss'],
                    # 'splitter':['best','random'],
                    # 'max_features':['sqrt','log2'],
                },
                "Random Forest":{
                    'criterion':['gini', 'entropy', 'log_loss'],
                    
                    'max_features':['sqrt','log2',None],
                    'n_estimators': [8,16,32,128,256]
                },
                "Gradient Boosting":{
                    # 'loss':['log_loss', 'exponential'],
                    'learning_rate':[.1,.01,.05,.001],
                    'subsample':[0.6,0.7,0.75,0.85,0.9],
                    # 'criterion':['squared_error', 'friedman_mse'],
                    # 'max_features':['auto','sqrt','log2'],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Logistic Regression":{},
                "AdaBoost":{
                    'learning_rate':[.1,.01,.001],
                    'n_estimators': [8,16,32,64,128,256]
                }    
                } 
            
            model_report : dict = evaluate_models(X_train=x_train,y_train=y_train,X_test=x_test,y_test=y_test,models=models,param=params)

            ## now after this , lets find best score from all this
            ## To get best model score from dict
            best_model_score = max(sorted(model_report.values()))

            ## now to get best model name
            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]

            best_model=models[best_model_name]
            y_train_pred=best_model.predict(x_train)



            ##lets for classification report
            classification_train_metric=get_classfication_report(y_train,y_train_pred)

            
            ## to Track the MLflow
            # mlflow: this is open source tool to manage entire lifecycle of datascience project, we can store various metric and then we can visulise them 
            ## after we get the best model, for that model whatever classifcation metric we get, we have to track that entire 
            #thung is mlflow
            self.track_mlflow(best_model,classification_train_metric)   #fn defined in class itself
            



            y_test_pred=best_model.predict(x_test)
            classification_test_metric=get_classfication_report(y_test,y_test_pred)

            ##to track mlflow of test also
            self.track_mlflow(best_model,classification_test_metric)   #fn defined in class itself

            ##for any new data we have to first transfrom it and then predict it
            preprocessor=load_object(file_path=self.data_transformation_artifacts.transformed_object_file_path)

            model_dir_path=os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path,exist_ok=True)


            ##lets make this both as a pickle file
            Network_Model=NetworkModel(preprocessor=preprocessor,model=best_model)
            save_object(self.model_trainer_config.trained_model_file_path,obj=NetworkModel)


            ## model Trainer Artifacts
            model_trainer_artfacts=ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                                train_metric_artifact=classification_train_metric,
                                test_metric_artifact=classification_test_metric)
            
            logging.info(f"Model trainer artifact: {model_trainer_artfacts}")
            
            return model_trainer_artfacts
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            train_file_path=self.data_transformation_artifacts.transformed_train_file_path
            test_file_path=self.data_transformation_artifacts.transformed_test_file_path
        
            ## load training array and test array
            train_array=load_numpy_array_data(train_file_path)
            test_array=load_numpy_array_data(test_file_path)


            ##split in train and test
            x_train,y_train,x_test,y_test=(
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1],
            )

            ##model train
            model=self.train_model(x_train,y_train,x_test,y_test)

        except Exception as e:
            raise NetworkSecurityException(e,sys)