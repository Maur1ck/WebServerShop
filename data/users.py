from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, index=True, unique=True, nullable=False)
    email = Column(String, index=True, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
