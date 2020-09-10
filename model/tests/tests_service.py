from django.test import TestCase
from ..services import root_url, get_pascal_name, get_content_type_model, get_model_by_content_type, get_model_permissions,\
    permission_check, get_content_type, get_view_permissions
from django.contrib.auth.models import User, Group, Permission, AnonymousUser
from django.test.client import RequestFactory
from django.conf import settings


import logging

logger = logging.getLogger(settings.LOGGING_ROLE)


class ServiceTest(TestCase):
    def test_root_url(self):
        self.assertEqual(root_url('news_category'), '/model/news_category/')

    def test_get_pascal_name(self):
        self.assertEqual(get_pascal_name('news_category'), 'NewsCategory')

    def test_get_content_type_model(self):
        self.assertEqual(get_content_type_model('news_category'), 'newscategory')

    def test_get_model_by_content_type(self):
        self.assertEqual(get_model_by_content_type('user'), User)


class ServicePermissionTest(TestCase):
    model = 'user'

    @classmethod
    def setUpTestData(cls):
        # 超級使用者
        User.objects.create_superuser(username='super', password='super')
        # 一般使用者
        User.objects.create_user(username='user', password='user')
        # 有權限的使用者
        permission_user = User.objects.create_user(username='permission_user', password='permission_user')
        group = Group.objects.create(name='group')
        group.user_set.add(permission_user)
        content_type = get_content_type(model='user')
        for permission in Permission.objects.filter(content_type=content_type):
            group.permissions.add(permission)

    def setUp(self):
        self.client.login(username='user', password='user')
        self.factory = RequestFactory()

    def test_get_model_permissions(self):
        super_user = User.objects.get(username='super')
        self.assertEqual(get_model_permissions(super_user, model=self.model), {'delete': 'auth.delete_user', 'add': 'auth.add_user', 'view': 'auth.view_user', 'change': 'auth.change_user'})
        user = User.objects.get(username='user')
        self.assertEqual(get_model_permissions(user, model=self.model), {})
        permission_user = User.objects.get(username='permission_user')
        self.assertEqual(get_model_permissions(permission_user, model=self.model), {'delete': 'auth.delete_user', 'add': 'auth.add_user', 'view': 'auth.view_user', 'change': 'auth.change_user'})

    def test_permission_check(self):
        # 4種角色做CRUD測試
        users = [
            {'username': 'anonymous_user', 'ans': False},
            {'username': 'user', 'ans': False},
            {'username': 'super', 'ans': True},
            {'username': 'permission_user', 'ans': True}
        ]
        id = User.objects.get(username='permission_user').id
        urls = [
            '/model/user/',
            '/model/user/new/',
            '/model/user/{id}/edit/'.format(id=id),
            '/model/user/{id}/delete/'.format(id=id)
        ]
        params = {'model': self.model}
        for url in urls:
            if 'edit' in url or 'delete' in url:
                params['pk'] = id
            else:
                params.pop('pk', None)
            request = self.factory.get(url)
            for user in users:
                if user['username'] == 'anonymous_user':
                    request.user = AnonymousUser()
                else:
                    request.user = User.objects.get(username=user['username'])
                self.assertEqual(permission_check(request, **params), user['ans'])

    def test_get_view_permissions(self):
        user = User.objects.get(username='super')
        ans = [
            {'model': 'user', 'model_name': '使用者'}, {'model': 'group', 'model_name': '群組'}]
        self.assertEqual(get_view_permissions(user), ans)
        user = AnonymousUser()
        ans = []
        self.assertEqual(get_view_permissions(user), ans)

