from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.contrib.auth.models import Permission
from django.core.exceptions import ValidationError
from django.db.models import Q

import logging
import os

logger = logging.getLogger(settings.LOGGING_ROLE)


def root_url(model):
    return '/model/{}/'.format(model)


# news_category => NewsCategory
def get_pascal_name(model, suffix=''):
    return ''.join([n.title() for n in model.split('_')]) + suffix


# news_category => newscategory
def get_content_type_model(model):
    return ''.join(model.split('_'))


def get_content_type(model):
    content_types = ContentType.objects.filter(model=get_content_type_model(model))
    if not content_types.exists():
        return None

    return content_types.first()


def get_model_by_content_type(model):
    content_type = get_content_type(model)
    if not content_type:
        return None

    return content_type.model_class()


def get_content_types(models):
    models = list(map(get_content_type_model, models))
    content_types = ContentType.objects.filter(model__in=models)
    return content_types


def permission_check(request, *args, **kwargs):
    model = kwargs.get('model', None)
    if model not in settings.MODELS:
        return False
    user = request.user
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    pk = kwargs.get('pk', None)
    url = request.get_full_path()
    method = '/'.join(url.split('/')[3:])
    content_type = get_content_type(model=model)
    content_type_model = content_type.model
    app_label = content_type.app_label
    if not pk:
        # 新增
        if 'new' in method:
            logger.debug('This user selecting add.')
            if user.has_perm('{}.add_{}'.format(app_label, content_type_model)):
                return True
        # 查看
        else:
            logger.debug('This user selecting view.')
            if user.has_perm('{}.view_{}'.format(app_label, content_type_model)):
                return True
    else:
        # 刪除
        if 'delete' in method:
            logger.debug('This user selecting delete.')
            if user.has_perm('{}.delete_{}'.format(app_label, content_type_model)):
                return True
        # 修改
        elif 'edit' in method:
            logger.debug('This user selecting edit.')
            if user.has_perm('{}.change_{}'.format(app_label, content_type_model)):
                return True

    return False


def get_model_permissions(user, model):
    response = {}
    if model not in settings.MODELS:
        return response

    content_type = get_content_type(model=model)
    model_permissions = Permission.objects.filter(content_type=content_type)
    model_permissions = set(['{}.{}'.format(permission.content_type.app_label, permission.codename) for permission in model_permissions])
    user_group_permissions = user.get_group_permissions()
    # 使用者對於這個model所有的權限
    permissions = model_permissions & user_group_permissions
    for permission in permissions:
        permission_key = permission.split('.')[1].split('_')[0]
        response[permission_key] = permission

    # {'add': 'auth.add_user', 'view': 'auth.view_user', 'change': 'auth.change_user', 'delete': 'auth.delete_user'}
    logger.debug(response)
    return response


def delete_model_file(_object):
    # 所有model的欄位
    for _field in _object._meta.fields:
        logger.debug(_field)
        _type = _field.get_internal_type()
        logger.debug(_type)
        # 若欄位為檔案類型 則依照路徑刪除檔案
        if _type == 'ImageField' or _type == 'FileField':
            file = getattr(_object, _field.attname)
            if not file:
                continue
            logger.debug(file.path)
            if os.path.isfile(file.path):
                os.remove(file.path)


def get_view_permissions(user):
    response = []
    if not user.is_authenticated:
        return response
    for model in settings.MODELS:
        content_type = get_content_type(model)
        if not content_type:
            continue
        _model = get_model_by_content_type(model)
        model_name = _model._meta.verbose_name.title()
        app_label = content_type.app_label
        if user.has_perm('{}.view_{}'.format(app_label, content_type.model)):
            response.append({'model': model, 'model_name': model_name})

    return response


def form_save(form):
    instance = None
    try:
        logger.debug(form.is_valid())
        # 已有資料並驗證過
        if form.is_valid():
            instance = form.save()
            return instance
        else:
            logger.debug(form.errors)
    except ValidationError:
        logger.warning(ValidationError)
    except Exception as e:
        logger.warning(e)

    logger.debug(instance)
    return instance


def objects_search(model, objects, keyword=None):
    try:
        if keyword and hasattr(model, 'config'):
            searchable = model.config.get('searchable')
            if searchable:
                # 如果有map的字串則取代
                maps = searchable.get('maps')
                if maps:
                    keyword = maps.get(keyword, keyword)

                params = Q()
                for item in searchable.get('columns'):
                    # 進行布林查詢(ex. status=True or status=False)
                    if type(keyword) == bool:
                        param = Q(**{item: keyword})
                    # 進行模糊查詢(ex. title__contains=keyword or content__contains=keyword)
                    else:
                        param = Q(**{item + '__contains': keyword})
                    params |= param

                print(params)
                objects = objects.filter(params)

    except Exception as e:
        logging.warning(e)
    
    return objects