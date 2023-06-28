from django.utils import timezone
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

    def get_conf_status(self, obj) -> str:
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

    def get_conf_s_desc(self, obj) -> str:
        formatted_text = linebreaks(obj.conf_s_desc)
        return formatted_text.replace('\n', '').replace('\t', '')

    def get_conf_desc(self, obj) -> str:
        formatted_text = linebreaks(obj.conf_desc)
        return formatted_text.replace('\n', '').replace('\t', '')

    def create(self, validated_data):
        tag_list = None
        if 'tags' in validated_data:
            tags_data = validated_data.pop('tags')
            tag_list = self.get_new_tags(tags_data)

        conf = Conference.objects.create(**validated_data)
        if tag_list:
            conf.tags.set(tag_list)
        return conf

    def update(self, instance, validated_data):
        if 'tags' in validated_data:
            tags_data = validated_data.pop('tags')
            tag_list = self.get_new_tags(tags_data)
            instance.tags.set(tag_list, clear=True)
        return super().update(instance, validated_data)

    @staticmethod
    def get_new_tags(tag_data: list) -> list[Tag]:
        tag_list = []
        for tag_data in tag_data:
            tag, _ = Tag.objects.get_or_create(**tag_data)
            tag_list.append(tag)
        return tag_list

    class Meta:
        model = Conference
        fields = ('id', 'conf_id', 'hash', 'un_name', 'local',
                  'reg_date_begin', 'reg_date_end', 'conf_date_begin',
                  'conf_date_end', 'conf_card_href', 'reg_href',
                  'conf_name', 'conf_s_desc', 'conf_desc', 'org_name',
                  'themes', 'online', 'conf_href', 'offline', 'conf_address',
                  'contacts', 'rinc', 'tags', 'vak', 'wos', 'scopus', 'conf_status')
