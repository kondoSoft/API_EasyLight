from django.contrib.auth.models import User, Group
from rest_framework.generics import ListCreateAPIView
from apps.serializers import UserSerializer, GroupSerializer, ContractSerializer, TipsAndAdvertisingSerializer, ReceiptSerializer, StateSerializer, MunicipalitySerializer
from apps.models import State, Municipality, Contract, Receipt, TipsAndAdvertising
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets, renderers
import xlrd
from xlrd import open_workbook, cellname
from django.http import HttpResponse

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
    queryset = State.objects.all()
    serializer_class = StateSerializer


class MunicipalityList(viewsets.ModelViewSet):
    """
    API Municipios
    """
    queryset = Municipality.objects.all()
    serializer_class = MunicipalitySerializer

class ContractList(viewsets.ModelViewSet):
    """
    API Contratos
    """
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer

class ReceiptList(viewsets.ModelViewSet):
    """
    API Contratos
    """
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer

class TipsAndAdvertisingList(viewsets.ModelViewSet):
    """
    API Contratos
    """
    queryset = TipsAndAdvertising.objects.all()
    serializer_class = TipsAndAdvertisingSerializer

def open_file(request):
    book = xlrd.open_workbook("doc/Calculadora.xlsx")

    worksheet = book.sheet_by_index(6)

    states = []
    rows = []
    for col in range(1, worksheet.ncols):
        states.append(worksheet.cell_value(0, col))

        for row in range(0, worksheet.nrows):
            if worksheet.cell_value(row, col) != '':
                rows.append(worksheet.cell_value(row, col))

    print (rows)

    return HttpResponse(worksheet)
