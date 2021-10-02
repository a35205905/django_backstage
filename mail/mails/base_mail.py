from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

import logging

logger = logging.getLogger(settings.LOGGING_ROLE)


class BaseMail:
    def __init__(self):
        self.subject = 'Subject'

        self.body = 'Base'
        self.body_params = {}

        self.from_email = settings.MAIL_FROM_ADDRESS
        if not settings.MAIL_FROM_ADDRESS:
            logger.info('Not find MAIL_FROM_ADDRESS')

        self.bcc = settings.MAIL_BCC_ADDRESS
        if isinstance(self.bcc, str):
            self.bcc = [self.bcc]
        if not settings.MAIL_BCC_ADDRESS:
            logger.info('Not find MAIL_BCC_ADDRESS')

    def send(self, to):
        try:
            body = render_to_string(
                'mail/' + self.body + '.html',
                self.body_params
            )

            if isinstance(to, str):
                to = [to]

            email = EmailMessage(
                self.subject,  # 標題
                body,  # 內文
                self.from_email,  # 發件人
                to,  # 收件人
                self.bcc  # 密件副本
            )

            email.send()
            logger.info('Mail Success')

            return self
        except Exception as e:
            logger.warning('Mail Error')
            logger.warning(e)

            return None
