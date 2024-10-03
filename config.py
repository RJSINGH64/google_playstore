from dotenv import load_dotenv
import pymongo 
from dataclasses import dataclass
import os

print("--->","loading .env" ,"<-----")
load_dotenv()


@dataclass #using decorator 
class EnvironmentsVariables():
     mongo_url:str =os.getenv("MONGO_DB_URL")

env_ob =EnvironmentsVariables()
mongo_client = pymongo.MongoClient(env_ob.mongo_url)
print("--->","connected to MongoDB Atlas" , "<-----")
