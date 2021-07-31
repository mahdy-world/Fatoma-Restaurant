from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import  serializers
from .models import *


# Serializers define the API representation.
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'phone']


