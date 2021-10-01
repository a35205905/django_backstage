from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import EmailMessage
from django.http import JsonResponse

import logging

logger = logging.getLogger(settings.LOGGING_ROLE)


@login_required
def test_send(request):
    try:
        bcc = settings.MAIL_BCC
        if isinstance(bcc, str):
            bcc = [bcc]

        email = EmailMessage(
            'Test Mail',  # 標題
            'This is test mail',  # 內文
            settings.MAIL_FROM_ADDRESS,  # 發件人
            [settings.MAIL_FROM_ADDRESS],  # 收件人
            bcc=bcc  # 密件副本
        )
        email.send()
        return JsonResponse({'message': 'Mail Success'})
    except Exception as e:
        logger.warning('Mail Error')
        logger.warning(e)
        return JsonResponse({'message': 'Mail Error'})
