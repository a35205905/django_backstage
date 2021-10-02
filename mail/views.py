from django.contrib.auth.decorators import login_required
from django.conf import settings
from mail.mails.test_mail import TestMail
from django.http import JsonResponse

import logging

logger = logging.getLogger(settings.LOGGING_ROLE)


@login_required
def test_send(request):
    mail = TestMail()
    mail = mail.send(settings.MAIL_NOTIFY_ADDRESS)
    if mail:
        return JsonResponse({'message': 'Mail Success'})
    else:
        return JsonResponse({'message': 'Mail Error'})

