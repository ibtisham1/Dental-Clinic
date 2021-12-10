from rest_framework import serializers
from .models import Booking
"""Garner, B. (2020). Build your first REST API with Django REST Framework. [online] Medium. 
Available at: https://medium.com/swlh/build-your-first-rest-api-with-django-rest-framework-e394e39a482c."""

"""	Title: Build a REST API in 30 minutes with Django REST Framework

*	Author: Bennet Garner
*	Date: 19th November, 2020
*	Code version: None
*	Availability: https://medium.com/swlh/build-your-first-rest-api-with-django-rest-framework-e394e39a482c
*
****************************************************************************
"""
class BookingSer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Booking
        fields = ['title', 'notes', 'id', 'importance', 'length', 'approved', 'date']