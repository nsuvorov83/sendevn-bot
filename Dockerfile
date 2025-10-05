FROM python:3.12

ADD ./src/sendevn-bot.py /
ADD ./src/globals.py /
ADD ./src/email_utils.py /
ADD ./src/utils.py /
RUN pip install pyTelegramBotAPI
CMD python sendevn-bot.py