from django.contrib.auth.models import User, Group
from rest_framework import serializers
from apps.models import State, Municipality,TipsAndAdvertising, Contract, Receipt, Rate
import json
from rest_auth.registration.serializers import RegisterSerializer

class UserSerializer(serializers.ModelSerializer):
    contracts = serializers.PrimaryKeyRelatedField(many=True, queryset=Contract.objects.all())

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups', 'contracts')

class RegistrationSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)


class GroupSerializer(serializers.ModelSerializer):
    # highlight = serializers.HyperlinkedIdentityField(view_name='group-highlight', format='html')

    class Meta:
        model = Group
        fields = ('id', 'url', 'name')
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


class ContractsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contract
# Datos de Recibos de Luz
class ReceiptSerializer(serializers.ModelSerializer):
    payday_limit = serializers.DateField(format="%d-%B-%Y", required=True, read_only=False)

    class Meta:
        model = Receipt
        fields = ('id', 'contract', 'payday_limit', 'amount_payable', 'current_reading', 'previous_reading', 'current_data')


# Datos de Contratos
class ContractSerializer(serializers.ModelSerializer):
    receipt = serializers.SerializerMethodField()
    image = serializers.ImageField()
    owner = serializers.ReadOnlyField(source='owner.id')

    def get_receipt(self, obj):
        listReceipt = []
        receipts = Receipt.objects.all().filter(contract=obj.pk)
        for receipt in receipts:
            bill = {'id': receipt.id, 'payday_limit': receipt.payday_limit, 'amount_payable': receipt.amount_payable,'current_reading': receipt.current_reading,'previous_reading': receipt.previous_reading, 'current_data': receipt.current_data}
            listReceipt.append(bill)
        return listReceipt

    class Meta:
        model = Contract
        fields = ('id','name_contract', 'number_contract', 'state', 'municipality', 'rate', 'period_summer', 'type_payment', 'receipt', 'image','owner')

# TipsAndAdvertising

class TipsAndAdvertisingSerializer(serializers.ModelSerializer):

    class Meta:
        model = TipsAndAdvertising
        fields = ('name_tip_advertising', 'type_data',)
