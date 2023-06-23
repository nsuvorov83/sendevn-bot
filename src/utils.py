import shutil
import tempfile
from globals import *

def cachFile(file_info):
    #Saving a file to the cache dir and return its name
    #Getting timestamp for filename
    dt = datetime.datetime.now()
    timestamp = dt.timestamp()
    #Getting info from file
    downloaded_file = bot.download_file(file_info.file_path)
    ext = os.path.split(file_info.file_path)[1].split('.')[1]
    cached_file_name = str(timestamp) + '.' + ext
    src = tempfile.gettempdir() + os.path.sep + cached_file_name
    
    #Writting a file
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
    return src

def is_photo(message):
        return message.photo

def is_document(message):
        return message.document

def is_text(message):
    return message.text

def is_caption(message):
    return message.caption

def processText(message):
    #Process text or caption (if image or document)
    if is_text(message): return message.text
    elif is_caption(message): return message.caption

def getPhotoCached(message):
    #Returns list of photos in a message (large size)
    cached_files = []
    ff = message.photo[-1]
    #Add file (large size) to cache
    file_info = bot.get_file(ff.file_id)
    asrc = cachFile(file_info)
    cached_files.append(asrc)
    return cached_files

def getDocumentCached(message):
    #Returns list of files in a message
    cached_files = []
    ff = message.document
    #Add file to cache
    file_info = bot.get_file(ff.file_id)
    asrc = cachFile(file_info)
    cached_files.append(asrc)
    return cached_files