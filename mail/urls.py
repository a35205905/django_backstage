from django.urls import path

from . import views

app_name = 'mail'
urlpatterns = [
    path('test_send/', views.test_send, name='test_send'),

]