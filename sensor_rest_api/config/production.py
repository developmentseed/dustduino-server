from configurations import values

from .base import Base


class Production(Base):

    INSTALLED_APPS = Base.INSTALLED_APPS

    SECRET_KEY = values.SecretValue()

    INSTALLED_APPS += ("gunicorn", )
