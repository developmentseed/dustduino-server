from os.path import join

from django.core.mail import EmailMultiAlternatives
from django.conf import settings


class VerificaitonEmail(object):
    def __init__(self, to_email, code, **kwargs):
        self.to_email = to_email
        self.from_email = settings.DEFAULT_FROM_EMAIL
        self.code = code
        self.site_url = settings.PORTAL_URL

    def verify_link(self):
        return '%s?code=%s' % (join(self.site_url, 'verify'), self.code)

    def buildText(self):
        text = 'Hi, \n\n'
        text += 'Your request to register a new sensor is received. Please verify this request by clicking '
        text += 'on the below link.\n\n'
        text += self.verify_link()
        text += '\n\nThank you!'

        return text

    def buildHTML(self):
        text = '<p>Hi,</p>'
        text += '<p>Your request to register a new sensor is received. Please verify this request '
        text += 'by clicking on the below link.</p>'
        text += '<p><a href="%s">%s</a></p>' % (self.verify_link(), self.verify_link())
        text += '<p>Thank you!</p>'

        return text

    def send(self):
        from_email = self.from_email
        subject = 'Verify The Sensor'
        text_content = self.buildText()
        html_content = self.buildHTML()

        msg = EmailMultiAlternatives(subject, text_content, from_email,
                                     [self.to_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


class TokenEmail(object):
    def __init__(self, to_email, token, sensor_name=None):
        self.to_email = to_email
        self.token = token
        self.sensor_name = sensor_name
        self.from_email = settings.DEFAULT_FROM_EMAIL
        self.site_url = settings.PORTAL_URL

    def buildText(self):
        text = 'Hi, \n\n'
        text += 'The API Token is %s \n\n' % self.token
        text += 'This sensor is registered using %s.\n\n' % self.to_email
        text += 'Thank you!'

        return text

    def buildHTML(self):
        text = '<p>Hi,</p>'
        text += '<p>The API Token is <code>%s</code></p>' % self.token
        text += '<p>This sensor is registered with %s.</p>' % self.to_email
        text += '<p>Thank you!</p>'

        return text

    def send(self):
        from_email = self.from_email
        subject = 'API Token for sensor named %s' % self.sensor_name
        text_content = self.buildText()
        html_content = self.buildHTML()

        msg = EmailMultiAlternatives(subject, text_content, from_email,
                                     [self.to_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
