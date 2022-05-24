from sqlalchemy import (create_engine, Table, MetaData,
                        Column, Integer, String, Boolean)
from sqlalchemy.orm import mapper, sessionmaker

engine = create_engine('sqlite:///sqlite.db', echo=True)
metadata = MetaData(engine)

user = Table('users', metadata,
             Column('id', Integer(), primary_key=True, nullable=False),
             Column('oauth_id', String()),
             Column('email', String()),
             Column('active', Boolean(), default=True),
    )

class User(object):
    def __init__(self, oauth_id, email):
        self.oauth_id = oauth_id
        self.email = email

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.oauth_id

    @staticmethod
    def load(oauth_id):
        try:
            user = session.query(User).filter_by(oauth_id=oauth_id).one()
            return user
        except:
            return None

    @staticmethod
    def add(**data):
        user = User(data['id'], data['email'])
        session.add(user)
        session.commit()
        return user

mapper(User, user)

Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session()
metadata.create_all()

if __name__ == '__main__':
    ed_user = User('8675309', 'ed', 'ed.jones@gmail.com')
    session.add(ed_user)
    session.commit()
    user = session.query(User).filter_by(oauth_id='8675309').one()
    print(user.name)
