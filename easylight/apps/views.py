from django.contrib.auth.models import User, Group
from rest_framework.generics import ListCreateAPIView
from apps.serializers import UserSerializer, GroupSerializer, StateSerializer, MunicipalitySerializer
from apps.models import State, Municipality
from rest_framework.decorators import api_view
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets, renderers

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
    API State
    """
    queryset = State.objects.all()
    serializer_class = StateSerializer

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        state = self.get_object()
        return Response(state.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class MunicipalityList(ListCreateAPIView):
    """
    API Municipality
    """
    queryset = Municipality.objects.all()
    serializer_class = MunicipalitySerializer
