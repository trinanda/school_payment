import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #     'sqlite:///' + os.path.join(basedir, 'app.db')
    # SQLALCHEMY_DATABASE_URI = 'postgresql://tri:321123#@localhost/school_payment'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:#Admin123@localhost/school_payment'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

    # FLask-Security config
    SECURITY_URL_PREFIX = "/admin_school"
    SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
    SECURITY_PASSWORD_SALT = "AS878jhjsdjh#@$!^"

    # Flask-Security URLs, overriden because they don't put a / at the end
    SECURITY_LOGIN_URL = "/login_admin/"
    SECURITY_LOGOUT_URL = "/logout_admin/"
    SECURITY_REGISTER_URL = "/register_admin/"

    SECURITY_POST_LOGIN_VIEW = "/admin_school/"
    SECURITY_POST_LOGOUT_VIEW = "/admin_school/"
    SECURITY_POST_REGISTER_VIEW = "/admin_school/"

    # Flask-Security features
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
