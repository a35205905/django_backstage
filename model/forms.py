from django.forms import ModelForm, CharField, Select, PasswordInput, MultipleChoiceField, CheckboxSelectMultiple, ModelChoiceField
from user.models import User
from django.contrib.auth.models import Group, Permission
from django.conf import settings
from model.services import get_content_types


class AdminUserForm(ModelForm):
    password = CharField(
        label="密碼",
        strip=False,
        required=True,
        widget=PasswordInput,
    )

    group = ModelChoiceField(
        label='群組', queryset=Group.objects.all(), required=False, widget=Select()
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'group']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()

        group = self.cleaned_data["group"]
        user.groups.add(group)

        return user


class AdminUserEditForm(ModelForm):
    group = ModelChoiceField(
        label='群組', queryset=Group.objects.all(), required=False, widget=Select()
    )

    class Meta:
        model = User
        fields = ['username', 'group', 'is_active']

    def __init__(self, *args, **kwargs):
        super(AdminUserEditForm, self).__init__(*args, **kwargs)
        self.fields['group'].initial = self.instance.groups.first()

    def save(self, commit=True):
        user = super().save(commit=False)

        new_group = self.cleaned_data["group"]
        old_group = user.groups.first()
        # 使用者更改群組時才替換
        if new_group != old_group:
            user.groups.clear()
            user.groups.add(new_group)

        if commit:
            user.save()

        return user


class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'content_types']

    content_types = MultipleChoiceField(label='權限', required=False, widget=CheckboxSelectMultiple)
    # group_users = ModelMultipleChoiceField(label='使用者', queryset=User.objects.all(), required=False, widget=CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)
        # 將使用者不需要的model排除
        content_types = get_content_types(settings.MODELS)
        # self.fields['permissions'].queryset = Permission.objects.filter(content_type__in=content_types)
        # 顯示群組裡的使用者
        # if self.instance.id:
        #     user_ids = [user.id for user in self.instance.user_set.all()]
        #     self.fields['group_users'].initial = user_ids

        # 將CRUD權限改為以model為單位(ex. 勾選user代表可以對user進行增刪改查)
        content_type_choices = tuple([(content_type.id, content_type.name) for content_type in content_types])
        self.fields['content_types'].choices = content_type_choices

        # 顯示群組有的model權限
        if self.instance.id:
            group_permissions = self.instance.permissions.all()
            group_content_types = set([permission.content_type for permission in group_permissions])
            content_types_initial = list(group_content_types.intersection(set(content_types)))
            self.fields['content_types'].initial = [item.id for item in content_types_initial]

    def save(self, commit=True):
        group = super().save(commit=False)
        if commit:
            group.save()
            # 寫入多對多表
            self.save_m2m()
        # 加入權限
        group_permissions = group.permissions.all()
        content_types = self.cleaned_data["content_types"]
        group_set_permissions = Permission.objects.filter(content_type_id__in=content_types)
        group_remove_permissions = group_permissions.exclude(id__in=group_set_permissions)
        group_add_permissions = group_set_permissions.exclude(id__in=group_permissions)
        for permission in group_remove_permissions:
            group.permissions.remove(permission)
        for permission in group_add_permissions:
            group.permissions.add(permission)


        # 加入使用者
        # group_users = group.user_set.all()
        # group_set_users = self.cleaned_data["group_users"]
        # group_remove_users = group_users.exclude(id__in=group_set_users)
        # group_add_users = group_set_users.exclude(id__in=group_users)
        # for user in group_remove_users:
        #     group.user_set.remove(user)
        # for user in group_add_users:
        #     group.user_set.add(user)
        return group

