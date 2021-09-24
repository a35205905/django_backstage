from django.test import TestCase
from django.conf import settings
from user.models import User
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile

import logging

logger = logging.getLogger(settings.LOGGING_ROLE)
ROOT_URL = 'model'


def create_image(filename, storage=None, size=(100, 100), image_mode='RGB', image_format='PNG'):
    """
    Generate a test image, returning the filename that it was saved as.

    If ``storage`` is ``None``, the BytesIO containing the image data
    will be passed instead.
    """
    data = BytesIO()
    Image.new(image_mode, size).save(data, image_format)
    data.seek(0)
    if not storage:
        return SimpleUploadedFile(filename, data.getvalue())
    image_file = ContentFile(data.read())
    return storage.save(filename, image_file)


def get_path(model, method, pk=None):
    path = ''
    if not pk:
        if method == 'new':
            # / model / about / new /
            path = '/{root_url}/{model}/{method}/'.format(root_url=ROOT_URL, model=model, method=method)
        elif method == 'view':
            # / model / about /
            path = '/{root_url}/{model}/'.format(root_url=ROOT_URL, model=model)
    else:
        # / model / about / pk / delete /
        # / model / about / pk / edit /
        path = '/{root_url}/{model}/{pk}/{method}/'.format(root_url=ROOT_URL, model=model, pk=pk, method=method)

    logger.debug(path)
    return path


class FormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_superuser(username='user', password='user')

    def setUp(self):
        self.client.login(username='user', password='user')
