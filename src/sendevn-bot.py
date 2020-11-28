import os
import telebot
import smtplib
import textwrap
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import datetime
import json


#Configuration
CFG_TOKEN = os.environ.get('CFG_TOKEN') #TELEGRAM_BOT_TOKEN
CFG_SMTP_LOGIN = os.environ.get('CFG_SMTP_LOGIN') #'%YOUR_SMTP_LOGIN_ON_YANDEX%'
CFG_SMTP_PASS = os.environ.get('CFG_SMTP_PASS') #'%YOUR_SMTP_PASS_ON_YANDEX%'
CFG_SMTP_FROM = os.environ.get('CFG_SMTP_FROM') #'%FROM_EMAIL_ADDRESS%'
CFG_SMTP_TO = os.environ.get('CFG_SMTP_TO') #'%TO_EMAIL_EVERNOTE_ADDRESS%'

#Common variables
d = datetime.date.today()
now = datetime.datetime.now()

#Change type if OWNER_ID is str
try:
    CFG_OWNER_ID = int(os.environ.get('CFG_OWNER_ID')) #YOUR_USER_ID_IN_TELEGRAM
except:
    CFG_OWNER_ID = os.environ.get('CFG_OWNER_ID')

#https://github.com/eternnoir/pyTelegramBotAPI
bot = telebot.TeleBot(CFG_TOKEN)

@bot.message_handler(content_types=['text', 'audio', 'document', 'photo', 'video'])
def get_text_messages(message):
    #Checking whether it's owner of the bot
    if message.from_user.id == CFG_OWNER_ID:
        do_next(message)
    else: 
        pass

def cachFile(file_info):
    #Saving a file to the cache dir and return its name
    #Getting timestamp for filename
    dt = datetime.datetime.now()
    timestamp = dt.timestamp()
    #Getting info from file
    downloaded_file = bot.download_file(file_info.file_path)
    ext = os.path.split(file_info.file_path)[1].split('.')[1]
    cached_file_name = str(timestamp) + '.' + ext
    src = os.getcwd() + os.path.sep + 'cache' + os.path.sep + cached_file_name
    #Writting a file
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
    return src

def _is_photo(message):
        return message.photo

def _is_text(message):
    return message.text

def processText(message):
    return message.text

def getPhotoCached(message):
    #Returns list of photos in a message (large size)
    cached_files = []
    ff = message.photo[2]

    #Add file (large size) to cache
    file_info = bot.get_file(ff.file_id)
    asrc = cachFile(file_info)
    cached_files.append(asrc)
    return cached_files

def do_next(message):

    txt = ''
    txt_subject = ''

    if _is_text(message):
        #Text handler
        txt = processText(message)

    #Ping
    if(txt == 'ping'):
        bot.send_message(message.from_user.id, "pong")
        return 0
    
    #Sening a message to outlook
    ##Check if Subject is too long
    msg = MIMEMultipart()

    if len(txt) > 30:
        txt_subject = textwrap.shorten(txt, width=30, placeholder="...")
    elif len(txt) == 0:
        txt_subject = 'Из Telegram ' + str(now)
    else:
        txt_subject = txt
    
    msg.attach(MIMEText(txt))
    
    
    #Check whether forwarded from another user
    if "forward_sender_name" in message.json:
        txt = f'{txt}'
    elif "forward_from" in message.json:
        txt = f'{txt}'

    if _is_photo(message):
        #Photo handler
        cached_files = getPhotoCached(message)
        #Insert into e-mail
        for f in cached_files:
            with open(f, 'rb') as image_file:
                msg.attach(MIMEImage(image_file.read()))
        #TODO Deleting cached files

    #Add ready data to MIME object
    msg['From'] = CFG_SMTP_FROM
    msg['To'] = CFG_SMTP_TO
    msg['Subject'] = f'{txt_subject} #{d.year}'
    msg_full = msg.as_string()

    try:
        server = smtplib.SMTP_SSL('smtp.yandex.ru:465')
        server.login(CFG_SMTP_LOGIN, CFG_SMTP_PASS)
        server.sendmail(CFG_SMTP_FROM, CFG_SMTP_TO, msg_full) 
        bot.send_message(message.from_user.id, "Задача отправлена в Evernote")
        server.quit()
    except Exception as err:
        #Exceptions processing with sending text of an error
        bot.send_message(message.from_user.id, f"При отправке сообщения произошла ошибка: {str(err)}")

#Running the bot
bot.polling(True, 0)