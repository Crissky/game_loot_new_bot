class FakePyTube:
    def __init__(self, video_url):
        from youtube_dl import YoutubeDL

        self.YDL = YoutubeDL
        ydl = self.YDL({'outtmpl': 'download/video.mp4'})

        try:
            dic = ydl.extract_info(video_url, download=False)
        except Exception as e:
            premier_error = 'Premieres in'
            is_premier_error = premier_error in e.args[0]
            
            if is_premier_error:
                self.premier(video_url)
                return None
            else: 
                raise e
                        
        self.dic = dic
        self.video_url = video_url
        self.channel_id = dic['channel_id']
        self.video_id = dic['display_id']
        self.author = dic['channel']
        self.length = dic['duration']
        self.title = dic['title']
        self.description = dic['description']
        self.str_date = dic['upload_date']
        self.streams = self
        self.__set_publish_date()
    
    
    def premier(self, video_url):
        from datetime import datetime

        self.video_url = video_url
        self.channel_id = ''
        self.video_id = ''
        self.author = ''
        self.length = 0
        self.title = ''
        self.description = ''
        self.str_date = datetime.today().strftime('%Y%m%d')
        self.streams = self
        self.__set_publish_date()


    def filter(self, *args, **kwargs):
        return self
    

    def first(self, *args, **kwargs):
        return self
    

    def download(self, output_path='download', filename='video'):
        from os import path, remove, listdir
        import shutil

        video_path = path.join(output_path, filename) + '.mp4'
        if path.exists(output_path):
            shutil.rmtree(output_path)
        ydl = self.YDL({'outtmpl': f'{video_path}',
                        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio',
                        'merge_output_format' : 'mp4'})
        ydl.download([self.video_url])

    
    def __set_publish_date(self):
        from datetime import datetime
        template_date = '%Y%m%d'
        self.publish_date = datetime.strptime(self.str_date, template_date)

    
    def __repr__(self):
        return f'''video_url: {self.video_url},
        title: {self.title},
        author: {self.author},
        length: {self.length},
        video_id: {self.video_id},
        channel_id: {self.channel_id},
        str_date: {self.str_date},
        publish_date: {self.publish_date}'''

    def __str__(self):
        return f'<title: {self.title}, resolution: {self.dic["width"]}x{self.dic["height"]}>'