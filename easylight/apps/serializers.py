from django.contrib.auth.models import User, Group
from allauth.account import app_settings as allauth_settings
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from apps.models import Profile, State, Municipality,TipsAndAdvertising, Contract, Receipt, Rate
import json
from rest_auth.registration.serializers import RegisterSerializer

class UserSerializer(serializers.ModelSerializer):
    contracts = serializers.PrimaryKeyRelatedField(many=True, queryset=Contract.objects.all())

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups', 'contracts')

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('__all__')


class RegistrationSerializer(RegisterSerializer):
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)
    birth_date = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    zip_code = serializers.IntegerField(required=False)
    avatar = serializers.ImageField(required=False)

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(_("Los dos campos de contraseña no coinciden."))
        return data


    def get_cleaned_data(self):
        return {
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'birth_date': self.validated_data.get('birth_date', ''),
            'phone': self.validated_data.get('phone', ''),
            'zip_code': self.validated_data.get('zip_code', ''),
            'avatar': self.validated_data.get('avatar', ''),
        }
    # def put(self, request):
    #     avatar = request.FILES.get('avatar')
    #

    def save(self, request):
        phone= request.POST.get('phone')
        birth_date = request.POST.get('birth_date')
        zip_code = request.POST.get('zip_code')
        avatar = request.FILES.get('avatar')
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        user.save()
        profile = Profile()
        profile.phone = phone
        profile.birth_date = birth_date
        profile.zip_code = zip_code
        profile.user = user
        profile.avatar = avatar
        profile.save()
        return user

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

class Mun_RateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Municipality
        fields = ('rate',)

# Datos de Recibos de Luz
class ReceiptSerializer(serializers.ModelSerializer):
    payday_limit = serializers.DateField(format="%d-%B-%Y", required=True, read_only=False)
    update_date = serializers.DateField(format="%d-%b-%Y", required=False, read_only=False)

    class Meta:
        model = Receipt
        fields = ('id', 'contract', 'payday_limit', 'amount_payable', 'current_reading', 'previous_reading', 'update_date', 'period')


# Datos de Contratos
class ContractSerializer(serializers.ModelSerializer):
    receipt = serializers.SerializerMethodField()
    image = serializers.ImageField(required=False)
    owner = serializers.ReadOnlyField(source='owner.id')

    def get_receipt(self, obj):
        listReceipt = []
        receipts = Receipt.objects.all().filter(contract=obj.pk)
        for receipt in receipts:
            bill = {'id': receipt.id, 'payday_limit': receipt.payday_limit, 'amount_payable': receipt.amount_payable,'current_reading': receipt.current_reading,'previous_reading': receipt.previous_reading, 'update_date': receipt.update_date, 'period': receipt.period}
            listReceipt.append(bill)
        return listReceipt

    class Meta:
        model = Contract
        fields = ('id','name_contract', 'number_contract', 'state', 'municipality', 'rate','initialDateRange', 'finalDateRange', 'type_payment', 'receipt', 'image','owner')

# TipsAndAdvertising

class TipsAndAdvertisingSerializer(serializers.ModelSerializer):

    class Meta:
        model = TipsAndAdvertising
        fields = ('name_tip_advertising', 'description','image',)
