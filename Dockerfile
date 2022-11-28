FROM python:3.10

ADD . ./

RUN pip install requests
# RUN pip install Telebot
RUN pip install psycopg2-binary
RUN pip install pytelegrambotapi
RUN pip install --upgrade pytelegrambotapi
RUN pip install fake_headers
RUN pip install aiogram
RUN pip install selenium
RUN pip install beautifulsoup4
RUN pip install bs4

CMD ["python3", "./main.py"]
