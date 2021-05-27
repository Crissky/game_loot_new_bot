class YoutubeToTwitter():
    def __init__(self, mongo_connector, youtube_handler):
        self.mongo_conn = mongo_connector.setDatabase().setCollection()
        self.yt_handler = youtube_handler
    
    def filterNotMatches(self, list1, list2):
        return list(set(list1) - set(list2))

    def getAllUnsendVideos(self, size_list=5):
        dict_unsend = dict()
        for document in self.mongo_conn.getAllDocuments():
            print(f"{document['name']} ({document['_id']})", end=': ')

            self.yt_handler.loadListVideos(document['_id'], size_list)
            video_id_list = self.yt_handler.getVideoIDList()
            not_matches_list = self.filterNotMatches( video_id_list, document['video_ids'] )
            dict_unsend[document['_id']] = not_matches_list
            
            print( len(not_matches_list), not_matches_list )
        
        return dict_unsend
    
    def updateYoutubeChannelsCollection(self, youtube_channel_ids_url='https://raw.githubusercontent.com/Crissky/game_loot_news_bot/main/youtube_channel_ids.txt'):
        import requests
        from pytube import YouTube
        response = requests.get(youtube_channel_ids_url)
        youtube_channel_ids = response.text.splitlines()

        print("youtube_channel_ids:\n", '\n'.join(youtube_channel_ids))

        for channel_id in youtube_channel_ids:
            self.yt_handler.loadListVideos(channel_id, 10)
            video_url = self.yt_handler.getLastVideoURL()
            try:
                youtube = YouTube(video_url)
                channel_name = youtube.author

                yt_channel_model = YoutubeChannelsModel(channel_id, channel_name)
                self.mongo_conn.collection.insert_one(yt_channel_model.data)
            except Exception as e:
                print('O canal de id:', channel_id, "Não pode ser atualizado com a URL:", video_url)
                print('Motivo:', e)