import requests


class TwitterToTelegram:

    def __init__(self, token, channel_id):
        self.__token = token
        self.__channel_id = channel_id
        self.__url = 'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}'

    def send_message(self, message):
        url = self.__url.format(
            token=self.__token,
            chat_id=self.__channel_id,
            message=message
        )
        print(requests.get(url).json())
