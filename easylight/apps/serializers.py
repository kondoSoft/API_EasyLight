from django.contrib.auth.models import User, Group
from rest_framework import serializers
from apps.models import State, Municipality,TipsAndAdvertising, TableRate, Contract, Receipt

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    highlight = serializers.HyperlinkedIdentityField(view_name='group-highlight', format='html')

    class Meta:
        model = Group
        fields = ('url','highlight', 'name')
# Estados
class StateSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = State
        fields = ('key_state','state', 'abbreviation')
# Municipios
class MunicipalitySerializer(serializers.HyperlinkedModelSerializer):
    state = serializers.HyperlinkedIdentityField(many=False, view_name='state-detail', read_only=False)

    class Meta:
        model = Municipality
        fields = ('state', 'key_mun', 'name_mun')

# Tabla de Tarifas
class TableRateSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = TableRate
        fields = ('name', 'precio',)

# Datos de Contratos
class ContractSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contract
        fields = ('name_contract', 'number_contract', 'state', 'municipality', 'rate', 'period_summer', 'type_payment', 'receipt')
# Datos de Recibos de Luz
class ReceiptSerializer(serializers.ModelSerializer):

    class Meta:
        model = Receipt
        fields = ('payday_limit', 'amount_payable', 'current_reading', 'previous_reading', 'current_data')

# TipsAndAdvertising

class TipsAndAdvertisingSerializer(serializers.ModelSerializer):

    class Meta:
        model = TipsAndAdvertising
        fields = ('name_tip_advertising', 'type_data',)
