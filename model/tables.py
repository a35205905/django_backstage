import django_tables2 as tables
from django.contrib.auth.models import User, Group

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


class UserTable(tables.Table):
    manage = MANAGE

    def render_groups(self, value):
        if value.all():
            return ', '.join(tuple([group.name for group in value.all()]))
        return '—'

    class Meta:
        model = User
        template_name = TEMPLATE_NAME
        fields = ('id', "username", 'first_name', 'groups', 'is_active', 'is_superuser', 'last_login', 'manage')


class GroupTable(tables.Table):
    manage = MANAGE

    class Meta:
        model = Group
        template_name = TEMPLATE_NAME
        fields = ('id', "name", 'manage')





