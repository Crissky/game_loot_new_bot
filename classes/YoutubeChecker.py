class YoutubeChecker():
    def __init__(self, YOUTUBE_API_KEY):
        self.API_KEY = YOUTUBE_API_KEY
        self.base_url = "https://www.googleapis.com/youtube/v3/search?key={API_YT}&channelId={CHANNEL_ID}&part=snippet,id&order=date&maxResults={MAX_RESULTS}"
        self.base_video_url = "https://www.youtube.com/watch?v={videoId}"

    def getURL(self, channel_id, max_results=1):
    
        return self.base_url.format(API_YT=self.API_KEY, CHANNEL_ID=channel_id, MAX_RESULTS=max_results)
    
    def loadListVideos(self, channel_id, max_results=5):
        import requests
        self.last_url = self.getURL(channel_id, max_results)
        response = requests.get(self.last_url)
        self.list_videos_json = response.json()

        return self

    def getVideoURL(self, video_id):
    
        return self.base_video_url.format(videoId=video_id)
    
    def getLastVideoURL(self):
        if(not self.list_videos_json):
            raise "Use a função 'loadListVideos()' antes desse método"
        
        video_id = self.getLastVideoID()
        return self.getVideoURL(video_id)
    
    def getVideoList(self):
        if(not self.list_videos_json):
            raise "Use a função 'loadListVideos()' antes desse método"

        return self.list_videos_json['items']
    
    def getLastVideo(self):
        if(not self.list_videos_json):
            raise "Use a função 'loadListVideos()' antes desse método"
        
        return self.list_videos_json['items'][0]

    def getVideoID(self, video_json):
        return video_json['id']['videoId']
    
    def getLastVideoID(self):
        if(not self.list_videos_json):
            raise "Use a função 'loadListVideos()' antes desse método"
        
        video_json = self.getLastVideo()
        return self.getVideoID(video_json)
    
    def getVideoTitle(self, video_json):
        return video_json['snippet']['title']
    
    def getLastVideoTitle(self):
        if(not self.list_videos_json):
            raise "Use a função 'loadListVideos()' antes desse método"
        
        video_json = self.getLastVideo()
        return self.getVideoTitle(video_json)
    
    def getVideoChannelTitle(self, video_json):
        return video_json['snippet']['channelTitle']
    
    def getLastVideoChannelTitle(self):
        if(not self.list_videos_json):
            raise "Use a função 'loadListVideos()' antes desse método"
        
        video_json = self.getLastVideo()
        return self.getVideoChannelTitle(video_json)
    
    def getVideoDescription(self, video_json):
        return video_json['snippet']['description']
    
    def getLastVideoDescription(self):
        if(not self.list_videos_json):
            raise "Use a função 'loadListVideos()' antes desse método"
        
        video_json = self.getLastVideo()
        return self.getVideoDescription(video_json)
    
    def getVideoHighThumbURL(self, video_json):
        return video_json['snippet']['thumbnails']['high']['url']
    
    def getLastVideoHighThumbURL(self):
        if(not self.list_videos_json):
            raise "Use a função 'loadListVideos()' antes desse método"
        
        video_json = self.getLastVideo()
        return self.getVideoHighThumbURL(video_json)
    
    def getVideoMaxResThumbURL(self, video_json):
        thumb_url = self.getVideoHighThumbURL(video_json)
        thumb_url = thumb_url.replace('hqdefault','maxresdefault')

        return thumb_url
    
    def getLastVideoMaxResThumbURL(self):
        if(not self.list_videos_json):
            raise "Use a função 'loadListVideos()' antes desse método"
        
        video_json = self.getLastVideo()
        return self.getVideoMaxResThumbURL(video_json)