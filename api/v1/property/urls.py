from django.urls import path, re_path
from . import views

app_name = "api_v1_property"

urlpatterns = [
    re_path(r'^create-property/$', views.create_property, name="create-property"),
    re_path(r'^list-property/$', views.list_property, name="list-property"),
    re_path(r'^list-units/$', views.list_units, name="list-units"),
    re_path(r'^property-profile-view/(?P<pk>.*)/$', views.property_profile_view, name="property-profile-view"),
    
]