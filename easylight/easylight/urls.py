from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from apps.views import StateViewSet, MunicipalityList, RateList, RateListUnique, ContractList, ReceiptList
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
contract_list = ContractList.as_view({
    'get': 'list',
    'post': 'create'
})
contract_detail = ContractList.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
receipt_list = ReceiptList.as_view({
    'get': 'list',
    'post': 'create'
})
receipt_detail = ReceiptList.as_view({
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
rate_list = RateList.as_view({
    'get': 'list',
    'post': 'create'
})
rate_unique_list = RateListUnique.as_view({
    'get': 'list',
    # 'post': 'create'
})

urlpatterns = format_suffix_patterns([
    # url(r'^', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.api_root),
    # url(r'^open/$', views.open_file),
    url(r'^groups/$', views.GroupsList.as_view(), name='group-list'),
    url(r'^states/$', state_list, name='state-list'),
    url(r'^states/(?P<pk>[0-9]+)/$', state_detail, name='state-detail'),
    url(r'^municipality/$', municipality_list, name='municipality-list'),
    url(r'^municipality/(?P<pk>[0-9]+)/$', municipality_detail, name='municipality-detail'),
    url(r'^rate/$', rate_list, name='rate-list'),
    url(r'^rate_unique/$', rate_unique_list, name='rate-unique-list'),
    url(r'^contract/$', contract_list, name='contract-list'),
    url(r'^contract/(?P<pk>[0-9]+)/$', contract_detail, name='contract-detail'),
    url(r'^receipt/$', receipt_list, name='receipt-list'),
    url(r'^receipt/(?P<pk>[0-9]+)/$', receipt_detail, name='receipt-detail'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))

])
