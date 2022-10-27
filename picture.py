import random
from ImageParser import YandexImage


def get_picture_links(query):
    parser = YandexImage()
    urls_ = []
    for item in parser.search(query):
        urls_.append(item.preview.url)

    return urls_


manicure_urls = get_picture_links("маникюр без лица")
pedicure_urls = get_picture_links("педикюр")


def get_manicure_link():
    return random.choice(manicure_urls)


def get_pedicure_link():
    return random.choice(pedicure_urls)
