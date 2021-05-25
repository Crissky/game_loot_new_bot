class YoutubeChecker():
    def __init__(self, YOUTUBE_API_KEY):
        self.API_KEY = YOUTUBE_API_KEY
        self.base_url = "https://www.googleapis.com/youtube/v3/search?key={API_YT}&channelId={CHANNEL_ID}&part=snippet,id&order=date&maxResults={MAX_RESULTS}"
        self.base_video_url = "https://www.youtube.com/watch?v={videoId}"
        self.list_videos_json = None

    def getURL(self, channel_id, max_results=1):
    
        return self.base_url.format(API_YT=self.API_KEY, CHANNEL_ID=channel_id, MAX_RESULTS=max_results)
    
    def loadListVideos(self, channel_id, max_results=5):
        import requests
        self.last_url = self.getURL(channel_id, max_results)
        response = requests.get(self.last_url)
        self.list_videos_json = response.json()

        return self

    def checkLoadListVideos(self):
        if(not self.list_videos_json):
            raise Exception("Vídeos não carregados: Use a função 'loadListVideos()' antes desse método para carregar os vídeos.")
        
    def getVideoURL(self, video_id):
    
        return self.base_video_url.format(videoId=video_id)
    
    def getLastVideoURL(self):
        self.checkLoadListVideos()
        
        video_id = self.getLastVideoID()
        return self.getVideoURL(video_id)
    
    def getVideoURLList(self):
        self.checkLoadListVideos()
        
        return [self.getVideoURL(video_id) for video_id in self.getVideoIDList()]
    
    def getVideoList(self):
        self.checkLoadListVideos()

        return self.list_videos_json['items']
    
    def getLastVideo(self):
        self.checkLoadListVideos()
        
        return self.list_videos_json['items'][0]

    def getVideoID(self, video_json):
        return video_json['id']['videoId']
    
    def getLastVideoID(self):
        self.checkLoadListVideos()
        
        video_json = self.getLastVideo()
        return self.getVideoID(video_json)
    
    def getVideoIDList(self):
        self.checkLoadListVideos()

        return [video_json['id']['videoId'] for video_json in self.getVideoList()  if video_json['id']['kind'] == 'youtube#video']

    def getVideoTitle(self, video_json):
        return video_json['snippet']['title']
    
    def getLastVideoTitle(self):
        self.checkLoadListVideos()
        
        video_json = self.getLastVideo()
        return self.getVideoTitle(video_json)
    
    def getVideoChannelTitle(self, video_json):
        return video_json['snippet']['channelTitle']
    
    def getLastVideoChannelTitle(self):
        self.checkLoadListVideos()
        
        video_json = self.getLastVideo()
        return self.getVideoChannelTitle(video_json)
    
    def getVideoDescription(self, video_json):
        return video_json['snippet']['description']
    
    def getLastVideoDescription(self):
        self.checkLoadListVideos()
        
        video_json = self.getLastVideo()
        return self.getVideoDescription(video_json)
    
    def getVideoHighThumbURL(self, video_json):
        return video_json['snippet']['thumbnails']['high']['url']
    
    def getLastVideoHighThumbURL(self):
        self.checkLoadListVideos()
        
        video_json = self.getLastVideo()
        return self.getVideoHighThumbURL(video_json)
    
    def getVideoMaxResThumbURL(self, video_json):
        thumb_url = self.getVideoHighThumbURL(video_json)
        thumb_url = thumb_url.replace('hqdefault','maxresdefault')

        return thumb_url
    
    def getLastVideoMaxResThumbURL(self):
        self.checkLoadListVideos()
        
        video_json = self.getLastVideo()
        return self.getVideoMaxResThumbURL(video_json)
    
    def getVideoMaxResThumbURLByID(self, video_id):
        
        return f'https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg'