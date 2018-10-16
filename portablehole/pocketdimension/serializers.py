from rest_framework import serializers
from . import models


class SystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.System
        fields = '__all__'


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Type
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Item
        fields = '__all__'


class PortableHoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PortableHole
        fields = '__all__'


class UserItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserItem
        fields = '__all__'
