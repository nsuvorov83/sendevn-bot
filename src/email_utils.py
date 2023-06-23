from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
import smtplib
import textwrap

from globals import *
from utils import *

def send_email(message, txt):
    #Sening a message to outlook
    ##Check if Subject is too long
    msg = MIMEMultipart()
    txt_subject = ''

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


    if is_photo(message):
        #Photo handler
        cached_files = getPhotoCached(message)
        #Insert into e-mail
        for f in cached_files:
            with open(f, 'rb') as file:
                filename = os.path.basename(f)
                att = MIMEImage(file.read())
                att.add_header('Content-Disposition','attachment; filename="%s"' % filename)
                msg.attach(att)

    if is_document(message):
        #Doc handler
        cached_files = getDocumentCached(message)
        #Insert into e-mail
        for f in cached_files:
            with open(f, 'rb') as file:
                filename = os.path.basename(f)
                att = MIMEApplication(file.read())
                att.add_header('Content-Disposition','attachment; filename="%s"' % filename)
                msg.attach(att)

    #Add ready data to MIME object
    msg['From'] = CFG_SMTP_FROM
    msg['To'] = CFG_SMTP_TO
    msg['Subject'] = f'{txt_subject}'
    msg_full = msg.as_string()

    server = smtplib.SMTP_SSL('smtp.yandex.ru:465')
    server.login(CFG_SMTP_LOGIN, CFG_SMTP_PASS)
    server.sendmail(CFG_SMTP_FROM, CFG_SMTP_TO, msg_full) 

    server.quit()