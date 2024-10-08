import pymongo as pm
import pandas as pd
from config import mongo_client #loading mongo url using .env 
from  dataclasses import dataclass



@dataclass
class DataIngestion:
    
    def initiate_data_ingestion(self):
        try :
            df =pd.DataFrame(mongo_client["Google"]["apps"].find())  #data ingestion from MngoDB Atlas
            if "_id" in df.columns:   #droping unnecessary column from dataset 
                df.drop("_id"  , axis=1 , inplace=True)
            return df
        except Exception as e:
            print(e)  

obj = DataIngestion()
try :
    df =obj.initiate_data_ingestion()
    #print(df.head())
except Exception as e:
   print(e)   
