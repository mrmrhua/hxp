class Config:
    SECRET_KEY = 'hello iam hxp'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 994
    MAIL_USE_SSL = True
    MAIL_USERNAME ='houxiaopangdeisgn@163.com'
    MAIL_PASSWORD = 'houxiaopang666'
    MAIL_SENDER = 'houxiaopangdeisgn@163.com'
     # FLASKY_MAIL_SUBJECT_PREFIX = '[FLASKY]'
    # FLASKY_MAIL_SENDER = 'Flasky Admin <dingyanhua@zju.edu.cn>'
    FLASKY_ADMIN = 'mrmrhua@126.com'
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    SQLALCHEMY_TRACK_MODIFICATIONS = True or False


    @staticmethod
    def init_app(app):
        pass


class DevConfig(Config):
    DEBUG = True
    #
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:126611@localhost/hxp'

class TestConfig(Config):
    pass
# SQLALCHEMY_DATABASE_URI =

class ReleaseConfig(Config):
    pass
# SQLALCHEMY_DATABASE_URI =

config = {
    'dev' : DevConfig,
    'test': TestConfig,
    'release': ReleaseConfig
}



# Global variables
SEX = {
    'MALE' : 1,
    'FEMALE' : 2,
    'UNKNOW' : 0
}


#apply status
APPLYSTATUS = {
    'APPLYING':0,
    'CHECKING': 1,
    'NOTPASS': -1,
    'PASS': 2
}

# 七牛
# 需要填写你的 Access Key 和 Secret Key
qiniu_access_key = 'Q3q69gi69DU3nre9CbFNUOdvlV9GhLANur32JF46'
qiniu_secret_key = '0xgKSNS1UKTSi69_GJ2qg5qjZq3wlkQF_OS2o-aS'
