import requests
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Candidates(Base):
    __tablename__ = "candidates"
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(40), index=True)
    fam_name: so.Mapped[str] = so.mapped_column(sa.String(40), index=True)
    city: so.Mapped[str] = so.mapped_column(sa.String(40), index=True)
    age: so.Mapped[int]
    gender: so.Mapped[str] = so.mapped_column(sa.String(10), index=True)
    vk_url: so.Mapped[str] = so.mapped_column(sa.String(200), index=True, unique=True, nullable=False)

    def __str__(self):
        return f"{self.id}: {self.name} {self.fam_name} {self.city} {self.age} {self.gender} {self.vk_url}"
    # homeworks = relationship("Homework", back_populates="course")

class Photos(Base):
    __tablename__ = "photos"
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    candidate_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("candidates.id"), nullable=False)
    photo_url: so.Mapped[str] = so.mapped_column(sa.String(200), index=True, unique=True, nullable=False)
    cand: so.Mapped['Candidates'] = so.relationship(backref='photos')
    def __str__(self):
        return f"{self.id}: {self.candidate_id} {self.photo_url} "

# Таблица с информацией о кандидатах: True - в списке избранных, False - в черном списке, None - остальные кандидаты
class Flag(Base):
    __tablename__ = "flag"
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    cand_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("candidates.id"), nullable=False)
    flag: so.Mapped[bool]
    candidate: so.Mapped['Candidates'] = so.relationship(backref='flag')
    def __str__(self):
        return f"{self.id}: {self.cand_id} {self.flag} "

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

class VK:

   def __init__(self, access_token, user_id, version='5.131'):
       self.token = access_token
       self.id = user_id
       self.version = version
       self.params = {'access_token': self.token, 'v': self.version}

   def users_info(self):
       url = 'https://api.vk.com/method/users.get'
       params = {'user_ids': self.id}
       response = requests.get(url, params={**self.params, **params})
       return response.json()

   def get_candidates(self, hometown, gender, age):
       url = 'https://api.vk.com/method/users.search'
       params = {'count': 5, 'fields': 'city, sex, bdate', 'hometown': hometown, 'sex': gender, 'age_from': (age-10), 'age_to': (age+10)}
       resp = requests.get(url, params={**self.params, **params})
       return resp.json()

