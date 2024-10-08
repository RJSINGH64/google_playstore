from config import mongo_client
import pandas as pd
import pymongo
import os

file_path = os.path.join(os.getcwd() , "dataset\google_data_merged.csv") #after performing EDA inside research.py, dumping cleaned merge dataset inside MongoDb 
data_base= "Google"
collection='apps'

if __name__=="__main__":

   df= pd.read_csv(file_path)
   print("Rows =" ,df.shape[0] , "columns=" ,df.shape[1] )
   df_to_dict = df.to_dict(orient="records")   
   print("converted data into dict")
   mongo_client[data_base][collection].insert_many(df_to_dict)
   print("Data Sucessfully stored inside MongoDB")




    

