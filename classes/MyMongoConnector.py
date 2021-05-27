class MyMongoConnector():
    def __init__ (self, url_connection):
        self.connectDB(url_connection)

    def connectDB(self, url_connection):
        from pymongo import MongoClient
        self.client = MongoClient(url_connection)

        return self

    def setDatabase(self, database_name='myFirstDatabase'):
        self.database = self.client[database_name]

        return self

    def setCollection(self, collection_name='youtubeChannels'):
        self.collection = self.database[collection_name]

        return self

    def getAllDocuments(self):
        return self.collection.find({})

    def getDocumentByID(self, document_id):
        return self.collection.find_one({'_id': document_id})
    
    def dropCollection(self):
        return self.collection.drop()