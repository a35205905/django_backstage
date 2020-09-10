from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone


"""
Refer to this package django-model-utils
"""


class SoftDeletableQuerySetMixin:
    """
    QuerySet for SoftDeletableModel. Instead of removing instance sets
    its ``delete_datetime`` field to timezone now.
    """

    def delete(self, soft=True):
        """
        Soft delete objects from queryset (set their ``delete_datetime``
        field to timezone now)
        Actually delete objects if setting ``soft`` to False.
        """
        if soft:
            self.update(delete_datetime=timezone.now())
        else:
            super().delete()

    def restore(self):
        self.update(delete_datetime=None)


class SoftDeletableQuerySet(SoftDeletableQuerySetMixin, QuerySet):
    pass


class SoftDeletableManagerMixin:
    """
    Manager that limits the queryset by default to show only not removed
    instances of model.
    """
    _queryset_class = SoftDeletableQuerySet

    def get_queryset(self):
        """
        Return queryset limited to not removed entries.
        """
        kwargs = {'model': self.model, 'using': self._db}
        if hasattr(self, '_hints'):
            kwargs['hints'] = self._hints

        return self._queryset_class(**kwargs).filter(delete_datetime=None)

    def all_deleted(self):
        kwargs = {'model': self.model, 'using': self._db}
        if hasattr(self, '_hints'):
            kwargs['hints'] = self._hints

        return self._queryset_class(**kwargs).exclude(delete_datetime=None)


class SoftDeletableManager(SoftDeletableManagerMixin, models.Manager):
    pass
