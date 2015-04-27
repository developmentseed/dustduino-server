from configurations import values
from .base import Base


class Local(Base):

    # DEBUG
    DEBUG = values.BooleanValue(True)
    TEMPLATE_DEBUG = DEBUG
    # END DEBUG

    # Mail settings
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    # End mail settings
