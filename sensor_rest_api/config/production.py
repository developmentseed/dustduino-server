from configurations import values

from .base import Base


class Production(Base):

    INSTALLED_APPS = Base.INSTALLED_APPS

    SECRET_KEY = values.SecretValue()

    INSTALLED_APPS += ("gunicorn", )
    ALLOWED_HOSTS = ['*']

    # EMAIL
    EMAIL_HOST = values.Value('smtp.sendgrid.com')
    EMAIL_HOST_PASSWORD = values.SecretValue(environ_prefix="", environ_name="SENDGRID_PASSWORD")
    EMAIL_HOST_USER = values.SecretValue(environ_prefix="", environ_name="SENDGRID_USERNAME")
    EMAIL_PORT = values.IntegerValue(587, environ_prefix="", environ_name="EMAIL_PORT")
    EMAIL_SUBJECT_PREFIX = values.Value('[Sensor API] ', environ_name="EMAIL_SUBJECT_PREFIX")
    EMAIL_USE_TLS = True
    SERVER_EMAIL = EMAIL_HOST_USER
    # END EMAIL
