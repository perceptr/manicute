import requests


class Translator:
    def __init__(self, iam_token: str, folder_id: str) -> None:
        self.__IAM_TOKEN = iam_token
        self.__folder_id = folder_id
        self.__target_language = 'en'

    def translate(self, text_to_translate: str) -> str:
        body = {
            "targetLanguageCode": self.__target_language,
            "texts": text_to_translate,
            "folderId": self.__folder_id,
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {0}".format(self.__IAM_TOKEN)
        }

        response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
                                 json=body,
                                 headers=headers)

        return response.json()['translations'][0]['text']
