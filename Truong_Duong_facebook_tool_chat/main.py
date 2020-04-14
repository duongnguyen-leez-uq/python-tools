from speech_to_text import SpeechToText
import text_to_speech

import fbchat
from fbchat import ThreadType, Message

import bot_config as cfg
from bot import Bot

def reply(text_message, client, thread_id):
    if client.uid == thread_id:
        return

    mess = Message(text=text_message)
    client.send(mess, thread_id=thread_id, thread_type=ThreadType.USER)
    client.delay()

client = Bot('', '',  max_tries=1, 
                    user_agent=cfg.user_agent,
                    session_cookies=cfg.session_cookies)
client.startListening()

acc_demo = '100041985261746'
acc_trDuong = '100014187060145'
recg = SpeechToText('right shift', reply, (client, acc_trDuong,))

while 1:
    client.doOneListen()
    recg.recognize_once()                 
while 1:
    pass

#speech_to_text.recognize('space', reply, (client, '100014187060145',))

