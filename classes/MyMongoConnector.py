class MyMongoConnector():
    def __init__ (self, url_connection):
        self.connectDB(url_connection)

    def connectDB(self, url_connection):
        from pymongo import MongoClient
        self.client = MongoClient(url_connection)

        return self

    def choiceDatabase(self, database_name='myFirstDatabase'):
        self.database = self.client[database_name]

        return self

    def getCollection(self, collection_name='youtubeChannels'):
        self.collection = self.database[collection_name]

        return self

    def getAllDocuments(self, collection_name='youtubeChannels'):
        return self.collection.find({})