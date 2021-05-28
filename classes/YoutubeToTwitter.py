class YoutubeToTwitter():
    def __init__(self, mongo_connector, youtube_handler, twitter_connector):
        self.mongo_conn = mongo_connector.setDatabase().setCollection()
        self.yt_handler = youtube_handler
        self.twitter = twitter_connector
    
    def filterNotMatches(self, list1, list2):
        return list(set(list1) - set(list2))

    def getAllUnsendVideos(self, size_list=5):
        dict_unsend = dict()
        for document in self.mongo_conn.getAllDocuments():
            print(f"{document['name']} ({document['_id']})", end=': ')

            channel_unsend_vids = self.getChannelUnsendVideos(document, size_list)
            dict_unsend.update(channel_unsend_vids)
            not_matches_list = channel_unsend_vids[document['_id']]

            print( len(not_matches_list), not_matches_list )
        
        return dict_unsend
    
    def getChannelUnsendVideos(self, document, size_list=5):
        self.yt_handler.loadListVideos(document['_id'], size_list)
        video_id_list = self.yt_handler.getVideoIDList()
        not_matches_list = self.filterNotMatches( video_id_list, document['video_ids'] )

        return {document['_id']: not_matches_list}

    # Atualiza Banco de Dados Mongo com os Canais que estão no TXT
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
    

    def sendTwitterChooser(self, channel_id, video_id):
        from pytube import YouTube
        from datetime import datetime, timedelta

        video_url = self.yt_handler.getVideoURL(video_id)
        youtube = YouTube(video_url)
        video_date = youtube.publish_date.date()
        limit_date = datetime.today() - timedelta(days=2)
        video_length = youtube.length
        video_author = youtube.author

        if ( video_date < limit_date.date()):
            print(f'{video_author}: Vídeo {video_url} é muito ANTIGO: {video_date}.')
        elif ( video_length >= 220 and video_length <= 300):
            print(f'{video_author}: Vídeo {video_url} é meio LONGO: {video_length} segundos. Enviando somente o link.')
            self.sendImage(channel_id, video_id, video_author, video_url, youtube)
        elif (video_length > 300):
            print(f'{video_author}: Vídeo {video_url} é muito LONGO: {video_length} segundos.')
        else:
            print(f'{video_author}: Vídeo {video_url} Enviando!')
            self.sendVideo(channel_id, video_id, video_author, video_url, youtube)

        self.updateVideoIDs(channel_id, video_id)

    def updateVideoIDs(self, channel_id, video_id):
        document = self.mongo_conn.getDocumentByID(channel_id)
        
        yt_channel_model = YoutubeChannelsModel(**document)
        yt_channel_model.addVideoID(video_id)
        yt_channel_model.updateDocumentVideoIDs(mongo_connector.collection)

    def sendImage(self, channel_id, video_id, video_author, video_url, youtube):
        image_path = self.saveImage(video_id)
        media_id = self.loadMedia(image_path)
        message = f'Vídeo novo do {video_author}: {youtube.title}'
        message += f'\n\nLink: {video_url}'
        
        self.updateStatus(message, media_id)

    def sendVideo(self, channel_id, video_id, video_author, video_url, youtube):
        video_path = self.saveVideo(youtube)
        media_id = self.loadMedia(video_path)
        message = f'Vídeo novo do {video_author}: {youtube.title}'
        message += f'\n\nLink: {video_url}'

        self.updateStatus(message, media_id)
    
    def saveImage(self, video_id):
        import requests
        image_url = self.yt_handler.getVideoMaxResThumbURLByID(video_id)
        image_path = 'download/image.jpg'
        response = requests.get(image_url)
        
        with open(image_path, 'wb') as file:
            file.write(response.content)
        
        return image_path

    def saveVideo(self, youtube):
        video = youtube.streams.filter(mime_type='video/mp4',
                               custom_filter_functions=[lambda s: (s.resolution == '720p') or (s.resolution == '480p')])\
                               .first()

        print('Baixando vídeo: ', video)
        video.download(output_path='download', filename='video')

        return 'download/video.mp4'

    def loadMedia(self, file_path):
        with open(file_path, 'rb') as file:
            if ('video.mp4' in file_path):
                response = self.twitter.upload_video(media=file, media_type='video/mp4', media_category='tweet_video', check_progress=True)
            else:
                response = self.twitter.upload_media(media=file)
        
        media_id = [response['media_id']]

        return media_id
    
    def updateStatus(self, message, media_id):
        self.twitter.update_status(status=message, media_ids=media_id)

    def startSend(self, size_list=5, document=None):
        from time import sleep
        if document:
            unsend_dict = document
        else:
            print('startSend() -> getAllUnsendVideos()')
            unsend_dict = self.getAllUnsendVideos(size_list)
        
        print('\nstartSend() -> sendTwitterChooser()')
        for key, value in unsend_dict.items():
            print(key, value)
            for video_id in value:
                self.sendTwitterChooser(key, video_id)
                sleep(120)
            print()