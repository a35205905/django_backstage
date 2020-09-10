from django.db import models
from utils.model.managers import SoftDeletableManager
from django.utils import timezone


"""
Refer to this package django-model-utils
"""


class SoftDeletableModel(models.Model):
    """
    An abstract base class model with a ``delete_datetime`` field that
    marks entries that are not going to be used anymore, but are
    kept in db for any reason.
    Default manager returns only not-removed entries.
    """
    delete_datetime = models.DateTimeField('刪除時間', null=True, default=None)

    class Meta:
        abstract = True

    objects = SoftDeletableManager()
    all_objects = models.Manager()

    def delete(self, using=None, soft=True, *args, **kwargs):
        """
        Soft delete object (set its ``delete_datetime`` field to timezone now).
        Actually delete object if setting ``soft`` to False.
        """
        if soft:
            self.delete_datetime = timezone.now()
            self.save(using=using)
        else:
            return super().delete(using=using, *args, **kwargs)

    def restore(self, using=None):
        self.delete_datetime = None
        self.save(using=using)
