from django.utils import timezone
from datetime import datetime
from rest_framework import serializers

from django.utils.html import linebreaks

from .models import Conference, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class ConferenceSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    conf_status = serializers.SerializerMethodField()
    conf_s_desc = serializers.SerializerMethodField()
    conf_desc = serializers.SerializerMethodField()

    def get_conf_status(self, obj):
        current_date = timezone.now().date()
        if obj.conf_date_begin is None or obj.conf_date_end is None:
            return "Дата уточняется"
        else:
            conf_date_begin = obj.conf_date_begin
            conf_date_end = obj.conf_date_end if obj.conf_date_end else None
            if conf_date_begin <= current_date <= conf_date_end:
                return "Конференция идёт"
            elif (conf_date_begin - current_date).days <= 14 and current_date < conf_date_begin:
                return "Конференция скоро начнётся"
            else:
                return "Конференция запланирована" if conf_date_begin > current_date else "Конференция окончена"

    def get_conf_s_desc(self, obj):
        formatted_text = linebreaks(obj.conf_s_desc)
        return formatted_text.replace('\n', '').replace('\t', '')

    def get_conf_desc(self, obj):
        formatted_text = linebreaks(obj.conf_desc)
        return formatted_text.replace('\n', '').replace('\t', '')

    class Meta:
        model = Conference
        fields = ('id', 'conf_id', 'hash', 'un_name', 'local',
                  'reg_date_begin', 'reg_date_end', 'conf_date_begin',
                  'conf_date_end', 'conf_card_href', 'reg_href',
                  'conf_name', 'conf_s_desc', 'conf_desc', 'org_name',
                  'themes', 'online', 'conf_href', 'offline', 'conf_address',
                  'contacts', 'rinc', 'tags', 'vak', 'wos', 'scopus', 'conf_status')
