import speech_to_text
import text_to_speech

import fbchat
from fbchat import ThreadType, log

import time
from enum import Enum

import bot_config as cfg

class Bot(fbchat.Client):
    def get_name_by_user_id(self, user_id):
        if user_id in cfg.stored_user_ids:
            return cfg.stored_user_ids[user_id]
        else:
            info = self.fetchUserInfo(user_id)
            name = info[user_id].name

            cfg.stored_user_ids_add(user_id, name)

            log.info('added: name: {}; id: {}'.format(name, user_id))
            self.delay()
            return name
        
    def onMessage(self, mid=None, author_id=None, message=None, message_object=None, 
                    thread_id=None, thread_type=ThreadType.USER, 
                    ts=None, metadata=None, msg=None):
        # igrone your own message
        if (author_id == self.uid):
            return

        self.markAsDelivered(thread_id, message_object.uid)
        self.delay()

        self.markAsRead(thread_id)
        self.delay()
        #handle
        name = self.get_name_by_user_id(author_id)
        text = message_object.text

        log.info('{}: {}'.format(name, text))

        text_to_speech.say(name + ' nói ' + text)

    def delay(self, time_in_second = 0.3):
        time.sleep(time_in_second)

if __name__ == "__main__":
    pass