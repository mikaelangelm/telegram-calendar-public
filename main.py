# https://habr.com/ru/post/425151/
import os
import configparser
import sys

# Асинхронность
import asyncio
import nest_asyncio # asyncio в google.colab https://colab.research.google.com/drive/1S8sbkImyJKGMCSm9GrKx_SDvDzm1kxTC?usp=sharing#scrollTo=j7eWFVOT2Ym0
nest_asyncio.apply()

# Телетон-клиент
from telethon.sync import TelegramClient
from telethon import connection
from telethon import functions, types, sync, events
from telethon.sessions import StringSession
# классы для работы с каналами
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
# класс для работы с сообщениями
from telethon.tl.functions.messages import GetHistoryRequest
# класс для работы с чатами
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty

# Гугл.календарь
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient import discovery
import datetime

# Считываем учетные данные телеграм
config = configparser.ConfigParser()
config.read("config.ini")
# Присваиваем значения внутренним переменным
API_ID   = config['Telegram']['api_id']
API_HASH = config['Telegram']['api_hash']
username = config['Telegram']['username']
SESSION_STRING = config['Telegram']['sess_string']

# и календаря
CALENDAR_CREDENTIALS = 'client_secret.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(CALENDAR_CREDENTIALS, 'https://www.googleapis.com/auth/calendar.readonly')

# ЗАПУСК
print ("=== initialaize TelegramClient ===")
sys.stdout.flush()
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
print ("=== init. NewMessage handler ===")
sys.stdout.flush()

 
@client.on(events.NewMessage()) # chats=('chat_name') 
async def normal_handler(event):
    
    message     = event.message.to_dict()['message'].lower()
#     await event.reply('Можно. Освобожусь в 21:34')
#     if ['322155227', '415925366'].count(str(message.from_user.id)) <= 0:
#         return None
    
    msg_list = ['смотрим сегодня', 'сегодня смотрим', 'посмотрим че нить', 'посмотрим чё нибудь', 'посмотрим что-нибудь', 'что-нибудь посмотрим',
            'сегодня смотреть',
            ' смотреть?', ' смотрим?', ' смотрю?', 'будем смотреть', 'смотреть будем', 'посмотрим завтра', 'завтра посмотрим', 'response_str']
    msg_match = next((_ for _ in msg_list if message.find(_)>-1), "")
    if not msg_match:
        print ("=== new message ignored ===")#, '\n', message)
#         sys.stdout.flush()
        return None
     
    print ("=== new message processed ===", '\n', message)
    sys.stdout.flush()   
 
    message_str = message#.text.lower() # import re        len(re.findall('седня|сегодня', message))
    tzinfo  = datetime.timezone(datetime.timedelta(hours=5))
    today   = datetime.datetime.utcnow().replace(tzinfo=tzinfo)
    # https://ru.stackoverflow.com/questions/135134/Как-получить-часовой-пояс-на-python
    today  += datetime.timedelta(hours=5-today.astimezone().utcoffset() // datetime.timedelta(hours=1)) # + 5 UTC ЕКБ - <UTC сервера европы>
    
    date            = today if message_str.find('завтра') < 0 else today.combine((today + datetime.timedelta(days=1)).date(), today.min.time(), tzinfo)
    last_end        = get_last_end(date) #, descr =
    time_left_min   = (last_end - date.combine(date.date(), datetime.time(23), tzinfo)).seconds // 60

    response_str    = 'можно. ' if time_left_min > 0 else 'Не получится, поздно освобождаюсь.'
    if today == last_end and time_left_min > 0:
        response_str = f'Я {"уже" if message_str.find("завтра") < 0 else "завтра вечером"} свободен, {response_str}'   
    elif time_left_min > 0:
        if date.day > today.day or message.find('завтра') > -1:
            response_str = 'Завтра ' + response_str + 'Освобожусь в ' + last_end.strftime('%H:%M')
        else: 
            response_str = 'Сегодня ' + response_str + 'Освобожусь в ' + last_end.strftime('%H:%M')
    
#     if descr.find('response_str:') > 0:
#         response_str += '.' + descr.split("response_str:")[1].replace('</span><br><span>&nbsp;</span>', '')
    
    await event.reply(response_str)#+descr)

   

def get_last_end(date: datetime.datetime = None) -> datetime.datetime:
    tzinfo  = datetime.timezone(datetime.timedelta(hours=5))
    if date == None:
        print('date is None!')
        tzinfo  = datetime.timezone(datetime.timedelta(hours=5))
        date    = datetime.datetime.now(tz=tzinfo)
        # https://ru.stackoverflow.com/questions/135134/Как-получить-часовой-пояс-на-python 
        date  += datetime.timedelta(hours=5-date.astimezone().utcoffset() // datetime.timedelta(hours=1)) # + 5 UTC ЕКБ - <UTC сервера европы>

    timeMin     = (date - datetime.timedelta(hours=1))      .isoformat() 
    timeMax     = date.combine(date.date(), date.max.time(), tzinfo).isoformat()       
    service     = discovery.build('calendar', 'v3', credentials=credentials)
    # print(timeMin, timeMax)
    events      = service.events().list(calendarId='bgbdgd@gmail.com', 
                                        timeMin=timeMin,
                                        timeMax=timeMax,                                     
                                        singleEvents=True, 
                                        timeZone='+05:00'
                                        # orderBy='startTime'
                                        )\
        .execute()\
        .get('items', 'empty')

    end_list = []
    for i in range(len(events))[-1::-1]:
        if events[i].get('transparency', 'opaque') != 'opaque': # занят
            events.pop(i)
        else:
            end_list.append([events[i]['end']['dateTime']])#, events[i]['description']])
    end_list.sort()
#     print(timeMin, timeMax, events)
 
    if len(end_list) > 0:
        return datetime.datetime.strptime(end_list[-1][0], '%Y-%m-%dT%H:%M:%S%z')#, end_list[-1][1]  
    else:
        return date#, ""

if __name__ == '__main__':
    print ("=== starting TelegramClient ===")
    sys.stdout.flush()
    client.start()
    print ("=== TelegramClient started===")
    sys.stdout.flush()
    client.run_until_disconnected()
    print ("=== TelegramClient stopped ===")
    sys.stdout.flush()
