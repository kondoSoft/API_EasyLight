from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from rest_framework.generics import ListCreateAPIView
from apps.serializers import LoginSerializer, UserSerializer, GroupSerializer, ContractSerializer, TipsAndAdvertisingSerializer, ReceiptSerializer, StateSerializer, MunicipalitySerializer, RateSerializer, RateNameSerializer
from apps.models import State, Municipality, Contract, Receipt, TipsAndAdvertising, Rate
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets, renderers
import xlrd
from xlrd import open_workbook, cellname
from django.http import HttpResponse
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from apps.permissions import IsOwnerOrDeny
from .pagination import ListStateSetPagination, ListMunicipalitySetPagination, ListRatePagination
from rest_framework.authtoken.models import Token

def get_auth_token(self, request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)

    if user is not None:
        # the password verified for the user
        if user.is_active:
            token, created = Token.objects.get_or_create(user=user)
            request.session['auth'] = token.key
            return request
    return HttpResponse

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class GroupsList(viewsets.ModelViewSet):
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
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        id_owner = self.request.user
        self.queryset = self.queryset.filter(owner = id_owner)

        return self.queryset

class ReceiptList(viewsets.ModelViewSet):
    """
    API Contratos
    """
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer
    permission_classes = (AllowAny,)


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
