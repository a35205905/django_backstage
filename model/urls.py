from django.urls import path

from . import views

app_name = 'model'
urlpatterns = [
    # 權限管理
    path('view_permissions/', views.view_permissions, name='view_permissions'),

    path('<model>/', views.index, name='index'),
    path('<model>/<pk>/delete/', views.delete, name='delete'),
    path('<model>/new/', views.new, name='new'),
    path('<model>/<pk>/edit/', views.edit, name='edit'),

]