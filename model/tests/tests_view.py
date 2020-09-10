from django.test import TestCase
from django.contrib.auth.models import User
from django.conf import settings

import logging

logger = logging.getLogger(settings.LOGGING_ROLE)


class ViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_superuser(username='user', password='user')

    def setUp(self):
        self.client.login(username='user', password='user')

    def test_get_list_page(self):
        resp = self.client.get('/model/user/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'model/index.html')
        # logger.debug(resp.content.decode())

    def test_get_list_fail_page(self):
        resp = self.client.get('/model/fail/', follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'index.html')
        # logger.debug(resp.content.decode())

    def test_get_new_page(self):
        resp = self.client.get('/model/user/new/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'model/new.html')
        # logger.debug(resp.content.decode())

    def test_get_new_fail_page(self):
        resp = self.client.get('/model/fail/new/', follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'index.html')
        # logger.debug(resp.content.decode())

    def test_get_edit_page(self):
        user = User.objects.get(username='user')
        resp = self.client.get('/model/user/{id}/edit/'.format(id=user.id))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'model/new.html')
        # logger.debug(resp.content.decode())

    def test_get_edit_fail_page(self):
        user = User.objects.get(username='user')
        resp = self.client.get('/model/fail/{id}/edit/'.format(id=user.id), follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'index.html')
        # logger.debug(resp.content.decode())

    def test_get_delete_page(self):
        user = User.objects.get(username='user')
        resp = self.client.get('/model/user/{id}/delete/'.format(id=user.id), follow=True)
        self.assertEqual(resp.status_code, 200)
        # 刪除使用者自己本身會強制登入並導回首頁
        self.assertTemplateUsed(resp, 'index.html')
        # logger.debug(resp.content.decode())

    def test_get_delete_fail_page(self):
        user = User.objects.get(username='user')
        resp = self.client.get('/model/fail/{id}/delete/'.format(id=user.id), follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'index.html')
        # logger.debug(resp.content.decode())

    def test_get_view_permissions_page(self):
        resp = self.client.get('/model/view_permissions/')
        self.assertEqual(resp.status_code, 200)


