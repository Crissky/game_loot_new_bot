class YoutubeAPIHandler():
    def __init__(self, YOUTUBE_API_KEY):
        self.API_KEY = YOUTUBE_API_KEY
        self.base_url = "https://www.googleapis.com/youtube/v3/search?key={API_YT}&channelId={CHANNEL_ID}&part=id&order=date&maxResults={MAX_RESULTS}&fields=items(id)"
        self.base_video_url = "https://www.youtube.com/watch?v={videoId}"
        self.base_maxresthumb_url = 'https://i.ytimg.com/vi/{videoId}/maxresdefault.jpg'
        self.list_videos_json = None

    def getURL(self, channel_id, max_results=1):
    
        return self.base_url.format(API_YT=self.API_KEY, CHANNEL_ID=channel_id, MAX_RESULTS=max_results)
    
    def loadListVideos(self, channel_id, max_results=5):
        import requests
        self.last_url = self.getURL(channel_id, max_results)
        response = requests.get(self.last_url)
        self.list_videos_json = response.json()

        if ('error' in self.list_videos_json.keys()):
            raise Exception(self.list_videos_json)

        return self

    def checkLoadListVideos(self):
        if(not self.list_videos_json):
            raise Exception("Vídeos não carregados: Use a função 'loadListVideos()' antes desse método para carregar os vídeos.")
        
    def getVideoList(self):
        self.checkLoadListVideos()
        
        video_json_list = self.list_videos_json['items'][:]
        filtered_list = [item for item in video_json_list if item['id']['kind'] == 'youtube#video']
        
        return filtered_list
    
    def getLastVideo(self):
        self.checkLoadListVideos()
        
        return self.getVideoList()[0]

    def getVideoID(self, video_json):
        video_id = None
        if (video_json['id']['kind'] == 'youtube#video'):
            video_id = video_json['id']['videoId']

        return video_id
    
    def getLastVideoID(self):
        self.checkLoadListVideos()
        
        video_json = self.getLastVideo()
        return self.getVideoID(video_json)
    
    def getVideoIDList(self):
        self.checkLoadListVideos()

        return [self.getVideoID(video_json) for video_json in self.getVideoList() if video_json['id']['kind'] == 'youtube#video']
    
    def getVideoURL(self, video_id):
    
        return self.base_video_url.format(videoId=video_id)
    
    def getLastVideoURL(self):
        self.checkLoadListVideos()
        
        video_id = self.getLastVideoID()
        return self.getVideoURL(video_id)
    
    def getVideoURLList(self):
        self.checkLoadListVideos()
        
        return [self.getVideoURL(video_id) for video_id in self.getVideoIDList()]

    def getVideoMaxResThumbURLByID(self, video_id):
        
        return self.base_maxresthumb_url.format(videoId=video_id)