import pymongo as pm
import pandas as pd
from  dataclasses import dataclass
import os


@dataclass
class DataIngestion:
    
    def initiate_data_ingestion(self):
        try :
            file_path = os.path.join(os.getcwd() , "dataset\google_data_merged.csv")
            df =pd.read_csv(file_path) 
            if "_id" in df.columns:   #droping unnecessary column from dataset 
                df.drop("_id"  , axis=1 , inplace=True)
            return df
        except Exception as e:
            print(e)  

obj = DataIngestion()
try :
    df =obj.initiate_data_ingestion()
    print(f"\ndata ingestion initiated Sucessfully")
except Exception as e:
   print(e)   
