import random
from ImageParser import YandexImage


class YandexImageGetter:
    def __init__(self, query: str) -> None:
        self.__parser = YandexImage()
        self.__urls_ = []
        for _ in range(10):
            self.__urls_.append(self.__parser.search(query)[0].url)
        # for item in self.__parser.search(query):
        #     self.__urls_.append(item.preview.url)

    def search(self) -> list[str]:
        tmp_res = []
        try:
            for _ in range(5):
                tmp_res.append(random.choice(self.__urls_))
            return tmp_res
        except IndexError:
            raise IndexError("No images found")
