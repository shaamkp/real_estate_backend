
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/accounts/', include('api.v1.accounts.urls', namespace='api_v1_accounts')),
    path('api/v1/property/', include('api.v1.property.urls', namespace='api_v1_property')),

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]
