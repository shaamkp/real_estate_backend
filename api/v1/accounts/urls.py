from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from django.urls import path, re_path

from . import views

app_name = "api_v1_accounts"

urlpatterns = [
    re_path(r'^chief-login/$', views.chief_profile_login, name="login-chief"),
    re_path(r'^create-tenant-profile/$', views.create_tenant_profile, name="create-tenant-profile"),
    re_path(r'^assign-unit-tenant/(?P<pk>.*)/$', views.assign_unit_to_tenant, name="assign-unit-tenant"),
    re_path(r'^list-tenant-profile/$', views.list_tenant_profile, name="list-tenant-profile"),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]