from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    TYPE_CHOICES = (
        ('AdminUser', '管理員'),
        ('Member', '會員'),
    )

    username = models.CharField('帳號', max_length=255, null=False, unique=True)
    password = models.CharField('密碼', max_length=128, null=False)
    type = models.CharField('類型', choices=TYPE_CHOICES, max_length=50, null=False, default='AdminUser')
    is_superuser = models.BooleanField('超級管理員狀態', null=False, default=False)
    is_active = models.BooleanField('啟用狀態', null=False, default=True)
    last_login = models.DateTimeField('最後登入時間', null=True, blank=True)
    created_at = models.DateTimeField('建立時間', auto_now_add=True)
    updated_at = models.DateTimeField('修改時間', auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = '使用者'
        verbose_name_plural = '使用者'


class AdminUser(models.Model):
    user = models.OneToOneField(User, verbose_name='使用者', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '管理者'
        verbose_name_plural = '管理者'
        db_table = 'admin_users'

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created and instance.type == 'AdminUser':
            AdminUser.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        if instance.type == 'AdminUser':
            instance.adminuser.save()


class Member(models.Model):
    user = models.OneToOneField(User, verbose_name='使用者', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '會員'
        verbose_name_plural = '會員'
        db_table = 'members'

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created and instance.type == 'Member':
            Member.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        if instance.type == 'Member':
            instance.member.save()