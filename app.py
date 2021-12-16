import requests
import datetime
from constants import token

class BotHandler:
    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)
        print('api_url', self.api_url)
        self.status = requests.get(self.api_url + 'getMe')
        print(self.status.json())

    def get_updates(self, offset=None, timeout=30):
        print('get updates alive')
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        print(self.api_url + method, params)
        resp = requests.get(self.api_url + method, params)
        print(resp)
        result_json = resp.json()['result']
        print('printing resp.json', resp.json())
        print('Printing result_json', result_json)
        return result_json

    def send_message(self, chat_id, text):
        print('send message alive')
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


greet_bot = BotHandler(token)
greetings = ('hello', 'hi', 'greetings', 'sup')
now = datetime.datetime.now()


def main():
    new_offset = None
    today = now.day
    hour = now.hour

    while True:
        greet_bot.get_updates(new_offset)

        last_update = greet_bot.get_last_update()

        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        last_chat_name = last_update['message']['chat']['first_name']
        print('last update id ', last_update_id)

        # if last_chat_text.lower() in greetings and today == now.day and 6 <= hour < 12:
        #     greet_bot.send_message(last_chat_id, 'Good Morning  {}'.format(last_chat_name))
        #     today += 1
        #
        # elif last_chat_text.lower() in greetings and today == now.day and 12 <= hour < 17:
        #     greet_bot.send_message(last_chat_id, 'Good Afternoon {}'.format(last_chat_name))
        #     today += 1
        #
        # elif last_chat_text.lower() in greetings and today == now.day and 17 <= hour < 23:
        #     greet_bot.send_message(last_chat_id, 'Good Evening  {}'.format(last_chat_name))
        #     today += 1
        greet_bot.send_message(last_chat_id, 'Good Morning  {}'.format(last_chat_name))

        new_offset = last_update_id + 1

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()