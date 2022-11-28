from selenium import webdriver
from selenium.webdriver.common.by import By


class NewYandexSearcher:
    def __init__(self, query: str):
        self.__query = query
        self.__url = f"https://yandex.ru/images/search?text={self.__query}"
        self.__opt = webdriver.ChromeOptions()
        self.__opt.add_argument('--incognito')
        self.__opt.add_argument('--headless')
        self.__opt.add_argument('--disable-gpu')
        self.__driver = webdriver.Chrome(options=self.__opt)

    def search(self) -> list[str]:
        res = []
        for i in range(5):
            self.__driver.get(self.__url)
            self.__driver.find_elements(By.CLASS_NAME, 'serp-item__link')[i].click()
            img_link = self.__driver.find_elements(By.CLASS_NAME, 'MMImage-Origin')[0]\
                .get_attribute('src')
            res.append(img_link)

        return res

