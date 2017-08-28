from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from apps.views import GroupsList, UserViewSet, StateViewSet, MunicipalityList, RateList, Mun_RateList, ContractList, ReceiptList, ContactUs, Subscribe
from rest_framework import renderers
from django.conf.urls.static import static
from apps import views
from django.contrib import admin
from easylight import settings
from rest_framework.authtoken import views as rest_framework_views


user_list =UserViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

group_list = GroupsList.as_view({
    'get': 'list',
    'post': 'create'
})
group_detail = GroupsList.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
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
#Vista de tarifa general
rate_list = RateList.as_view({
    'get': 'list',
    'post': 'create'
})
#Vista de tarifa por municipio
mun_rate_list = Mun_RateList.as_view({
    'get': 'list',
    # 'post': 'create'
})
# contact_list = ContactUs.as_view({
#     'get': 'list',
#     'post': 'create'
# })

urlpatterns = format_suffix_patterns([
    url(r'^admin/', include(admin.site.urls)),
    # Session Login
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^groups/$', group_list, name='group-list'),
    url(r'^group/(?P<pk>[0-9]+)/$', group_detail, name='group-detail'),
    # Estados
    url(r'^states/$', state_list, name='state-list'),
    url(r'^states/(?P<pk>[0-9]+)/$', state_detail, name='state-detail'),
    # Municipios
    url(r'^municipality/$', municipality_list, name='municipality-list'),
    url(r'^municipality/(?P<pk>[0-9]+)/$', municipality_detail, name='municipality-detail'),
    # Tarifas
    url(r'^rate/$', rate_list, name='rate-list'),
    url(r'^rate_unique/$', mun_rate_list, name='mun-rate-list'),
    #Contratos
    url(r'^contract/$', contract_list, name='contract-list'),
    url(r'^contract/(?P<pk>[0-9]+)/$', contract_detail, name='contract-detail'),
    #recibos
    url(r'^receipt/$', receipt_list, name='receipt-list'),
    url(r'^receipt/(?P<pk>[0-9]+)/$', receipt_detail, name='receipt-detail'),
    # Autenticacion API
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^contact/$', ContactUs.as_view(), name='contact-list'),
    url(r'^subscribe/$', Subscribe.as_view(), name='subscribe-list'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
