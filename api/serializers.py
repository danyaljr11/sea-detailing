from rest_framework import serializers
from .models import Request, Picture


class Request_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = '__all__'


class Picture_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = '__all__'
