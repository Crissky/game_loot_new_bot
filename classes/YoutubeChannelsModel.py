class YoutubeChannelsModel():
    def __init__(self, channel_id, channel_name):
        self.data = dict()
        self.data['_id'] = channel_id
        self.data['name'] = channel_name
        self.data['video_ids'] = list()