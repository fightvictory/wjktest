import os

class Config:
    SECRET_KEY = '12345678a'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://puser:123456@127.0.0.1/pblog'
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.qq.com')
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', '你的邮箱地址')
    MAIL_PASSWORD = '你的邮箱密码'

    FLASKY邮件主题前缀 = '【FLASKY博客】'
    FLASK邮件发送者 = 'FLASK管理员<你的邮箱地址>'
    FLASKY管理员 = '你的邮箱地址'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    FLASKY_POSTS_PER_PAGE = 10
    FLASKY_FOLLOWERS_PER_PAGE = 50
    FLASKY_COMMENTS_PER_PAGE = 30

    @staticmethod
    def init_app(app):
        pass

# 需要修改成自己的数据库和用户名密码
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
