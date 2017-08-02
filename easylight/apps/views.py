from django.contrib.auth.models import User, Group
from rest_framework.generics import ListCreateAPIView
from apps.serializers import UserSerializer, GroupSerializer, ContractSerializer, TipsAndAdvertisingSerializer, ReceiptSerializer, StateSerializer, MunicipalitySerializer, RateSerializer, RateNameSerializer
from apps.models import State, Municipality, Contract, Receipt, TipsAndAdvertising, Rate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets, renderers
import xlrd
from xlrd import open_workbook, cellname
from django.http import HttpResponse
from rest_framework.permissions import AllowAny
from .pagination import ListStateSetPagination, ListMunicipalitySetPagination, ListRatePagination

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'groups': reverse('group-list', request=request, format=format),
        'state': reverse('state-list', request=request, format=format),
        'municipality': reverse('municipality-list', request=request, format=format),
    })

class UserViewSet(ListCreateAPIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupsList(ListCreateAPIView):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class StateViewSet(viewsets.ModelViewSet):
    """
    API Estados
    """
    permission_classes = (AllowAny,)
    pagination_class = ListStateSetPagination
    queryset = State.objects.all()
    serializer_class = StateSerializer


class MunicipalityList(viewsets.ModelViewSet):
    """
    API Municipios
    """
    queryset = Municipality.objects.all()
    serializer_class = MunicipalitySerializer
    permission_classes = (AllowAny,)
    pagination_class = ListMunicipalitySetPagination

    def get_queryset(self):
        states = self.request.GET.get('state_id')
        if states :
            self.queryset = self.queryset.filter(state_id = states)

        return self.queryset

class ContractList(viewsets.ModelViewSet):
    """
    API Contratos
    """
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = (AllowAny,)

    # def perform_create(self, serializer):
    #     print(self.request)
    #     serializer.save(name_contract = self.request.name_contract)

class ReceiptList(viewsets.ModelViewSet):
    """
    API Contratos
    """
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer
    permission_classes = (AllowAny,)

    # def perform_create(self, serializer):
    #     print(self.request)
    #     serializer.save(name_contract = self.request.name_contract)

class TipsAndAdvertisingList(viewsets.ModelViewSet):
    """
    API Contratos
    """
    queryset = TipsAndAdvertising.objects.all()
    serializer_class = TipsAndAdvertisingSerializer

class RateList(viewsets.ModelViewSet):
    """
    API Tarifas
    """


    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    permission_classes = (AllowAny,)
    pagination_class = ListRatePagination

class RateListUnique(viewsets.ModelViewSet):
    """
    API Lista de tarifas con nombres unicos
    """
    queryset = Rate.objects.order_by('name_rate').distinct('name_rate')
    serializer_class = RateNameSerializer
    permission_classes = (AllowAny,)

    # pagination_class = ListRatePagination

# def open_file(request):
#     book = xlrd.open_workbook("doc/Calculadora.xlsx")
#
#     worksheet = book.sheet_by_index(6)
#
#     states = []
#     rows = []
#     for col in range(1, worksheet.ncols):
#         states.append(worksheet.cell_value(0, col))
#
#         for row in range(0, worksheet.nrows):
#             if worksheet.cell_value(row, col) != '':
#                 rows.append(worksheet.cell_value(row, col))
#
#     print (rows)
#
#     return HttpResponse(worksheet)
