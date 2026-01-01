## file for push data in mongoDB Atlas 
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://vivekchouhan590_db_user:<password>@cluster0networksecurity.22dnv2e.mongodb.net/?appName=Cluster0NetworkSecurity"
## add password when needed


## for testing:

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)