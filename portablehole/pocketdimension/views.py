from . import models
from . import serializers
from rest_framework import generics


class SystemList(generics.ListAPIView):
    queryset = models.System.objects.all()
    serializer_class = serializers.SystemSerializer


class TypeList(generics.ListAPIView):
    queryset = models.Type.objects.all()
    serializer_class = serializers.TypeSerializer


class CategoryList(generics.ListAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.TypeSerializer
    filter_fields = ('system__id', 'system__name',)


class ItemList(generics.ListAPIView):
    queryset = models.Item.objects.all()
    serializer_class = serializers.ItemSerializer
    filter_fields = ('system__id', 'system__name',)


class PortableHoleList(generics.ListCreateAPIView):
    queryset = models.PortableHole.objects.all()
    serializer_class = serializers.PortableHoleSerializer

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
