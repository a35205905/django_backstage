from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, TokenVerifyView)

router = routers.DefaultRouter()

app_name = 'api'
urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    # 新增Token
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # 刷新Token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # 驗證Token
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]