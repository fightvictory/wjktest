import os

class Config:
    SECRET_KEY = '12345678a'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://puser:123456@127.0.0.1/pblog'
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.qq.com')
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', '你的邮箱地址')
    MAIL_PASSWORD = '你的第三方邮箱密码'

    FLASKY邮件主题前缀 = '【FLASKY博客】'
    FLASK邮件发送者 = 'FLASK管理员<你的邮箱地址>'
    FLASKY管理员 = '你的邮箱地址'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://puser:123456@127.0.0.1/pblog'

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://puser:123456@127.0.0.1/pblog'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://puser:123456@127.0.0.1/pblog'

config = {
    'development': DevelopmentConfig,
    'testing': TestConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
