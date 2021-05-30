# GERENCIA A POSTAGEM DE VÍDEOS NO TWITTER
class YoutubeToTwitter():
    def __init__(self, mongo_connector, youtube_handler, twitter_connector):
        self.mongo_conn = mongo_connector.setDatabase().setCollection()
        self.yt_handler = youtube_handler
        self.twitter = twitter_connector
    
    # RETORNA UMA LISTA COM OS ELEMENTOS DA "list1" QUE NÃO EXISTEM NA "list2"
    def filterNotMatches(self, list1, list2):
        return list(set(list1) - set(list2))

    # RETORNA UM DICIONÁRIO ONDE AS CHAVES SÃO OS IDs DOS CANAIS
    # E O VALOR É UMA LISTA COM OS IDs DOS VÍDEOS ÚLTIMOS QUE AINDA NÃO FORAM ANALISADOS (QUE ESTÃO ARMAZENADOS DO BANCO DE DADOS)
    # "size_list" DEFINE QUANTOS ELEMENTOS SERÃO PESQUISADOS NA API DO GOOGLES
    # (A API PODE RETORNAR VÍDEOS OS PLAYLISTS, ONDE AS PLAYLISTS SERÃO DESCARTADAS — AFETANDO O TOTAL DE VÍDEOS RETORNADOS)
    def getAllUnsendVideos(self, size_list=5):
        dict_unsend = dict()
        for document in self.mongo_conn.getAllDocuments():
            print(f"{document['name']} ({document['_id']})", end=': ')

            channel_unsend_vids = self.getChannelUnsendVideos(document, size_list)
            dict_unsend.update(channel_unsend_vids)
            not_matches_list = channel_unsend_vids[document['_id']]

            print( len(not_matches_list), not_matches_list )
        
        return dict_unsend
    
    # RETORNA UM DICIONÁRIO COM O ID DO CANAIS E OS IDs DOS VÍDEOS ÚLTIMOS QUE AINDA NÃO FORAM ANALISADOS
    # MAIS DETALHES EM "getAllUnsendVideos()"
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

        # print("youtube_channel_ids:\n", '\n'.join(youtube_channel_ids))

        for channel_id in youtube_channel_ids:
            document = self.mongo_conn.getDocumentByID(channel_id)
            if document:
                print(f"Canal {document['name']} já existe no banco de dados com o ID: {document['_id']}.")
                continue

            self.yt_handler.loadListVideos(channel_id, 50)
            video_url = self.yt_handler.getLastVideoURL()
            try:
                youtube = YouTube(video_url)
                channel_name = youtube.author

                yt_channel_model = YoutubeChannelsModel(channel_id, channel_name)
                self.mongo_conn.collection.insert_one(yt_channel_model.data)
            except Exception as e:
                print('O canal de id:', channel_id, "Não pode ser atualizado com a URL:", video_url)
                print('Motivo:', e)
    
    # ESCOLHE SE O VÍDEO SERÁ ENVIADO PARA O TWITTER
    # VÍDEO MAIS ANTIGO QUE O (HOJE MENOS O "limit_date") NÃO SERÁ ENVIADO
    # VÍDEO COM MINUTAGEM MAIOR QUE ("video_length" > 300) TAMBÉM NÃO SERÁ ENVIADO
    # VÍDEO COM MINUTAGEM ENTRE ( "video_length" >= 140 and "video_length" <= 300 ) SERÁ ENVIADO COM CORTE DE 2 MINUTOS FEITO NO MEIO DO VÍDEO
    # VÍDEO COM MENOS DE 2 MINUTOS E 20 SEGUDOS SERÁ ENVIADO COMPLETO
    # AO FIM DA ESCOLHA, O ID DO VÍDEO É ADICIONADO NO BANCO DE DADOS NA LISTA DO SEU RESPECTIVO CANAL
    def sendTwitterChooser(self, channel_id, video_id):
        from pytube import YouTube
        from datetime import datetime, timedelta

        video_url = self.yt_handler.getVideoURL(video_id)
        youtube = YouTube(video_url)
        video_date = youtube.publish_date.date()
        limit_date = datetime.today() - timedelta(days=2)
        video_length = youtube.length
        video_author = youtube.author

        is_sending = False
        if ( video_date < limit_date.date() ):
            print(f'\t{video_author}: Vídeo {video_url} é muito ANTIGO: {video_date}.')
        elif ( video_length >= 140 and video_length <= 300 ):
            # print(f'\t{video_author}: Vídeo {video_url} é meio LONGO: {video_length} segundos. Enviando somente o link.')
            # self.sendMedia(channel_id, video_id, video_author, video_url, youtube, 'image')
            print(f'\t{video_author}: Vídeo {video_url} é meio LONGO: {video_length} segundos. Enviando vídeo cortado.')
            self.sendMedia(channel_id, video_id, video_author, video_url, youtube, 'cutted')
            is_sending = True
        elif ( video_length > 300 ):
            print(f'\t{video_author}: Vídeo {video_url} é muito LONGO: {video_length} segundos.')
        else:
            print(f'\t{video_author}: Vídeo {video_url} Enviando!')
            self.sendMedia(channel_id, video_id, video_author, video_url, youtube, 'video')
            is_sending = True

        self.updateVideoIDs(channel_id, video_id)

        return is_sending

    # ADICIONA O ID DO VÍDEO NO BANCO DE DADOS NA LISTA DO SEU RESPECTIVO CANAL
    def updateVideoIDs(self, channel_id, video_id):
        document = self.mongo_conn.getDocumentByID(channel_id)
        
        yt_channel_model = YoutubeChannelsModel(**document)
        yt_channel_model.addVideoID(video_id)
        yt_channel_model.updateDocumentVideoIDs(mongo_connector.collection)

    # ENVIA UMA IMAGEM PARA O TWITTER
    def sendImage(self, channel_id, video_id, video_author, video_url, youtube):
        image_path = self.saveImage(video_id)
        media_id = self.loadMedia(image_path)
        message = f'Vídeo {video_author}:\n{youtube.title}.'
        message += f'\n\nLink: {video_url}'
        
        self.updateStatus(message, media_id)

    # ENVIA UM VÍDEO PARA O TWITTER
    def sendVideo(self, channel_id, video_id, video_author, video_url, youtube):
        video_path = self.saveVideo(youtube)
        media_id = self.loadMedia(video_path)
        message = f'Vídeo {video_author}:\n{youtube.title}.'
        message += f'\n\nLink: {video_url}'

        self.updateStatus(message, media_id)

    # SALVA LOCALMENTE UMA MÍDIA (THUMBNAIL OU VÍDEO) DO YOUTUBE COM BASE NO "media_type" PASSADO
    # SE O "media_type" FOR DIFERENTE DE  "image" OU "video", O VÍDEO SERÁ CORTADO PARA 2 MINUTOS
    def sendMedia(self, channel_id, video_id, video_author, video_url, youtube, media_type='cutted'):
        from time import sleep

        if (media_type.lower() == 'video'):
            media_path = self.saveVideo(youtube)
        elif (media_type.lower() == 'image'):
            media_path = self.saveImage(youtube)
        else:
            media_path = self.saveCuttedVideo(youtube)

        media_id = self.loadMedia(media_path)
        message = f'Vídeo {video_author}:\n{youtube.title}.'
        message += f'\n\nLink: {video_url}'
        
        sleep(2)
        
        self.updateStatus(message, media_id)

    # SALVA UMA IMAGEM LOCALMENTE
    def saveImage(self, video_id):
        import requests
        image_url = self.yt_handler.getVideoMaxResThumbURLByID(video_id)
        image_path = 'download/image.jpg'
        response = requests.get(image_url)
        
        with open(image_path, 'wb') as file:
            file.write(response.content)
        
        return image_path

    # SALVA UM VÍDEO LOCALMENTE
    def saveVideo(self, youtube):
        video = youtube.streams.filter(mime_type='video/mp4',
                               custom_filter_functions=[lambda s: (s.resolution == '720p') or (s.resolution == '480p')])\
                               .first()

        print('\tBaixando vídeo: ', video)
        video.download(output_path='download', filename='video')

        return 'download/video.mp4'
    
    # SALVA UM VÍDEO LOCALMENTE, MAS ELE E CORTADO EM 2 MINUTOS (PARTE CENTRAL DO VÍDEO)
    def saveCuttedVideo(self, youtube):
        print('\tCortando vídeo...')
        from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
        video_path = self.saveVideo(youtube)
        cutted_video_path = 'download/cutted.mp4'
        mid_time = (youtube.length) // 2
        start_time = mid_time - 60
        end_time = mid_time + 60
        
        ffmpeg_extract_subclip(video_path, start_time, end_time, targetname=cutted_video_path)

        return cutted_video_path

    # CARREGA UMA MÍDIA (IMAGEM OU VÍDEO) NO TWITTER
    # RETORNA O ID DA MÍDIA CARREGADA
    def loadMedia(self, file_path):
        with open(file_path, 'rb') as file:
            if ('video.mp4' in file_path or 'cutted.mp4' in file_path):
                response = self.twitter.upload_video(media=file, media_type='video/mp4', media_category='tweet_video', check_progress=True)
            else:
                response = self.twitter.upload_media(media=file)
        
        media_id = [response['media_id']]

        return media_id
    
    # ENVIA UM POST NO TWITTER
    # "media_id" É O ID DA MÍDIA CARREGADA PELO "loadMedia()"
    def updateStatus(self, message, media_id):
        self.twitter.update_status(status=message, media_ids=media_id)

    # RETORNA O DICIONÁRIO ONDE AS CHAVES SÃO OS IDs DOS CANAIS
    # E OS VALORES SÃO LISTAS COM DOS IDs DOS VÍDEOS QUE SERÃO USADOS PELO "sendTwitterChooser()"
    # ESSE DICIONÁRIO É USADO PARA QUE O "startSend()" POSSA CONTINUAR O
    # ENVIO DOS VÍDEOS CASO ACONTEÇA ALGUM ERRO DURANTE A EXECUÇÃO — ISSO ECONOMIZA CONSULTAS NA API DO GOOGLE
    def getInWork(self):
        self.mongo_conn.setCollection('inWork')
        unsend_dict = self.mongo_conn.collection.find_one()
        if unsend_dict:
            unsend_dict.pop('_id')

        self.mongo_conn.setCollection()
        
        return unsend_dict
    
    # SALVA O PROGRESSO DO "startSend()" NA COLEÇÃO 'inWork'
    # MAIS DETALHES EM "getInWork()"
    def saveInWork(self, unsend_dict):
        self.mongo_conn.setCollection('inWork')
        self.mongo_conn.dropCollection()
        self.mongo_conn.collection.insert_one(unsend_dict)
        self.mongo_conn.setCollection()
    
    # EXCLUI A COLEÇÃO 'inWork'
    # MAIS DETALHES EM "getInWork()"
    def dropInWork(self):
        self.mongo_conn.setCollection('inWork')
        self.mongo_conn.dropCollection()
        self.mongo_conn.setCollection()
    
    # GERENCIA O ENVIO DE VÍDEOS PARA O TWITTER
    # A CONSULTA É FEITA PRIMEIRAMENTE NO MONGODB NA COLEÇÃO 'inWork'
    # CASO NÃO EXISTA VIDEOS PARA SER ENVIADO NO 'inWork'
    # OS VÍDEOS SERÃO BUSCADOS NA API DO GOOGLE
    def startSend(self, size_list=5, document=None):
        from time import sleep
        from copy import deepcopy

        unsend_dict = self.getInWork()
        if document:
            unsend_dict = document
        elif unsend_dict:
            print(f"Continuando Trabalho inacabado...\n{unsend_dict}")
        else:
            print('startSend() -> getAllUnsendVideos() — VÍDEOS NOVOS:')
            unsend_dict = self.getAllUnsendVideos(size_list)
        
        unsend_dict_copy = deepcopy(unsend_dict)

        print('\nstartSend() -> sendTwitterChooser()')
        for key, value in unsend_dict.items():
            print(key, value)
            for video_id in value:
                is_spleep = self.sendTwitterChooser(key, video_id)
                if (is_spleep):
                    print('\tDormindo...')
                    sleep(300)
                else:
                    sleep(5)
                
                unsend_dict_copy[key].remove(video_id)
                self.saveInWork(unsend_dict_copy)
            print()
        self.dropInWork()
        print("\n startSend() Terminou!!!")