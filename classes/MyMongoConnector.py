# CLASSE QUE GERECIA A CONECXÃO COM O MONGODB
class MyMongoConnector():
    def __init__ (self, url_connection):
        self.connectDB(url_connection)

    # CONECTA A UM BANCO MONGO COM BASE EM UMA URL
    def connectDB(self, url_connection):
        from pymongo import MongoClient
        self.client = MongoClient(url_connection)

        return self

    # CONECTA, OU CRIA SE ÃO EXISTIR, UM BANCO DE DADOS
    def setDatabase(self, database_name='myFirstDatabase'):
        self.database = self.client[database_name]

        return self

    # CONECTA, OU CRIA SE ÃO EXISTIR, COLEÇÃO (TABELA)
    def setCollection(self, collection_name='youtubeChannels'):
        self.collection = self.database[collection_name]

        return self

    # RETORNA TODOS OS DOCUMENTOS DA COLEÇÃO CONECTADA
    def getAllDocuments(self):
        return self.collection.find({})

    # RETORNA UM DOCUMENTO DA COLEÇÃO CONECTADA BASEADO NO ID
    def getDocumentByID(self, document_id):
        return self.collection.find_one({'_id': document_id})
    
    # EXCLUI A COLEÇÃO CONECTADA
    def dropCollection(self):
        return self.collection.drop()