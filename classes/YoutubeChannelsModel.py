# CLASSE QUE REPRESENTA UM DOCUMENTO:
# self.data['_id'] = ID DO DOCUMENTO
# self.data['name'] = NOME DO CANAL
# self.data['video_ids'] = LISTA DE IDs DOS VÍDEOS QUE JÁ FORAM ANALISÁDOS PARA SEREM ENVIADOS
class YoutubeChannelsModel():
    def __init__(self, _id, name, video_ids=[]):
        self.data = dict()
        self.data['_id'] = _id
        self.data['name'] = name
        self.data['video_ids'] = video_ids
    
 
    def __repr__(self):
        return f"('_id': {self.data['_id']},'name': {self.data['name']}, 'video_ids': {self.data['video_ids']})"
    
 
    # ATUALIZA LISTA DE IDs DOS VÍDEOS DO BANCO DE DADOS
    def updateDocumentVideoIDs(self, collection):
        query = {'_id': self.data['_id']}
        newvalues = { "$set": { "video_ids": self.data['video_ids'] } }
        collection.update_one(query, newvalues)
    
    
    # ADICIONA UM NOVO ID DE VÍDEO A LISTA DE IDs DOS VÍDEOS DO OBJETO (LOCAL)
    def addVideoID(self, video_id):
        if (video_id not in self.data['video_ids']):
            self.data['video_ids'].append(video_id)
        else:
            print(f'Vídeo id "{video_id}" já está na lista.')