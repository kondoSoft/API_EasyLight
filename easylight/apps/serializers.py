from django.contrib.auth.models import User, Group
from rest_framework import serializers
from apps.models import State, Municipality,TipsAndAdvertising, Contract, Receipt, Rate

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
class StateSerializer(serializers.ModelSerializer):

    class Meta:
        model = State
        fields = ('id','state', 'abbreviation')
# Municipios
class MunicipalitySerializer(serializers.ModelSerializer):
    state = StateSerializer(many=False, read_only=True)

    class Meta:
        model = Municipality
        fields = ('id','key_mun','name_mun','state')

# Tabla de Tarifas
class RateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rate
        fields = ('__all__')

class RateNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rate
        fields = ('name_rate',)
# Datos de Contratos
class ContractSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contract
        fields = ('id','name_contract', 'number_contract', 'state', 'municipality', 'rate', 'period_summer', 'type_payment', 'receipt')
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
