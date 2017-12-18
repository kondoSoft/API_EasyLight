from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from rest_framework.generics import ListCreateAPIView
from apps.serializers import RateSerializer, UserSerializer, GroupSerializer, ContractSerializer, TipsAndAdvertisingSerializer, ReceiptSerializer, StateSerializer, MunicipalitySerializer, RateSerializer, Mun_RateSerializer, ProfileSerializer, RecordsSerializer, HistorySerializer, RateHighConsumptionSerializer, LimitRateDacSerializer
from apps.models import Profile, State, Municipality, Contract, Receipt, TipsAndAdvertising, Rate, Records, History, RateHighConsumption, LimitRateDac
from rest_framework.decorators import detail_route, api_view, list_route
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets, renderers
import xlrd
from xlrd import open_workbook, cellname
from django.http import HttpResponse, JsonResponse
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
from django.core import serializers
import json

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
    # permission_classes = (IsAuthenticated,)

    def create(self, *arg,**kwargs):
        # data = self.request.data
        contract = Contract()

        high_consumption = self.request.POST.get('high_consumption')
        if high_consumption == 'true' :
            high_consumption = True
        else:
            high_consumption = False

        contract.municipality_id= self.request.POST.get('municipality')
        contract.name_contract = self.request.POST.get('name_contract')
        contract.number_contract = self.request.POST.get('number_contract')
        contract.state_id = self.request.POST.get('state')
        contract.type_payment = self.request.POST.get('type_payment')
        contract.rate = self.request.POST.get('rate')
        contract.initialDateRange = self.request.POST.get('initialDateRange')
        contract.finalDateRange = self.request.POST.get('finalDateRange')
        contract.high_consumption = high_consumption
        contract.owner_id = self.request.POST.get('owner')

        if(len(self.request.FILES) > 0):
            image = self.request.FILES['image']
            contract.image = image
        contract.save()
        receipts = Receipt.objects.filter(contract= contract.id)
        # return Response( {'results': { 'name_contract': contract.name_contract, 'number_contract': contract.number_contract}} )
        # return Response(data)
        return Response({ "id": contract.id, "number_contract": contract.number_contract, "receipt": receipts, "type_payment": contract.type_payment, "rate": contract.rate})

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        id_owner = self.request.user
        profile = Profile.objects.filter(pk= id_owner)
        query = self.queryset.filter(owner = id_owner)

        self.queryset = query

        return self.queryset

    def update(self, request, pk=None):
        contract_id = request.data['contract_id']
        contracts = Contract.objects.get(pk= contract_id)
        rate = request.data['rate']
        print(request.data)
        try:
            high_consumption = request.data['high_consumption']
            if( high_consumption ):
                print('true')
                high_consumption == True
                contracts.high_consumption = high_consumption
            else:
                print('false')
                high_consumption == False
                contracts.high_consumption = high_consumption
        except:
            pass

        if(len(request.FILES) > 0):
            image = request.FILES['image']
            contracts.image = image


        contracts.rate = rate



        contracts.save()


        return Response({'Message': 'Se actualizo el contrato'})

class ReceiptList(viewsets.ModelViewSet):
    """
    API Contratos
    """
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer
    # permission_classes = (IsAuthenticated,)

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

class HistoryList(viewsets.ModelViewSet):
    """
    API History
    """
    queryset = History.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = HistorySerializer

    def get_queryset(self):
        contract_id = self.request.GET.get('contract_id')
        if contract_id:
            self.queryset = self.queryset.filter(contract = contract_id)

        return self.queryset

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
    # permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        municipality = self.request.GET.get('mun_id')
        if municipality:
            self.queryset = self.queryset.filter(id = municipality)
        return self.queryset

# Tarifas por Periodo
class Rate_PeriodList(viewsets.ModelViewSet):


    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    # permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # period = self.request.GET.get('period')
        # if period:
        #     self.queryset = self.queryset.filter(period_name= period)
        rate = self.request.GET.get('rate')
        if rate:
            self.queryset = self.queryset.filter(name_rate= rate)

        return self.queryset


class ContactUs(APIView):
    # permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        # name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        description = request.POST.get('message') + ' Mensaje enviado por: ' + email
        send_email = EmailMessage(subject,description,email,['contactos@easylight.com.mx'],)
        res = send_email.send()

        return Response({ 'Message': 'Mensaje Enviado'})

class RegionView(viewsets.ModelViewSet):

    queryset = LimitRateDac.objects.all()
    serializer_class = LimitRateDacSerializer
    # permission_classes = (IsAuthenticated,)

class RateHighConsumptionView(viewsets.ModelViewSet):

    queryset = RateHighConsumption.objects.all()
    serializer_class = RateHighConsumptionSerializer
    # permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        region_id = self.request.GET.get('region_id')
        if region_id:
            self.queryset = self.queryset.filter(region = region_id)

        return self.queryset

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

        date = request.data['date']
        datetime = request.data['datetime']
        daily_reading = request.data['daily_reading']
        rest_day = request.data['rest_day']
        projected_payment = request.data['projected_payment']
        status = request.data['status']
        contract_id = request.data['contracts']
        amount_payable = request.data['amount_payable']
        total_days = request.data['total_days']
        dac = request.data['dac']
        high_consumption = request.data['jsonFuncHigh']
        if high_consumption:
            high_consumption = request.data['jsonFuncHigh']
        else:
            high_consumption = ''

        if status :
            status = True
        else:
            status = False

        if record[0] != None:
            self.update_next_records(record[0], request.data['ratePeriod'], date, total_days, dac, high_consumption)
            itemRecord = record[0]
            itemRecord.hours_elapsed = 0
            itemRecord.hours_totals = 0
            itemRecord.datetime = date +'T12:00Z'
            itemRecord.days_elapsed = 0
            itemRecord.days_totals = 0
            itemRecord.daily_consumption = 0
            itemRecord.cumulative_consumption = 0
            itemRecord.average_global = 0
            itemRecord.rest_day = total_days
            itemRecord.projection = 0
            itemRecord.date = date
            itemRecord.projected_payment = 0
            itemRecord.amount_payable = amount_payable
            itemRecord.daily_reading = daily_reading
            itemRecord.status = status
            itemRecord.save()
            return Response({ 'Message': 'Record Actualizado'})

        else :
            contract = Contract.objects.get(pk= contract_id)
            newRecord = Records()
            newRecord.hours_elapsed = 0
            newRecord.hours_totals = 0
            newRecord.days_elapsed = 0
            newRecord.days_totals = 0
            newRecord.daily_consumption = 0
            newRecord.cumulative_consumption = 0
            newRecord.average_global = 0
            newRecord.rest_day = rest_day
            newRecord.projection = 0
            newRecord.date = date
            newRecord.projected_payment = 0
            newRecord.daily_reading = daily_reading
            newRecord.status = status
            newRecord.contracts = contract
            newRecord.datetime = datetime
            newRecord.amount_payable = amount_payable
            newRecord.save()
            return Response({'Message': 'Se agrego un nuevo Record'})

    def update_next_records(self, record, ratePeriod, date, total_days, dac, high_consumption):
        formato_fecha = "%Y-%m-%d %H:%M:%S"
        listRecords = Records.objects.filter(date__gte= record.date, daily_reading__gt= record.daily_reading ).order_by('daily_reading')
        dateRecord = datetime.strftime(record.datetime, formato_fecha)
        for idx,recordItem in enumerate(listRecords):
            dateItem = datetime.strftime(recordItem.datetime, formato_fecha)
            if(listRecords[0]):
                dateRecord = date +' 12:00:00'

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

            recordItem.rest_day = total_days - recordItem.days_totals

            # Consumo acumulado es la lectura actual menos el valor de la lectura actual del record que se actualizo
            cumulative_consumption = float(recordItem.daily_reading) - float(record.daily_reading)
            recordItem.cumulative_consumption = round(cumulative_consumption, 3)

            #variable para sacar el average
            if (recordItem.days_totals > 0):
                average_global = float(recordItem.cumulative_consumption) / float(recordItem.days_totals)
            else:
                average_global = float(recordItem.cumulative_consumption)

            recordItem.average_global = round(average_global, 3)
            #varible para sacar la proyeccion
            multProjection = float(recordItem.rest_day) * average_global
            projection = multProjection + recordItem.cumulative_consumption
            recordItem.projection = round(projection, 3)
            if(dac):
                recordItem.projected_payment = self.getHighConsumption(high_consumption, recordItem.projection)
            else:
                recordItem.projected_payment = self.getCostProjected(ratePeriod, recordItem.projection)

            # recordItem.projected_payment = self.getCostProjected(ratePeriod, recordItem.projection)

            recordItem.save()

    def getIVA (self, total):
          if(total):
              iva = 1.16
              return total * iva

    def getHighConsumption(self, high_consumption, projection):
        if(high_consumption['typeSummer'] == 'verano'):
            costProjectDac = (high_consumption['typePayment'] * float(high_consumption['arrHighConsumption'][0]['fixedCharge'])) + (float(high_consumption['arrHighConsumption'][0]['kwhVerano']) * projection)
        elif(high_consumption['typeSummer'] == 'mixtoVerano'):
            costProjectDac =(high_consumption['typePayment'] * float(high_consumption['arrHighConsumption'][0]['fixedCharge'])) + (float(high_consumption['arrHighConsumption'][0]['kwhVerano']) * projection)
        elif(high_consumption['typeSummer'] == 'mixtoNoVerano'):
            costProjectDac =(high_consumption['typePayment'] * float(high_consumption['arrHighConsumption'][0]['fixedCharge'])) + (float(high_consumption['arrHighConsumption'][0]['kwhNoVerano']) * projection)
        else:
            costProjectDac = (high_consumption['typePayment'] * float(high_consumption['arrHighConsumption'][0]['fixedCharge'])) + (float(high_consumption['arrHighConsumption'][0]['kwhNoVerano']) * projection)

        costProjectDac = self.getIVA(costProjectDac)

        return costProjectDac

    def getCostProjected(self, ratePeriod, projection):

        consumoTotal = 0
        if (ratePeriod):
            ratePeriod.reverse()
            ratePeriod = list(filter(lambda x: float(x['cost'])> 0, ratePeriod))
        while (projection >= 0 and len(ratePeriod) > 0):
            range = ratePeriod.pop()
            valueKilowatt = range['kilowatt']
            if(projection > valueKilowatt):
                consumo = projection - valueKilowatt
                projection -= valueKilowatt
                consumo = valueKilowatt * float(range['cost'])
                consumoTotal += consumo
            if (len(ratePeriod) == 0 and projection > 0):
                consumo = projection * float(range['cost'])
                consumoTotal += consumo

        consumoTotal = self.getIVA(consumoTotal)
        return consumoTotal
