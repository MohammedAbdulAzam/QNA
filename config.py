import os

class Config:
    SECRET_KEY ='dev-secret-key-123'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///qna.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    QUIZMASTER_USERNAME = 'quizmaster'
    QUIZMASTER_PASSWORD = '123'