class YoutubeChannelsModel():
    def __init__(self, _id, name, video_ids=[]):
        self.data = dict()
        self.data['_id'] = _id
        self.data['name'] = name
        self.data['video_ids'] = video_ids
    
    def __repr__(self):
        return f"('_id': {self.data['_id']},'name': {self.data['name']}, 'video_ids': {self.data['video_ids']})"
    
    def updateDocumentVideoIDs(self, collection):
        query = {'_id': self.data['_id']}
        newvalues = { "$set": { "video_ids": self.data['video_ids'] } }
        collection.update_one(query, newvalues)