import json

email = r'nqdduong31415@gmail.com'
password = r'******'

user_agent = r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36'

session_cookies_file = r'bot_session.json'
stored_user_ids_file = r'bot_stored_user_ids.json'

#user_ids nà ~~
stored_user_ids = {}

with open(stored_user_ids_file, 'r', encoding='utf-8') as f:
    stored_user_ids = json.load(f)

def stored_user_ids_add(id, name):
    global stored_user_ids
    
    stored_user_ids[id] = name

    with open(stored_user_ids_file, 'w', encoding='utf-8') as f:
        json.dump(stored_user_ids, f, ensure_ascii=False)

#cookies nà ~~
session_cookies = ''

with open(session_cookies_file, 'r') as f:
    session_cookies = json.load(f)

def session_cookies_update(json_obj):
    global session_cookies_file
    
    with open(session_cookies_file, 'w') as f:
        json.dump(json_obj, f)