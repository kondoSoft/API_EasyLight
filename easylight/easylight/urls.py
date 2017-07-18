from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from apps.views import StateViewSet, MunicipalityList
from rest_framework import renderers
from apps import views
from django.contrib import admin

state_list = StateViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
state_detail = StateViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
municipality_list = MunicipalityList.as_view({
    'get': 'list',
    'post': 'create'
})
municipality_detail = MunicipalityList.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
urlpatterns = format_suffix_patterns([
    # url(r'^', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.api_root),
    url(r'^open/$', views.open_file),
    url(r'^groups/$', views.GroupsList.as_view(), name='group-list'),
    url(r'^states/$', state_list, name='state-list'),
    url(r'^states/(?P<pk>[0-9]+)/$', state_detail, name='state-detail'),
    url(r'^municipality/$', municipality_list, name='municipality-list'),
    url(r'^municipality/(?P<pk>[0-9]+)/$', municipality_detail, name='municipality-detail'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))

])
