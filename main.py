import sqlalchemy
import sqlalchemy as sa
import psycopg2
import requests
from pprint import pprint

from sqlalchemy.orm import sessionmaker

from models import create_tables, Candidates, Photos, Flag, VK

DSN = open("dsn").read()

engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

from urllib.parse import urlencode
#
# Oauth_Base_url = 'https://oauth.vk.com/authorize'
# params = {'client_id': '51780516', 'redirect_uri': 'https://oauth.vk.com/blank.html', 'display': 'page', 'scope': 65536, 'response_type': 'token', 'v':'5.131', 'state': '123456'}
# auth_url = f'{Oauth_Base_url}?{urlencode(params)}'
# print(auth_url)


access_token = open("token").read()
user_id = 'id815147892'
vk = VK(access_token, user_id)
print(vk.users_info())
hometown = 'Москва'
gender = 2
age = 35
pprint(vk.get_candidates(hometown, gender, age))
