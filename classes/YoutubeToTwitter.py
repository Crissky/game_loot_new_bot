class YoutubeToTwitter():
    def __init__(self, mongo_connector, youtube_handler):
        self.mongo_conn = mongo_connector
        self.yt_handler = youtube_handler
    
    def filterNotMatches(self, list1, list2):
        return list(set(list1) - set(list2))

    def getAllUnsendVideos(self):
        dict_unsend = dict()
        for document in self.mongo_conn.getAllDocuments():
            print(f"{document['name']} ({document['_id']})", end=': ')
            self.yt_handler.loadListVideos(document['_id'])
            video_id_list = self.yt_handler.getVideoIDList()
            not_matches_list = self.filterNotMatches( video_id_list, document['video_ids'] )
            dict_unsend[document['name']] = not_matches_list
            print( len(not_matches_list), not_matches_list )
        
        return dict_unsend