import sqlalchemy
import sqlalchemy as sa
import psycopg2
import requests
from pprint import pprint

from sqlalchemy.orm import sessionmaker

from models import create_tables, Candidates, Photos, Flag, VK, VK_Client

DSN = open("dsn").read()

engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

from urllib.parse import urlencode
# Получение токена для поиска кандидатов вVK
# Oauth_Base_url = 'https://oauth.vk.com/authorize'
# params = {'client_id': '51780516', 'redirect_uri': 'https://oauth.vk.com/blank.html', 'display': 'page', 'scope': 65536, 'response_type': 'token', 'v':'5.131', 'state': '123456'}
# auth_url = f'{Oauth_Base_url}?{urlencode(params)}'
# print(auth_url)


access_token = open("token").read()
#user_id = 'id815147892'
user_id = 'id340257056'
vk = VK(access_token, user_id)
cl_info = vk.users_info()
# print(cl_info)
town = cl_info['response'][0]['city']['id']
# print(town)
sex = cl_info['response'][0]['sex']
if sex == 2:
    gender = 1
else:
    gender = 2
# print(gender)
sp = cl_info['response'][0]['bdate'].split('.')
# print(sp)
age = 2023 - int(sp[2])
# print(age)
#hometown = 'Москва'
# city = 1
# gender = 2
# age = 35
data_for_db = vk.get_candidates(town, gender, age)['response']['items']
#pprint(data_for_db)
Session = sessionmaker(bind=engine)
session = Session()
for el in data_for_db:
    el.setdefault('city', {'id': None, 'title': ''})
    el.setdefault('bdate', '')
pprint(data_for_db)
for el in data_for_db:
    #print(f"https://vk.com/id{el['id']}")
    #print(el['city']['title'])
    cand = Candidates(name=el['first_name'], fam_name=el['last_name'], city=el['city']['title'], age=(2023-int(el['bdate'].split('.')[2])), gender=el['sex'], vk_id=el['id'], vk_url=f"https://vk.com/id{el['id']}")
    session.add(cand)
session.commit()


# Получение токена для фотографий
# Oauth_Base_url = 'https://oauth.vk.com/authorize'
# params = {'client_id': '51722110', 'redirect_uri': 'https://oauth.vk.com/blank.html', 'display': 'page', 'scope': 'photos', 'response_type': 'token', 'v':'5.131', 'state': '123456'}
# auth_url = f'{Oauth_Base_url}?{urlencode(params)}'
# print(auth_url)
token1 = open('token1').read()
for el in data_for_db:
    vk_klient = VK_Client(token1, el['id'])
    try:
        dict = vk_klient.get_photos()['response']['items']
        # pprint(dict)
    # except: KeyError:
    except Exception as e:
        print(e)
    dict2={}
    for elem in dict:
        a=elem['likes']['count']
        dict2[a] = elem['sizes'][1]['url']
    sp_photos = sorted(dict2.items(), reverse=True)
    # pprint(sp_photos)
    if len(sp_photos)>=3:
        photo = Photos(candidate_id=el['id'], photo_url=sp_photos[0][1])
        session.add(photo)
        photo = Photos(candidate_id=el['id'], photo_url=sp_photos[1][1])
        session.add(photo)
        photo = Photos(candidate_id=el['id'], photo_url=sp_photos[2][1])
        session.add(photo)
    elif len(sp_photos)==2:
        photo = Photos(candidate_id=el['id'], photo_url=sp_photos[0][1])
        session.add(photo)
        photo = Photos(candidate_id=el['id'], photo_url=sp_photos[1][1])
        session.add(photo)
    elif len(sp_photos)==1:
        photo = Photos(candidate_id=el['id'], photo_url=sp_photos[0][1])
        session.add(photo)

session.commit()
session.close()