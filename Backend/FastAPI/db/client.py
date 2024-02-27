from pymongo import  MongoClient

#Base de datos Local
#db_client = MongoClient().local

#Base de datos remota
db_client = MongoClient("mongodb+srv://test:test@cluster0.lutmkfs.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0").test
