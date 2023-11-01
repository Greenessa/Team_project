from pprint import pprint
from urllib.parse import urlencode
from vk_api.keyboard import VkKeyboard, VkKeyboardColor, MAX_BUTTONS_ON_LINE, VkKeyboardButton
import requests
from vk_api.utils import sjson_dumps

from Team_project.main import search

token_bot = open("token2").read()

id_bot = 223245358

from random import randrange
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

vk = vk_api.VkApi(token=token_bot)
longpoll = VkBotLongPoll(vk, id_bot)


def write_msg(user_id, message):
    button = open('keyboard_first.json').read() # это кнопка, для отправки в сообщении
    vk.method('messages.send', # вид метода
              {'user_id': user_id, # идентификатор пользователя, без него отправить сообщение не возможно
               'message': message, # само сообщение
               'keyboard': button, # это кнопки, передается в формате json, его тоже отправлю на гит
               'random_id': randrange(10 ** 7), }) # это уникальность сообщения, для защиты , что бы много сообщений не было


for event in longpoll.listen(): # прослушиваем чат
    if event.type == VkBotEventType.MESSAGE_NEW: # ожидаем нового сообщения
        request = event.message['text'] # забираем текст сообщения
        if request == "привет":
            result = vk.method('users.get', # получаем информацию о пользователе
                               {
                                   'user_ids': event.message['from_id'],
                                   'fields': 'screen_name',
                               })
            write_msg(event.message['from_id'], f"Хай, {result[0]['first_name']} {result[0]['last_name']}") # отправка сообщения
        elif request == "пока":
            write_msg(event.message['from_id'], "Пока((")
        elif request == 'Найти пару':
            write_msg(event.message['from_id'], f"Ищу")
            # а вот здесь должен быть наш код))
        else:
            write_msg(event.message['from_id'], "Не поняла вашего ответа...")

