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
        kwh = self.request.GET.get('kwh')
        if contract_id:
            self.queryset = self.queryset.filter(contracts= contract_id)
        if date:
            date = datetime.strptime(date, "%Y-%m-%d")
            self.queryset = self.queryset.filter(date__gt= date)
        if kwh:
            self.queryset = [self.queryset.filter(daily_reading__gte= kwh).last()]
        return self.queryset

    def diferencia(self, initialDate, finalDate):
        formato_fecha = "%Y-%m-%d %H:%M:%S"
        fecha_inicial = datetime.strptime(initialDate, formato_fecha)
        fecha_actual = datetime.strptime(finalDate, formato_fecha)
        diferenciaDias = fecha_actual - fecha_inicial

        return diferenciaDias

    def update(self, request, pk=None):
        record = self.get_queryset()
        # listRecords = Records.objects.all()
        date = request.data['date']
        daily_reading = request.data['daily_reading']
        rest_day = request.data['rest_day']
        projected_payment = request.data['projected_payment']
        print(record)
        self.update_next_records(record[0])
        
        itemRecord = record[0]
        itemRecord.hours_elapsed = 0
        itemRecord.hours_totals = 0
        itemRecord.days_elapsed = 0
        itemRecord.days_totals = 0
        itemRecord.daily_consumption = 0
        itemRecord.cumulative_consumption = 0
        itemRecord.average_global = 0
        itemRecord.rest_day = rest_day
        itemRecord.projection = 0
        itemRecord.projected_payment = projected_payment
        itemRecord.daily_reading = daily_reading
        itemRecord.save()

        return Response({ 'Message': 'Record Actualizado'})

    def update_next_records(self, record):
        formato_fecha = "%Y-%m-%d %H:%M:%S"
        listRecords = Records.objects.filter(date__gte= record.date, daily_reading__gt= record.daily_reading ).order_by('daily_reading')
        dateRecord = datetime.strftime(record.datetime, formato_fecha)
        for idx,recordItem in enumerate(listRecords):
            dateItem = datetime.strftime(recordItem.datetime, formato_fecha)
            diffDate = self.diferencia(dateRecord, dateItem)
            
            hours= (diffDate.days * 24) + (diffDate.seconds/3600) 
            # Condicion para hacer la variacion de datos dependiendo el item del array
            if idx == 0:
                index = 0
                hours_elapsed = hours
                days_elapsed = hours/24

            else:
                index = idx-1
                hours_elapsed = float(recordItem.hours_totals) - float(listRecords[index].hours_totals)
                days_elapsed = float(recordItem.days_totals) - float(listRecords[index].days_totals)

            recordItem.hours_totals = round(hours, 3)
            recordItem.hours_elapsed = round(hours_elapsed,3)
            recordItem.days_elapsed = round(days_elapsed, 3)
            recordItem.days_totals = round(hours / 24 , 3)
            # Consumo acumulado es la lectura actual menos el valor de la lectura actual del record que se actualizo
            cumulative_consumption = float(recordItem.daily_reading) - float(record.daily_reading)
            recordItem.cumulative_consumption = round(cumulative_consumption, 3)
            #variable para sacar el average
            average_global = float(recordItem.cumulative_consumption) / float(recordItem.days_totals)
            recordItem.average_global = round(average_global, 3)
            #varible para sacar la proyeccion
            multProjection = float(recordItem.rest_day) * average_global
            projection = multProjection + recordItem.cumulative_consumption
            recordItem.projection = round(projection, 3)
            recordItem.save()
            
    