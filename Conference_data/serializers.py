from django.utils import timezone
from rest_framework import serializers

from .models import Conference, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class ConferenceSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    conf_status = serializers.SerializerMethodField()

    class Meta:
        model = Conference
        fields = ('id', 'conf_id', 'hash', 'un_name', 'local',
                  'reg_date_begin', 'reg_date_end', 'conf_date_begin',
                  'conf_date_end', 'conf_card_href', 'reg_href',
                  'conf_name', 'conf_s_desc', 'conf_desc', 'org_name',
                  'themes', 'online', 'conf_href', 'offline', 'conf_address',
                  'contacts', 'rinc', 'tags', 'conf_status')

    def get_conf_status(self, obj):
        current_date = timezone.now().date()
        if obj.conf_date_begin is None or obj.conf_date_end is None:
            return "unclear"
        elif obj.conf_date_begin <= current_date <= obj.conf_date_end:
            return "ongoing"
        else:
            return "upcoming" if obj.conf_date_begin > current_date else "past"
