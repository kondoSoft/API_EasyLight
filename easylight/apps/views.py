from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from rest_framework.generics import ListCreateAPIView
from apps.serializers import RateSerializer, UserSerializer, GroupSerializer, ContractSerializer, TipsAndAdvertisingSerializer, ReceiptSerializer, StateSerializer, MunicipalitySerializer, RateSerializer, Mun_RateSerializer, ProfileSerializer, RecordsSerializer
from apps.models import Profile, State, Municipality, Contract, Receipt, TipsAndAdvertising, Rate, Records
from rest_framework.decorators import detail_route, api_view
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
from rest_framework.views import APIView
from django.core.mail import send_mail, EmailMessage
from dateutil.easter import *
from dateutil.relativedelta import *
from dateutil.rrule import *
from dateutil.parser import *
from datetime import *
import time

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_queryset(self):
        user = self.request.GET.get('user_id')
        if user:
            self.queryset = self.queryset.filter(user_id = user)

        return self.queryset



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
    permission_classes = (IsAuthenticated,)

    # ©detail_route(methods=['patch'])
    # def partial_update(self, request, pk=None):
    #     obj = Receipt.objects.get(id= pk)
    #     data = request.data['current_data']
    #     obj.current_data = obj.current_data + int(data)
    #     obj.save()
    #
    #     return Response({ 'Message': 'Se ha actualizado'})

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

    def get_queryset(self):
        names_rates = self.request.GET.get('name_rate')
        if names_rates:
            self.queryset = self.queryset.filter(name_rate = names_rates)

        return self.queryset


# Tarifas por Municipio

class Mun_RateList(viewsets.ModelViewSet):
    """
    API Lista de tarifas por Municipio
    """
    queryset = Municipality.objects.all()
    serializer_class = Mun_RateSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        municipality = self.request.GET.get('mun_id')
        if municipality:
            self.queryset = self.queryset.filter(id = municipality)
        return self.queryset

# Tarifas por Periodo
class Rate_PeriodList(viewsets.ModelViewSet):


    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # period = self.request.GET.get('period')
        # if period:
        #     self.queryset = self.queryset.filter(period_name= period)
        rate = self.request.GET.get('rate')
        if rate:
            self.queryset = self.queryset.filter(name_rate= rate)

        return self.queryset



class ContactUs(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        # name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        description = request.POST.get('message') + ' Mensaje enviado por: ' + email
        send_email = EmailMessage(subject,description,email,['contactos@easylight.com.mx'],)
        res = send_email.send()
        print(request)

        return Response({ 'Message': 'Mensaje Enviado'})

class Subscribe(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        name = 'Este es un mail de suscriptores'
        email = request.POST.get('email')
        description = email + ' solicitó una suscripción '
        # description = request.POST.get('message') + ' Mensaje enviado por: ' + email
        send_email = EmailMessage(name,description,email,['contactos@easylight.com.mx'],)
        res = send_email.send()

        return Response({ 'Message': 'Suscripción Enviado'})

class RecordsList(viewsets.ModelViewSet):

    queryset = Records.objects.all()
    serializer_class = RecordsSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        contract_id = self.request.GET.get('contract_id')
        date = self.request.GET.get('date')
        if contract_id:
            self.queryset = self.queryset.filter(contracts= contract_id)
        if date:
            self.queryset = [self.queryset.filter(contracts= contract_id, date= date).last()]
        return self.queryset

    def diferencia(self, fecha, initialDate):
        formato_fecha = "%Y-%m-%d"
        fecha_inicial = datetime.strptime(fecha, formato_fecha)
        fecha_actual = datetime.strptime(initialDate, formato_fecha)
        resultado = relativedelta(fecha_actual, fecha_inicial)
        
        # print(resultado.days, 'dias',resultado.hours, 'horas', resultado.minutes, 'minutos')

        return resultado

    def update(self, request, pk=None):
        record = self.get_queryset()
        date = request.data['date']
        day = request.data['day']
        daily_reading = request.data['daily_reading']
        rest_day = request.data['rest_day']
        listRecords = Records.objects.all()
        initialDate = time.strptime(date, '%Y-%m-%d')
        
        for recordItem in listRecords:
            dateItem = datetime.strftime(recordItem.date, '%Y-%m-%d')
            dateItem = time.strptime(dateItem, '%Y-%m-%d')
            if(dateItem > initialDate):
                diffDate = self.diferencia(date, datetime.strftime(recordItem.date, '%Y-%m-%d'))
                recordItem.hours_totals = diffDate.hours + (diffDate.days*24)
                recordItem.days_totals = diffDate.days
                recordItem.save()

        # hours_elapsed = request.data['hours_elapsed']
        # hours_totals= request.data['hours_totals']
        # days_elapsed= request.data['days_elapsed']
        # days_totals= request.data['days_totals']
        # daily_consumption= request.data['daily_consumption']
        # cumulative_consumption= request.data['cumulative_consumption']
        # average_global= request.data['average_global']
        # rest_day= request.data['rest_day']
        # projection= request.data['projection']
        # projected_payment= request.data['projected_payment']
        # contracts= request.data['contracts']
        itemRecord = record[0]
        itemRecord.daily_reading = 0
        itemRecord.hours_elapsed = 0
        itemRecord.hours_totals = 0
        itemRecord.days_elapsed = 0
        itemRecord.days_totals = 0
        itemRecord.daily_consumption = 0
        itemRecord.cumulative_consumption = 0
        itemRecord.average_global = 0
        itemRecord.rest_day = rest_day
        itemRecord.projection = 0
        itemRecord.projected_payment = 0
        # itemRecord.contracts = contracts
        itemRecord.day = day
        itemRecord.daily_reading = daily_reading

        itemRecord.save()

        return Response({ 'Message': 'Record Actualizado'})

    