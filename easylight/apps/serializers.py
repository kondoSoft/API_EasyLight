from django.contrib.auth.models import User, Group
from rest_framework import serializers
from apps.models import State, Municipality

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    highlight = serializers.HyperlinkedIdentityField(view_name='group-highlight', format='html')

    class Meta:
        model = Group
        fields = ('url','highlight', 'name')

class StateSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = State
        fields = ('key_state','state', 'abbreviation')

class MunicipalitySerializer(serializers.HyperlinkedModelSerializer):
    state = serializers.HyperlinkedIdentityField(many=False, view_name='state-detail', read_only=False)

    class Meta:
        model = Municipality
        fields = ('state', 'key_mun', 'name_mun')
