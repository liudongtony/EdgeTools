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
    ET_ADMIN = os.environ.get('ET_ADMIN')
    SQLALCHEMY_RECORD_QUERIES = True
    ET_DB_QUERY_TIMEOUT = 0.5
    SSL_DISABLE = True

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
    WTF_CSRF_ENABLED = False


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
                              'sqlite:///' + os.path.join(basedir, 'data.sqlite')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
                fromadd = cls.ET_MAIL_SENDER,
                toaddrs=[cls.ET_ADMIN],
                subject=cls.ET_MAIL_SUBJECT_PREFIX + ' Application Error',
                credentials=credentials,
                secure=secure
            )
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)


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
