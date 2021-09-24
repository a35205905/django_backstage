import django_tables2 as tables
from user.models import User
from django.contrib.auth.models import Group

TEMPLATE_NAME = "django_tables2/bootstrap4.html"
# 編輯、刪除按鈕頁面
ROOT_URL = 'model'
MANAGE = tables.TemplateColumn(template_name='{}/manage_column.html'.format(ROOT_URL), verbose_name='操作', orderable=False)
PREVIEW_QUILL = tables.TemplateColumn(template_name='{}/preview_quill_column.html'.format(ROOT_URL), verbose_name='內文', orderable=False)
PREVIEW_QUILL_CONTACT = tables.TemplateColumn(template_name='{}/preview_quill_contact_column.html'.format(ROOT_URL), verbose_name='內文', orderable=False)


def image_template_column(field):
    width = 150
    height = 150
    html = '{{% if record.{field} %}}' \
           '<img src="{{{{ record.{field}.url }}}}" width="{width}" height="{height}">' \
           '{{% else %}}' \
           '—' \
           '{{% endif %}}'.format(field=field, width=width, height=height)
    return tables.TemplateColumn(html, orderable=False)


class AdminUserTable(tables.Table):
    manage = MANAGE
    is_active = tables.Column(accessor='user.is_active')

    def render_is_active(self, value, record):
        if record.user.is_active:
            return '啟用'
        else:
            return '停用'

    class Meta:
        model = User
        template_name = TEMPLATE_NAME
        fields = ('id', "user.username", 'is_active', 'user.last_login', 'user.created_at', 'user.updated_at', 'manage')


class GroupTable(tables.Table):
    manage = MANAGE

    class Meta:
        model = Group
        template_name = TEMPLATE_NAME
        fields = ('id', "name", 'manage')





