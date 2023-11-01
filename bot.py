from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

photo = 'photo602776567_457239019'
token_bot = open("token2").read()
vk_session = vk_api.VkApi(token=token_bot)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)


# Отправка текста
def text(id, text):
    button = open('keyboard_first.json', encoding='utf-8').read()
    vk.messages.send(user_id=id, message=text, keyboard=button, random_id=randrange(10 ** 7))


# Отправка фото
def url(id, url):
    vk.messages.send(user_id=id, attachment=url, random_id=randrange(10 ** 7))


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:

            request = event.text.lower()
            user_id = event.user_id

            # Используем первую функцию:
            if request == 'привет':
                result = vk.users.get(user_ids=event.user_id, fields='screen_name')
                text(user_id, f'Приввет {result[0]["first_name"]}')
            # Первая функция + вторая
            elif request == 'как':
                text(user_id, 'Вот так')
                url(user_id, photo)
            else:
                print('[ + ]')