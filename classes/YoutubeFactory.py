def youtube_factory(choice='pytube'):
    youtube = None
    choice = choice.lower()

    if (choice == 'pytube'):
        from pytube import YouTube
        youtube = Youtube
    elif (choice in ['youtube-dl', 'youtubedl', 'dl']):
        youtube = FakePyTube
    else:
        raise f'ERRO: Nenhuma classe youtube foi escolhida para "{choice}"'
    
    return youtube