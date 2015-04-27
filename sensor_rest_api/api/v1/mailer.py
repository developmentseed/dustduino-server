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
        return '%s?code=%s' % (join(self.site_url, 'api', 'v1', 'verify'), self.code)

    def buildText(self):
        text = 'Hi, \n\n'
        text += 'You request to register a new sensor is received. Please verify this request by clicking '
        text += 'on the below link.\n\n'
        text += self.verify_link()
        text += '\n\nThank you!'

        return text

    def buildHTML(self):
        text = '<p>Hi,</p>'
        text += '<p>You request to register a new sensor is received. Please verify this request '
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
