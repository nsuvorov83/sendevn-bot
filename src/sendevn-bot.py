from globals import *
from utils import *
from email_utils import *


#Change type if OWNER_ID is str
try:
    CFG_OWNER_ID = int(os.environ.get('CFG_OWNER_ID')) #YOUR_USER_ID_IN_TELEGRAM
except:
    CFG_OWNER_ID = os.environ.get('CFG_OWNER_ID')



@bot.message_handler(content_types=['text', 'audio', 'document', 'photo', 'video'])
def get_messages(message):
    #Checking whether it's owner of the bot
    if message.from_user.id == CFG_OWNER_ID:
        try:
            do_next(message)
        except Exception as err:
            #Exceptions processing with sending text of an error
            bot.send_message(message.from_user.id, f"Произошла ошибка: {str(err)}")
    else: 
        pass

def do_next(message):
    txt = ''

    if is_text(message) or is_caption(message):
        #Text handler
        txt = processText(message)

    #Ping
    if(txt == 'ping'):
        bot.send_message(message.from_user.id, "pong")
        return 0
    
    #Dev Credentials input
    if(txt == '/creds'):
        bot.send_message(message.from_user.id, "Change credentials")
        return 0

    #Dev Stop server
    if(txt == 'stopserver'):
        bot.send_message(message.from_user.id, "Stopping server...")
        raise SystemExit

    send_email(message, txt)

    bot.send_message(message.from_user.id, "Заметка отправлена в Obsidian")

#Running the bot
bot.polling(True, 0)