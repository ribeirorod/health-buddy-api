#connect to MongoDB Cloud Atlas
from pymongo import MongoClient
import json

user = 'dbadmin'
password = 'mongoatlas1305'
client = MongoClient(f"mongodb+srv://{user}:{password}@cluster0.cxvpd.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db=client.corpus


with open( 'legacy.json', 'r') as f:
    dados = json.load(f)

db.legacy.insert_many(dados)