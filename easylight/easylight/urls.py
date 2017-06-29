from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from apps.views import StateViewSet
from rest_framework import renderers
from apps import views

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
state_highlight = StateViewSet.as_view({
    'get': 'highlight'
}, renderer_classes=[renderers.StaticHTMLRenderer])

urlpatterns = format_suffix_patterns([
    # url(r'^', include(router.urls)),
    url(r'^$', views.api_root),
    url(r'^groups/$', views.GroupsList.as_view(), name='group-list'),
    url(r'^states/$', state_list, name='state-list'),
    url(r'^states/(?P<pk>[0-9]+)/$',
        state_detail,
        name='state-detail'),
    url(r'^states/(?P<pk>[0-9]+)/highlight/$',
        state_highlight,
        name='state-highlight'),
    url(r'^municipality/$', views.MunicipalityList.as_view(), name='municipality-list'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
])
