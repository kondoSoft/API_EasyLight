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


class ContractsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
# Datos de Recibos de Luz
class ReceiptSerializer(serializers.ModelSerializer):
    payday_limit = serializers.DateField(format="%d-%B-%Y", required=True, read_only=False)
    contract = serializers.SerializerMethodField()
    # contract = serializers.PrimaryKeyRelatedField(many=False, source=Contract, read_only=True)
    # contract = ContractsSerializer(many=False, read_only=False)

    def get_contract(self, obj):
        listContract = []
        contract = Contract.objects.filter(receipt=obj.pk)
        for contract in contract:
            listContract.append((contract.id, contract.name_contract, contract.number_contract))
        return listContract

    # def create(self, validation_data):
    #     # print(self.contract)
    #     # contract_id = Contract.objects.get(id=self.id)
    #     receipt = Receipt.objects.create(**validation_data)
    # #     # contract_id.objects.create(receipt=receipt)
    #     receipt.save()
    #     return receipt

    class Meta:
        model = Receipt
        fields = ('id', 'contract', 'payday_limit', 'amount_payable', 'current_reading', 'previous_reading', 'current_data')


# Datos de Contratos
class ContractSerializer(serializers.ModelSerializer):
    receipt = ReceiptSerializer(many=True, read_only=True)
    class Meta:
        model = Contract
        fields = ('id','name_contract', 'number_contract', 'state', 'municipality', 'rate', 'period_summer', 'type_payment', 'receipt')

# TipsAndAdvertising

class TipsAndAdvertisingSerializer(serializers.ModelSerializer):

    class Meta:
        model = TipsAndAdvertising
        fields = ('name_tip_advertising', 'type_data',)
