from selenium import webdriver
from bs4 import BeautifulSoup


class Pinterester:
    def __init__(self):
        opt = webdriver.ChromeOptions()
        opt.add_argument('--incognito')
        opt.add_argument('--headless')

        self.__driver = webdriver.Chrome(options=opt)
        self.url = "https://ru.pinterest.com/search/pins/?q="

    def search(self, search_request) -> list[str]:
        self.__driver.get(self.url + search_request)
        soup = BeautifulSoup(self.__driver.page_source, 'html.parser')
        search_result = []
        for link in soup.find_all('img'):
            search_result.append(link.get('src').replace('236x', 'originals'))

        return search_result
