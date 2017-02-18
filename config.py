"""
This is the configuration for the whole package.

@Author: Dong Liu
"""

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'This is a secret'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    EDGETOOLS_MAIL_SUBJECT_PREFIX = '[EdgeTools]'
    EDGETOOLS_MAIL_SENDER = 'EdgeTools Admin <testofdong@gmail.com>'
    EDGETOOLS_ADMIN = os.environ.get('EDGETOOLS_ADMIN')

    @staticmethod
    def init_app(app):
        pass


class DevConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI') or \
                              'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI') or \
                              'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
                              'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevConfig,
    'testing': TestConfig,
    'production': ProdConfig,
    'default': DevConfig
}


users = {
    '1': 'alex',
    '2': 'burton',
    '3': 'cathy'
}
