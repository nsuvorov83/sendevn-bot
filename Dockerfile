FROM python:3.7

ADD ./src/sendevn-bot.py /
RUN pip install pyTelegramBotAPI
CMD python sendevn-bot.py