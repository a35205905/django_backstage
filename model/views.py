from django.shortcuts import render, get_object_or_404, redirect
from .forms import AdminUserForm, AdminUserEditForm, GroupForm
from .tables import AdminUserTable, GroupTable
from .services import root_url, get_pascal_name, get_model_by_content_type, permission_check, get_model_permissions,\
    get_view_permissions, form_save
from django.http import JsonResponse
from utils.auth.decorator import user_passes_test
from django.contrib.auth.decorators import login_required
from django.conf import settings

import logging

logger = logging.getLogger(settings.LOGGING_ROLE)


@user_passes_test(permission_check, login_url='/', redirect_field_name='')
def index(request, model):
    _model = get_model_by_content_type(model)
    _objects = _model.objects.all()
    # 排序
    sort = request.GET.get('sort', '-id')
    # table 一定要為大駝峰命名(ex. UserTable)
    table = globals()[get_pascal_name(model, 'Table')](_objects, order_by=sort)
    table.paginate(page=request.GET.get("page", 1), per_page=25)
    model_name = _model._meta.verbose_name.title()

    model_permissions = get_model_permissions(request.user, model)
    return render(request, 'model/index.html', {
        'model': model, 'model_name': model_name, 'table': table, 'model_permissions': model_permissions
    })


@user_passes_test(permission_check, login_url='/', redirect_field_name='')
def delete(request, model, pk):
    _model = get_model_by_content_type(model)
    _object = get_object_or_404(_model, pk=pk)
    if model == 'admin_user':
        user = _object.user
        _object.delete()
        user.delete()
    else:
        _object.delete()
    return redirect(root_url(model))


@user_passes_test(permission_check, login_url='/', redirect_field_name='')
def new(request, model):
    _model = get_model_by_content_type(model)
    model_name = _model._meta.verbose_name.title()
    # model from 一定要為大駝峰命名(ex. UserForm)
    logger.debug(request.POST)
    form = globals()[get_pascal_name(model, 'Form')](request.POST or None, request.FILES or None)
    instance = form_save(form)
    if instance:
        return redirect(root_url(model))

    return render(request, 'model/new.html', {'form': form, 'model': model, 'model_name': model_name, 'model_method': 'new'})


@user_passes_test(permission_check, login_url='/', redirect_field_name='')
def edit(request, model, pk):
    _model = get_model_by_content_type(model)
    model_name = _model._meta.verbose_name.title()
    _object = get_object_or_404(_model, pk=pk)
    logger.debug(request.POST)
    if model == 'admin_user':
        form = AdminUserEditForm(request.POST or None, request.FILES or None, instance=_object.user)
    else:
        # model from 一定要為大駝峰命名(ex. UserForm)
        form = globals()[get_pascal_name(model, 'Form')](request.POST or None, request.FILES or None, instance=_object)
    instance = form_save(form)
    if instance:
        return redirect(root_url(model))

    return render(request, 'model/new.html', {'form': form, 'model': model, 'model_name': model_name, 'model_method': 'edit', 'object': _object})


@login_required
def view_permissions(request):
    return JsonResponse(get_view_permissions(request.user), safe=False)
