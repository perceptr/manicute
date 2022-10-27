FROM python:3.10

ADD . ./

RUN pip install bs4
RUN pip install requests
# RUN pip install Telebot
RUN pip install pytelegrambotapi
RUN pip install --upgrade pytelegrambotapi
RUN pip install fake_headers

CMD ["python3", "./main.py"]
