from datetime import datetime

class FakePyTube:
    def __init__(self, video_url):
        #from youtube_dl import YoutubeDL
        from yt_dlp import YoutubeDL

        self.YDL = YoutubeDL
        ydl = self.YDL({
            'outtmpl': 'download/video.mp4',
            'cookiefile': 'cookies.txt'
        })

        try:
            dic = ydl.extract_info(video_url, download=False)
        except Exception as e:
            premier_errors = [
                              'Premieres in',
                              'ERROR: This live event will begin in',
                              'ERROR: Este evento ao vivo começará em',
                              'Estreia em',
                              'Este evento ao vivo começará em',
                              'This live event will begin in',
                              'Vídeo indisponível.',
                              'A gravação dessa transmissão ao vivo'
                              ' não está disponível.',

            ]
            is_premier_error = any(
                [(text_error in e.args[0]) for text_error in premier_errors]
            )
            
            if is_premier_error:
                self.premier(video_url)
                return None
            else: 
                raise e
                        
        self.dic = dic
        self.video_url = video_url
        self.channel_id = dic.get('channel_id', '')
        self.video_id = dic.get('display_id', '')
        self.author = dic.get('channel', '')
        self.length = dic.get('duration', 0)
        self.title = dic.get('title', '')
        self.description = dic.get('description', '')
        self.str_date = dic.get('upload_date', datetime.today().strftime('%Y%m%d'))
        self.streams = self
        self.__set_publish_date()
    
    
    def premier(self, video_url):
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
        ydl = self.YDL({
            'outtmpl': f'{video_path}',
            # 'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio',
            'format': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=1080]+bestaudio',
            'merge_output_format' : 'mp4',
            'cookiefile': 'cookies.txt'
        })
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