#!/usr/bin/env python3
import sqlite3
import requests


class CredentialsTable:
    def __init__(self, db_name: str):
        self.__conn = sqlite3.connect(db_name)
        self.__cursor = self.__conn.cursor()
        self.__create_table()

    def __create_table(self):
        self.__cursor.execute("""CREATE TABLE IF NOT EXISTS credentials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cred_name TEXT NOT NULL,
            cred_value TEXT NOT NULL,
            _data INTEGER NOT NULL DEFAULT (DATETIME('now', 'localtime'))
        )""")
        self.__conn.commit()

    def insert_cred(self, cred_name: str, cred_value: str):
        self.__cursor.execute("INSERT INTO credentials (cred_name, cred_value) VALUES (?, ?)", (cred_name, cred_value))
        self.__conn.commit()

    def get_last_created_cred(self, cred_name: str):
        self.__cursor.execute("SELECT cred_value FROM credentials WHERE cred_name = ? ORDER BY _data DESC LIMIT 1",
                              (cred_name,))
        return self.__cursor.fetchone()[0]


class YandexHelper:
    def __init__(self, ya_auth_token: str) -> None:
        self.__token = ya_auth_token

    def get_IAM_TOKEN(self):
        body = {"yandexPassportOauthToken": f"{self.__token}"}
        response = requests.post('https://iam.api.cloud.yandex.net/iam/v1/tokens', json=body)
        return response.json()['iamToken']


ct = CredentialsTable('credentials.db')
ct.insert_cred('IAM_TOKEN', YandexHelper(ct.get_last_created_cred('yandex_token')).get_IAM_TOKEN())
