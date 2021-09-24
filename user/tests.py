from django.test import TestCase
from user.models import User


# 未登入
class ViewTest(TestCase):
    def test_get_home_page(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'index.html')

    def test_get_login_page(self):
        resp = self.client.get('/login/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'registration/login.html')

    def test_get_register_page(self):
        resp = self.client.get('/register/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'user/register.html')


# 登入後(一般使用者)
class UserViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_superuser(username='user', password='user')

    def setUp(self):
        self.client.login(username='user', password='user')

    def test_get_logout_page(self):
        resp = self.client.get('/logout/', follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'registration/login.html')

    def test_get_password_change_page(self):
        resp = self.client.get('/password_change/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'user/change.html')

    def test_get_user_change_page(self):
        resp = self.client.get('/user_change/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'user/change.html')
