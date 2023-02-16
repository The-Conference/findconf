from rest_framework import serializers
from .models import Conference


class ConferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conference
        fields = ('name', 'logo', 'short_description', 'url',
                  'date', 'full_description', 'place', 'organizer')
