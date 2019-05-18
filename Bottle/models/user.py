from sqlalchemy import Column, Integer, String, SmallInteger
from werkzeug.security import generate_password_hash, check_password_hash
from Bottle.models.base import BaseModel, db
from Bottle.utils.enums import UserTypeEnum
from Bottle.utils.generate_key import generate_app_key


class User(BaseModel):
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(24), unique=True, nullable=False)
    nickname = Column(String(24), unique=True)
    _password = Column('password', String(128))
    #默认普通用户

    scope = Column(SmallInteger, default=UserTypeEnum.NORMAL.value)
    app_key = Column(String(128), unique=True)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)


    def check_password(self, raw):
        if not self._password:
            raise False
        return check_password_hash(self._password, raw)

    @staticmethod
    def register(nickname, email, password):
        with db.auto_commit():
            user = User()
            user.nickname = nickname
            user.email = email
            user.password = password
            db.session.add(user)


    @staticmethod
    def register_developer():
        with db.auto_commit():
            user = User()
            user.scope = UserTypeEnum.DEVELOPER.value
            user.app_key = generate_app_key(user.id)
            db.session.add(user)

