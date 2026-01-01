## Here we will setup ETL pipeline(extract , transform, load) , in which we will extract data and tranform it and then load to mongo Db
## PDF attached already on notebook

import os
import sys
import json

from dotenv import load_dotenv  ## to get mogodb url from .env
load_dotenv()

MONGO_DB_URL=os.getenv('MONGODB_URL')
# print(MONGO_DB_URL)    #for checking

import certifi    ##packages thta provide, set of root certificates,which commenly used by python library's need to make the secure Http connection ,
## so when we made request ,so when it check the request, it get that secure request it is.
ca=certifi.where()  ## retreive the part of bundle of ca certificate and store ot in ca(certificate Authority)


## Now we have to read data from dataset locally
import pandas as pd
import numpy as np
import pymongo
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException

class NetworkDataExtract():    ## This will basically our ETL Pipeline
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def csv_to_json_converter(self,file_path):   ## convert csv to json for mongodb
        try:
            data=pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True) ## we have to drop index
            ## lets convert to JSON, see PDF attached also
            records=list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def insert_data_mongodb(self,records,database,collection):
        try:
            self.database=database        #The name of the database (e.g., "vivekai").
            self.collection=collection    #collection: The "table" within that database (e.g., "PhishingData").
            self.records=records          #The list of website data (the list of dictionaries we discussed).

            ##to create mongo_clienta
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            self.database=self.mongo_client[self.database]      # structure: Client --> Database --> Collection

            self.collection=self.database[self.collection]
            self.collection.insert_many(self.records)
            return (len(self.records))
        except Exception as e:
            raise NetworkSecurityException(e,sys)
                            

'''

records=list(json.loads(data.T.to_json()).values())


1. data.T (Transpose)
This flips the DataFrame. Rows become columns, and columns become rows.

Why? By default, pandas' .to_json() method often structures data by column. Transposing it prepares the data so that the "keys" in the resulting JSON will be the row indices.

2. .to_json()
This converts the transposed DataFrame into a JSON-formatted string. Because it was transposed, the resulting string looks like this: {"0": {"Name": "Alice", "Age": 25}, "1": {"Name": "Bob", "Age": 30}}

3. json.loads(...)
The json.loads function takes that JSON string and turns it back into a standard Python dictionary.

4. .values()
Since the dictionary created in the previous step uses the row index (e.g., "0", "1") as the keys, calling .values() strips those keys away and keeps only the data objects (the rows).

5. list(...)
Finally, this wraps those values into a clean Python list.
'''

## to execute ETL pipeline
if __name__=="__main__":
    FILE_PATH="Network_data\phisingData.csv"
    DATABASE="VIVEKAI"
    collection="Network data"

    ##initailise class
    networkdataobj=NetworkDataExtract()
    records=networkdataobj.csv_to_json_converter(file_path=FILE_PATH)
    print(records)
    no_of_records=networkdataobj.insert_data_mongodb(records,DATABASE,collection)
    print(no_of_records)