import requests
import datetime

import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from constants import token


class BotHandler:
    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)
        self.status = requests.get(self.api_url + 'getMe')

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        print('get last update alive')
        get_result = self.get_updates()
        print(get_result)
        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result[len(get_result)]

        return last_update

    def actions(self, last_update):
        routes = ['/start', '/ensonneoldu', '/kirmizialarm']
        last_chat_name = last_update['message']['chat']['first_name']
        action = last_update['message']['text']
        if action == '/start':
            return 'start works \n /ensonneoldu \n /kirmizialarm'
        elif action == '/ensonneoldu':
            return 'hicbisiiii'
        last_resort = 'Selam  {}'.format(last_chat_name)
        return last_resort


greet_bot = BotHandler(token)


def main():
    new_offset = None

    while True:
        greet_bot.get_updates(new_offset)
        last_update = greet_bot.get_last_update()
        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        last_chat_name = last_update['message']['chat']['first_name']
        print('last update id ', last_update_id)
        message = greet_bot.actions(last_update)
        greet_bot.send_message(last_chat_id, message)
        print(last_chat_text)
        new_offset = last_update_id + 1


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
